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
import typing
import urllib.parse

import pydantic
import requests
import telegram  # pylint: disable=wrong-import-order
import yaml

import t000_wtp.harmonica.session                as session
import t000_wtp.harmonica.track                  as track
import t000_wtp.harmonica.telegram.configuration as tg_config
import t000_wtp.harmonica.util.log               as log_util


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
    cfg:                tg_config
    update:             typing.Any
    context:            typing.Any
    state:              track.State
    track_dependencies: track.RuntimeDependencies

    # -------------------------------------------------------------------------
    def __init__(self,
                 cfg:     tg_config,
                 update:  typing.Any,
                 context: typing.Any):
        """
        Return an instance of BotInteractionContext.

        Gets called at the start of each interaction.

        """

        self.id_chat = update.effective_chat.id

        try:
            self.state   = track.State(**cfg.db_track[self.id_chat])
        except KeyError:
            self.state   = track.State()
        finally:
            self.cfg     = cfg
            self.update  = update
            self.context = context
            self.track_dependencies = track.RuntimeDependencies(
                chat_message         = self.chat_message,
                chat_reply           = self.chat_reply,
                chat_group_options   = self.chat_group_options,
                chat_private_options = self.chat_private_options,
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

        self.cfg.db_track[self.id_chat] = self.state.dict()
        self.cfg.db_track.commit()

    # -------------------------------------------------------------------------
    @log_util.trace
    async def reset(self, str_topic = ''):
        """
        Reset the interaction state.

        """

        logging.info('Reset/restart chat.')
        self.state.str_topic                   = str_topic
        self.state.str_message_last            = ''
        self.cfg.map_queue_track[self.id_chat] = asyncio.Queue()
        self.cfg.map_track[self.id_chat]       = self.cfg.app.create_task(
            track.coro(
                queue        = self.cfg.map_queue_track[self.id_chat],
                dependencies = self.track_dependencies))
        await self.cfg.map_queue_track[self.id_chat].put(self.state)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def _step_impl(self):
        """
        Single step the logic coroutine, creating it if necessary.

        """

        try:
            await self.cfg.map_queue_track[self.id_chat].put(self.state)
        except KeyError:
            logging.warning(
                ('Possible server restart? '
                 'Recreating sessions and tracks from saved state.'))
            self.cfg.map_queue_track[self.id_chat] = asyncio.Queue()
            self.cfg.map_track[self.id_chat]       = self.cfg.app.create_task(
                track.coro(
                    queue        = self.cfg.map_queue_track[self.id_chat],
                    dependencies = self.track_dependencies))
            await self.cfg.map_queue_track[self.id_chat].put(self.state)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def step(self):
        """
        Single step the logic coroutine, creating it if necessary.

        """

        self.state.str_message_last = self.update.message.text
        await self._step_impl()

    # -------------------------------------------------------------------------
    @log_util.trace
    async def handle_callback_query(self):
        """
        Handle a callback query.

        """

        self.update.callback_query.answer()
        await self._step_impl()

    # -------------------------------------------------------------------------
    @log_util.trace
    async def chat_edit_query(self, str_text, **kwargs):
        """
        Utility function to edit a query via telegram.

        """

        query = self.update.callback_query
        await query.edit_message_text(text=f"Selected option: {query.data}")


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
    async def chat_group_options(self, str_text, iter_str_opt, **kwargs):
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
    async def chat_private_options(self, str_text, iter_str_opt, **kwargs):
        """
        Utility function to present options to the sender via telegram.

        """

        keys = [[
            telegram.InlineKeyboardButton(opt, callback_data = opt)
                                                    for opt in iter_str_opt]]

        markup = telegram.InlineKeyboardMarkup(keys)

        await self.update.message.reply_text(text         = str_text,
                                             reply_markup = markup,
                                             **kwargs)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def session_create(self):
        """
        Utility function to ensure a new session exists.

        """

        print('>>> SESSION CREATE')

        return 0

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
