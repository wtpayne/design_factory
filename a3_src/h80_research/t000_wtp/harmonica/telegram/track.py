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
import collections
import logging
import pprint
import typing

import pydantic
import telegram

import t000_wtp.harmonica as harmonica


# =============================================================================
class State(pydantic.BaseModel):
    """
    Session track state.

    """

    version:              int        = 1
    id_session:           str        = 'default_session'
    name_session:         str        = 'Default Session'
    map_session:          dict       = dict()   # id_session -> name_session
    type_chat:            str        = ''
    type_input:           str        = ''
    str_input:            str        = ''
    id_message_last:      str        = ''
    callback_query_last:  typing.Any = None


# -----------------------------------------------------------------------------
class RuntimeDependencies(pydantic.BaseModel):
    """
    Runtime dependencies for dependency injection.

    """

    chat_message:         typing.Any = None
    chat_reply:           typing.Any = None
    chat_options:         typing.Any = None
    chat_options_inline:  typing.Any = None
    chat_query_edit_text: typing.Any = None
    session_create:       typing.Any = None
    session_join:         typing.Any = None
    session_update:       typing.Any = None
    session_summary:      typing.Any = None


# -----------------------------------------------------------------------------
async def coro(queue: asyncio.Queue, fcn: RuntimeDependencies):
    """
    Session track coroutine.

    This asynchronous coroutine is responsible
    for defining the track lifecycle from
    initiation through to termination.

    Two inputs are provided. The first is the
    asyncio queue that is used to recieve state
    updates from the rest of the system and
    the second is a set of runtime dependencies
    used for dependency injection, allowing this
    track logic to be tested in isolation.


    """

    map_transcript = collections.defaultdict(list)

    while True:

        state = await queue.get()

        is_command        = state.type_input == 'command'
        is_callback_query = state.type_input == 'callback_query'
        is_message        = state.type_input == 'message'
        is_private        = state.type_chat  == 'private'

        if is_message and is_private:
            map_transcript[state.id_session].append(state.str_input)
            continue

        if is_command and state.str_input.startswith('/start'):
            maybe_id_session = await _handle_start(queue, fcn, state)
        if is_command and state.str_input.startswith('/join'):
            maybe_id_session = await _handle_join(queue, fcn, state)
        if is_callback_query:
            maybe_id_session = await _handle_callback_query(queue, fcn, state)
        if maybe_id_session is not None:
            id_session = maybe_id_session


# ----------------------------------------------------------------------------
async def _handle_start(queue: asyncio.Queue,
                        fcn:   RuntimeDependencies,
                        state: State):
    """
    Return id_session after a /start command.

    """

    try:
        (str_cmd, str_param) = state.str_input.split(maxsplit = 1)
    except ValueError:
        await fcn.chat_reply('Please choose a name for your session:')
        state        = await queue.get()
        name_session = state.str_input
    else:
        name_session = str_param

    id_session = await fcn.session_create(name_session)
    await fcn.chat_reply(f'Started session: "{name_session}"')
    return id_session


# -----------------------------------------------------------------------------
async def _handle_join(queue: asyncio.Queue,
                       fcn:   RuntimeDependencies,
                       state: State):
    """
    Return id_session or None after a /join command.

    """

    try:
        (str_cmd, str_param) = state.str_input.split(maxsplit = 1)
    except ValueError:
        await fcn.chat_options_inline(
                                'Which session do you want to join?',
                                _opt_id_session(state.map_session, '/join'))
        return None

    assert state.type_input == 'command'
    assert str_cmd          == '/join'

    for (id_session, name_session) in state.map_session.items():

        if str_param == name_session:
            await fcn.chat_reply(f'User joined session: "{name_session}"')
            return id_session

    await fcn.chat_options_inline(
                            ('Invalid session.\n'
                             'Which session do you want to join?'),
                            _opt_id_session(state.map_session, '/join'))
    return None


# -----------------------------------------------------------------------------
async def _handle_callback_query(queue: asyncio.Queue,
                                 fcn:   RuntimeDependencies,
                                 state: State):
    """
    Return id_session or None after a /join command.

    """

    (str_cmd, id_session) = state.str_input.split(maxsplit = 1)
    name_session = state.map_session[id_session]
    await fcn.chat_reply(f'User joined session: "{name_session}"')
    assert state.type_input == 'callback_query'
    assert str_cmd          == '/join'
    assert id_session in state.map_session
    return id_session


# -----------------------------------------------------------------------------
def _opt_id_session(map_session: dict,
                    str_cmd:     str):
    """
    Return options to configure a keyboard that lets the user select a session.

    """

    return [[(name_session, ' '.join((str_cmd, id_session)))]
                                            for (id_session, name_session)
                                                in sorted(map_session.items())]
