# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot interaction context module."

description:
    "This module contains a class based context
    manager to help manage the life cycle of
    individual interactions with a Telegram bot
    implemented using the python-telegram-bot
    library."

id:
    "42e685b9-8891-42b2-859c-827ca283122e"

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
import http
import logging
import os
import pprint
import re
import typing
import urllib.parse

import pydantic
import requests
import sqlitedict
import telegram  # pylint: disable=wrong-import-order
import yaml

import t000_wtp.harmonica.telegram.bot     as tg_bot
import t000_wtp.harmonica.telegram.session as tg_session
import t000_wtp.harmonica.telegram.track   as tg_track
import t000_wtp.harmonica.util.log         as log_util


# =============================================================================
class Context():
    """
    Interaction context for a telegram bot.

    This context will be exited when the
    current interaction with the bot is
    complete.

    An interaction consists of zero or one
    inputs from the user and zero or more
    responses from the bot. In other words
    any action taken by or to the bot.

    """

    id_chat:            int
    id_track:           str
    bot:                tg_bot.Context
    update:             typing.Any
    context:            typing.Any
    state:              tg_track.State
    track_dependencies: tg_track.RuntimeDependencies

    # -------------------------------------------------------------------------
    def __init__(self,
                 bot:     tg_bot,
                 update:  typing.Any,
                 context: typing.Any):
        """
        Return an instance of BotInteractionContext.

        Gets called at the start of each interaction.

        """

        self.id_chat  = update.effective_chat.id
        self.id_track = f'tg.{self.id_chat}'

        try:
            self.state   = tg_track.State(**bot.db_track[self.id_track])
        except KeyError:
            self.state   = tg_track.State()
        finally:

            for (id_session, session) in bot.db_session.items():
                self.state.map_session[id_session] = session.str_name

            self.bot                = bot
            self.update             = update
            self.context            = context
            self.track_dependencies = tg_track.RuntimeDependencies(
                            chat_message         = self.chat_message,
                            chat_reply           = self.chat_reply,
                            chat_options         = self.chat_options,
                            chat_options_inline  = self.chat_options_inline,
                            chat_query_edit_text = self.chat_query_edit_text,
                            session_create       = self.session_create,
                            session_join         = self.session_join,
                            session_update       = self.session_update,
                            session_summary      = self.session_summary)

    # -------------------------------------------------------------------------
    def __enter__(self):
        """
        Enter the interaction context for the telegram bot.

        """

        return self

    # -------------------------------------------------------------------------
    def __exit__(self, type_exc, value_exc, tb_exc):
        """
        Exit the interaction context for the telegram bot.

        Make sure that relevant state is saved in the db.

        """

        _ensure_track_database_updated(
                            db_track = self.bot.db_track,
                            id_track = self.id_track,
                            state    = self.state.dict())

        _ensure_session_database_updated(
                            db_session   = self.bot.db_session,
                            id_session   = self.state.id_session,
                            name_session = self.state.name_session,
                            id_track     = self.id_track)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def handle_message(self):
        """
        Handle a new message from the user.

        """

        self.state.type_chat  = str(self.update.message.chat.type)
        self.state.type_input = 'message'
        self.state.str_input  = self.update.message.text
        await self._step()

    # -------------------------------------------------------------------------
    @log_util.trace
    async def handle_callback_query(self):
        """
        Handle a new callback query.

        """

        await self.update.callback_query.answer()
        self.state.type_input          = 'callback_query'
        self.state.str_input           = self.update.callback_query.data
        self.state.callback_query_last = self.update.callback_query
        await self._step()

    # -------------------------------------------------------------------------
    @log_util.trace
    async def handle_command(self):
        """
        Handle a new command.

        """

        self.state.type_chat  = str(self.update.message.chat.type)
        self.state.type_input = 'command'
        self.state.str_input  = self.update.message.text
        await self._step()

    # -------------------------------------------------------------------------
    @log_util.trace
    async def _step(self):
        """
        Single step the logic coroutine, creating it if necessary.

        """

        try:
            await self.bot.map_queue_track[self.id_track].put(self.state)
        except KeyError:
            logging.warning(
                ('Possible server restart? '
                 'Recreating sessions and tracks from saved state.'))
            self.bot.map_queue_track[self.id_track] = asyncio.Queue()
            self.bot.map_track[self.id_track]       = self.bot.app.create_task(
                tg_track.coro(queue = self.bot.map_queue_track[self.id_track],
                              fcn   = self.track_dependencies))
            await self.bot.map_queue_track[self.id_track].put(self.state)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def reset(self):
        """
        Reset the interaction state.

        """

        logging.info('Reset/restart chat.')
        self.state.type_chat  = str(self.update.message.chat.type)
        self.state.type_input = 'command'
        self.state.str_input  = self.update.message.text
        self.bot.map_queue_track[self.id_track] = asyncio.Queue()
        self.bot.map_track[self.id_track]       = self.bot.app.create_task(
            tg_track.coro(queue = self.bot.map_queue_track[self.id_track],
                          fcn   = self.track_dependencies))
        await self.bot.map_queue_track[self.id_track].put(self.state)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def chat_message(self, str_text, **kwargs):
        """
        Utility function to send a message to the user via telegram.

        """

        await self.context.bot.send_message(chat_id = self.id_chat,
                                            text    = str_text,
                                            **kwargs)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def chat_reply(self, str_text, **kwargs):
        """
        Utility function to send a reply message to the user via telegram.

        """

        await self.update.message.reply_text(text = str_text,
                                             **kwargs)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def chat_options(self, str_text, iter_str_opt, **kwargs):
        """
        Utility function to present options to the group via telegram.

        """

        keys   = [[telegram.KeyboardButton(opt) for opt in iter_str_opt]]
        markup = telegram.ReplyKeyboardMarkup(keys,
                                              resize_keyboard   = True,
                                              one_time_keyboard = True)

        await self.update.message.reply_text(text         = str_text,
                                             reply_markup = markup,
                                             **kwargs)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def chat_options_inline(self, str_text, iter_iter_opt, **kwargs):
        """
        Utility function to present options to the sender via telegram.

        """

        keys = []
        for iter_opt in iter_iter_opt:
            row = []
            for tup_opt in iter_opt:
                (text, callback_data) = tup_opt
                row.append(
                    telegram.InlineKeyboardButton(
                                            text          = text,
                                            callback_data = callback_data))
            keys.append(row)
        markup = telegram.InlineKeyboardMarkup(keys)

        await self.update.message.reply_text(text         = str_text,
                                             reply_markup = markup,
                                             **kwargs)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def chat_query_edit_text(
                                self,
                                query,
                                str_text,
                                iter_iter_opt = None,
                                **kwargs):
        """
        Utility function to edit message text from a telegram callback_query.

        """

        if iter_iter_opt is not None:
            keys = []
            for iter_opt in iter_iter_opt:
                row = []
                for opt in iter_opt:
                    (text, callback_data) = opt
                    row.append(
                        telegram.InlineKeyboardButton(
                                                text          = text,
                                                callback_data = callback_data))
                keys.append(row)
            markup = telegram.InlineKeyboardMarkup(keys)
        else:
            markup = None

        await query.edit_message_text(text         = str_text,
                                      reply_markup = markup)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def session_create(self, name_session):
        """
        Utility function to ensure a new session exists.

        """

        # id_session is name_session in lowercase
        # with any sequence of non-alphanumeric
        # characters replaced with a single
        # underscore
        #
        id_session = re.sub('[^a-zA-Z0-9]+', '_', name_session.lower())
        self.state.id_session = id_session
        self.state.map_session[id_session] = name_session
        self.bot.db_session[id_session]    = tg_session.State(
                                                    str_name  = name_session)
        self.bot.db_session.commit()
        return id_session

    # -------------------------------------------------------------------------
    async def session_join(self, id_session, id_track):
        """
        Utility function to add a track to an existing session.

        """

        print('>>> SESSION JOIN')

    # -------------------------------------------------------------------------
    async def session_update(self, id_session, id_track, transcript_track):
        """
        Utility function to add an update to an existing session.

        """

        print('>>> SESSION UPDATE')

    # -------------------------------------------------------------------------
    async def session_summary(self, id_session, id_track, transcript_track):
        """
        Utility function to get a summary from a session.

        """

        print('>>> SESSION SUMMARY')

        return ''


# -----------------------------------------------------------------------------
def _ensure_track_database_updated(db_track: sqlitedict.SqliteDict,
                                   id_track: str,
                                   state:    dict) -> None:
    """
    Update session database.

    """

    db_track[id_track] = state
    db_track.commit()


# -----------------------------------------------------------------------------
def _ensure_session_database_updated(db_session:   sqlitedict.SqliteDict,
                                     id_session:   str,
                                     name_session: str,
                                     id_track:     str) -> None:
    """
    Update session database.

    """

    is_dirty = False
    try:
        session = db_session[id_session]
    except KeyError:
        session = tg_session.State()
        is_dirty = True

    if session.str_name != name_session:
        session.str_name = name_session
        is_dirty = True

    if id_track not in session.set_track:
        session.set_track.add(id_track)
        is_dirty = True

    if is_dirty:
        db_session[id_session] = session
        db_session.commit()
