# -*- coding: utf-8 -*-
"""
---

title:
    "Track logic module."

description:
    "This module contains track logic for
    the harmonica bot."

id:
    "44950a35-70dc-4519-82a0-a4e63a80ba0a"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2024 William Payne"

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


import logging
import typing

import pydantic


# =============================================================================
class State(pydantic.BaseModel):
    """
    Session track state.

    """

    version:          int  = 1
    id_conversation:  str  = ''
    id_message_last:  str  = ''
    str_message_last: str  = ''
    str_topic:        str  = ''


# -----------------------------------------------------------------------------
class RuntimeDependencies(pydantic.BaseModel):
    """
    Runtime dependencies for dependency injection.

    """

    chat_message:         typing.Any = None
    chat_reply:           typing.Any = None
    chat_group_options:   typing.Any = None
    chat_private_options: typing.Any = None
    session_create:       typing.Any = None
    session_join:         typing.Any = None
    session_update:       typing.Any = None
    session_summary:      typing.Any = None


# -----------------------------------------------------------------------------
async def coro(queue,
               dependencies: RuntimeDependencies):
    """
    Chat business logic coroutine.

    This asynchronous coroutine is responsible
    for defining the chat lifecycle from
    initiation through to conclusion.

    All dependencies are injected so that the
    chat logic can be tested in isolation.

    """


    while True:

        await dependencies.chat_private_options(
                        str_text     = 'Please choose:',
                        iter_str_opt = ['CHOICE A', 'CHOICE B'])

        state = await queue.get()

        await dependencies.chat_message('FOO')

    # while state.str_topic == '':

    #     # Termination criterion. We have found the
    #     # topic of conversation so we can move on.
    #     #
    #     if isinstance(cursor, str):
    #         state.str_topic = cursor
    #         break

    #     # Sanity checking.
    #     #
    #     if not isinstance(cursor, dict):
    #         str_err = 'Bad configuration (Expected a nested dict)'
    #         fcn_send_message(str_err)
    #         logging.error(str_err)
    #         raise RuntimeError(str_err)
    #     if '_txt' not in cursor:
    #         str_err = 'Bad configuration (Expected a _txt field)'
    #         fcn_send_message(str_err)
    #         logging.error(str_err)
    #         raise RuntimeError(str_err)

    #     # Present the next set of options to the
    #     # user.
    #     #
    #     set_str_opt  = set(cursor.keys()) - {'_txt'}
    #     list_str_opt = sorted(set_str_opt)
    #     await fcn_chat_options(str_text     = cursor['_txt'],
    #                            iter_str_opt = list_str_opt)
    #     state     = await queue.get()
    #     selection = state.str_message_last

    #     # Sanity checking.
    #     #
    #     if selection not in set_str_opt:
    #         await fcn_send_reply('Selection not recognized.')
    #         continue

    #     # Descend to the next level of the tree.
    #     #
    #     cursor = cursor[selection]
    #     continue

    # question = await fcn_session_ensure(state.str_topic)
    # await fcn_send_reply(question)

    # Carry out the conversation.
    #
    while True:

        state   = await queue.get()
        # message = await fcn_session_update(state.str_message_last)

        import pprint
        pprint.pprint(state.dict())

        # if message:
        #     print('--- ' + message)
        #     await fcn_send_reply(message)

