# -*- coding: utf-8 -*-
"""
---

title:
    "Kazul application state."

description:
    "This module defines Kazul application state."

id:
    "14711bf2-7646-4b73-b985-61c35673348e"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."


"""


import asyncio

import reflex


# =============================================================================
class WorkItemField(reflex.Base):
    """
    """
    name:       str
    content:    str
    criteria:   str
    assessment: str


# =============================================================================
class WorkItem(reflex.Base):
    """
    A work item.

    """
    title:      str
    list_field: list[WorkItemField]


# =============================================================================
class App(reflex.State):
    """
    Kazul application state.

    """

    # Command input
    # =============
    #
    # - str_cmd_input  - Content of command input box.
    # - _job_queue     - Job queue for interactions with the LLM.
    # - _count_workers - Count active workers handling LLM interactions.
    #
    str_cmd_input:  str           = ''
    _job_queue:     asyncio.Queue = asyncio.Queue()
    _count_workers: int           = 0

    # Items
    # =====

    list_work_item: list[WorkItem] = [
        WorkItem(
            title      = 'Work Item #1',
            list_field = [
                WorkItemField(name       = 'A thing',
                              content    = 'Some sort of content to review',
                              criteria   = '',
                              assessment = ''),
                WorkItemField(name       = 'Another thing',
                              content    = 'More content to review',
                              criteria   = '',
                              assessment = '')]),
        WorkItem(
            title      = 'Work Item #2',
            list_field = [
                WorkItemField(name       = 'key3',
                              content    = 'value3',
                              criteria   = '',
                              assessment = ''),
                WorkItemField(name       = 'key4',
                              content    = 'value4',
                              criteria   = '',
                              assessment = '')])]


    # -------------------------------------------------------------------------
    @reflex.background
    async def handle_page_index_on_load(self):
        """
        Handle the on_load event on the index page.

        """
        pass

    # -------------------------------------------------------------------------
    @reflex.background
    async def handle_btn_cmd_submit(self, form_data):
        """
        Handle the on_clicked callback on the submit button.

        """

        await self._enqueue_llm_interaction(input = form_data['input'])

    # -------------------------------------------------------------------------
    async def _enqueue_llm_interaction(self, input):
        """
        Enqueue a new interaction with the LLM.

        """

        # Work out if we are starting a new
        # conversation or continuing an old
        # one.
        #
        job = dict(input = input)

        # Enqueue the job.
        #
        async with self:
            self._job_queue.put_nowait(job)

        # Start a worker to process the job queue
        # if required.
        #
        await self._ensure_job_queue_is_being_worked_on()

    # -------------------------------------------------------------------------
    async def _ensure_job_queue_is_being_worked_on(self):
        """
        If required, process all items in the job queue, halting when empty.

        """

        # Ensure only one worker is active at a time.
        #
        async with self:
            if self._count_workers > 0:
                return
            else:
                self._count_workers += 1

        # Empty the job queue, processing all items.
        #
        try:

            while True:
                try:
                    async with self:
                        job = self._job_queue.get_nowait()
                    await self._process_one_job(job)
                except asyncio.QueueEmpty:
                    break

        finally:
            async with self:
                self._count_workers -= 1

    # -------------------------------------------------------------------------
    async def _process_one_job(self, job):
        """
        """

        if job['input']:
            async with self:
                self._append_new_transcript_entry('USR', job['input'])


    # -------------------------------------------------------------------------
    def _append_new_transcript_entry(self, role, content):
        """
        Add a new entry to the end of the transcript for the current stage.

        """

        self.component_display.append(dict(role    = role,
                                           content = content))
