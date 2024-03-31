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


import asyncio
import logging
import pprint
import typing

import pydantic
import telegram


# =============================================================================
class State(pydantic.BaseModel):
    """
    Session track state.

    """

    version:             int        = 1
    id_session:          str        = ''
    type_chat:           str        = ''
    type_input:          str        = ''
    str_input:           str        = ''
    id_message_last:     str        = ''
    callback_query_last: typing.Any = None


# -----------------------------------------------------------------------------
class RuntimeDependencies(pydantic.BaseModel):
    """
    Runtime dependencies for dependency injection.

    """

    chat_message:         typing.Any = None
    chat_reply:           typing.Any = None
    chat_group_options:   typing.Any = None
    chat_private_options: typing.Any = None
    chat_query_edit_text: typing.Any = None
    session_create:       typing.Any = None
    session_join:         typing.Any = None
    session_update:       typing.Any = None
    session_summary:      typing.Any = None


# -----------------------------------------------------------------------------
async def coro(queue: asyncio.Queue, fcn: RuntimeDependencies):
    """
    Chat business logic coroutine.

    This asynchronous coroutine is responsible
    for defining the chat lifecycle from
    initiation through to conclusion.

    All dependencies are injected so that the
    chat logic can be tested in isolation.

    """

    await _display_greeting(queue, fcn)
    await _loop_forever(queue, fcn)


# -----------------------------------------------------------------------------
async def _display_greeting(queue, fcn):
    """
    Display greetings.

    """
    await fcn.chat_message('Hello world')


# -----------------------------------------------------------------------------
async def _loop_forever(queue, fcn):
    """
    Loop forever noop holding pattern.

    """
    while True:
        state = await queue.get()
        pprint.pprint(state)


# # -----------------------------------------------------------------------------
# async def _session_setup(queue, fcn):
#     """
#     Create or join session.

#     """

#     await fcn.chat_private_options(str_text     = str_text,
#                                    iter_str_opt = iter_str_opt)
#     while True:
#         state = await queue.get()
#         if state.type_input == 'callback_query':
#             str_opt = state.str_input
#             await fcn.chat_query_edit_text(
#                                     query    = state.callback_query_last,
#                                     str_text = f'Next question',
#                                     opt_inline = ['CHOICE C', 'CHOICE D'])
#             return str_opt
