# -*- coding: utf-8 -*-
"""
---

title:
    "Gradio NLP demo support module."

description:
    "This Python module is designed to
    interact with a Gradio UI that is
    running in a separate process."

id:
    "f42feb22-a8dd-4c66-9968-475cb4c78e94"

type:
    dt004_python_stableflow_edict_component

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

...
"""


import itertools
import multiprocessing
import queue

import gradio

import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro_ui(cfg):
    """
    """

    cfg['queue_to_ui']   = multiprocessing.Queue()  # coro --> ui
    cfg['queue_from_ui'] = multiprocessing.Queue()  # ui --> coro

    proc_ui = multiprocessing.Process(target = _proc_ui_main,
                                      args   = (cfg,),
                                      name   = 'workflow-ui',
                                      daemon = True)
    proc_ui.start()

    list_str_user_input = list()
    list_str_generated  = list()

    for idx in itertools.count():

        list_str_generated.clear()
        (list_str_generated) = yield (list_str_user_input)
        list_str_user_input.clear()

        if list_str_generated:
            for str_generated in list_str_generated:
                try:
                    cfg['queue_to_ui'].put(str_generated, block = False)
                except queue.Full as err:
                    pass

        while True:
            try:
                list_str_user_input.append(
                                    cfg['queue_from_ui'].get(block = False))
            except queue.Empty:
                break


# -----------------------------------------------------------------------------
def _proc_ui_main(cfg):
    """
    Service the request queue, forwarding requests to the UI.

    """

    polling_interval_secs = 0.5
    str_generated_output  = '(None)'

    # -------------------------------------------------------------------------
    def _on_click_btn_submit(txt_user_input):
        """
        Callback function for the submit button.

        Put inputs onto the queue.

        """
        try:
            str_user_input = txt_user_input
            cfg['queue_from_ui'].put(str_user_input, block = False)
        except queue.Full as err:
            pass
        return

    # -------------------------------------------------------------------------
    def _poll():
        """
        Callback function for the periodic timer.

        """
        nonlocal str_generated_output
        try:
            str_generated_output = cfg['queue_to_ui'].get(block = False)
        except queue.Empty:
            pass
        return str_generated_output

    # -------------------------------------------------------------------------
    with gradio.Blocks() as ui:
        with gradio.Row():
            with gradio.Column():

                txt_user_input = gradio.TextArea(
                                            interactive = True,
                                            label       = 'User input',
                                            lines       = 15)

                txt_generated_output = gradio.TextArea(
                                            interactive = False,
                                            label       = 'Generated output',
                                            lines       = 25)

                btn_submit = gradio.Button(value = 'Submit')
                btn_submit.click(fn     = _on_click_btn_submit,
                                 inputs = [txt_user_input])

        ui.load(
            fn      = _poll,
            outputs = [txt_generated_output],
            every   = polling_interval_secs)

    ui.queue(
        concurrency_count = 2,
        max_size          = 3)

    ui.launch(
        inbrowser           = True,
        share               = False,
        prevent_thread_lock = False)  # Blocks
