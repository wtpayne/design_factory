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

import t000_wtp.harmonica.telegram.logutil
import t000_wtp.harmonica.telegram.runtime
import t000_wtp.harmonica.logic


# =============================================================================
class InteractionState(pydantic.BaseModel):
    """
    Bot interaction state.

    """

    version:          int  = 1
    id_conversation:  str  = ''
    id_message_last:  str  = ''
    str_message_last: str  = ''
    str_topic:        str  = ''


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

    id_chat: int
    bot:     t000_wtp.harmonica.telegram.runtime.Context
    update:  typing.Any
    context: typing.Any
    state:   InteractionState

    # -------------------------------------------------------------------------
    def __init__(self,
                 bot:     t000_wtp.harmonica.telegram.runtime.Context,
                 update:  typing.Any,
                 context: typing.Any):
        """
        Return an instance of BotInteractionContext.

        Gets called at the start of each interaction.

        """

        self.id_chat = update.effective_chat.id

        try:
            self.state   = InteractionState(**bot.db[self.id_chat])
        except KeyError:
            self.state   = InteractionState()
        finally:
            self.bot     = bot
            self.update  = update
            self.context = context

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

        self.bot.db[self.id_chat] = self.state.dict()
        self.bot.db.commit()

    # -------------------------------------------------------------------------
    @t000_wtp.harmonica.telegram.logutil.trace
    async def reset(self, str_topic = ''):
        """
        Reset the interaction state.

        """

        logging.info('Reset/restart chat.')
        self.state.str_topic             = str_topic
        self.state.str_message_last      = ''
        self.bot.map_queue[self.id_chat] = asyncio.Queue()
        self.bot.map_chat[self.id_chat]  = asyncio.create_task(
            tgbot_logic.coro(
                    queue              = self.bot.map_queue[self.id_chat],
                    fcn_chat_msg       = self.telegram_msg,
                    fcn_chat_reply     = self.telegram_reply,
                    fcn_chat_options   = self.telegram_options,
                    fcn_session_create = self._new_conv,
                    fcn_session_update = self._reply))
        await self.bot.map_queue[self.id_chat].put(self.state)

    # -------------------------------------------------------------------------
    @t000_wtp.harmonica.telegram.logutil.trace
    async def step(self):
        """
        Single step the logic coroutine, creating it if necessary.

        """

        self.state.str_message_last = self.update.message.text
        try:
            await self.bot.map_queue[self.id_chat].put(self.state)
        except KeyError:
            logging.warning(
                ('Possible server restart? '
                 'Recreating chat coroutine from saved state.'))
            self.bot.map_queue[self.id_chat] = asyncio.Queue()
            self.bot.map_chat[self.id_chat]  = asyncio.create_task(
                tgbot_logic.coro(
                        queue              = self.bot.map_queue[self.id_chat],
                        fcn_chat_msg       = self.telegram_msg,
                        fcn_chat_reply     = self.telegram_reply,
                        fcn_chat_options   = self.telegram_options,
                        fcn_session_create = self._new_conv,
                        fcn_session_update = self._reply))
            await self.bot.map_queue[self.id_chat].put(self.state)

    # -------------------------------------------------------------------------
    @t000_wtp.harmonica.telegram.logutil.trace
    async def telegram_msg(self, str_text, **kwargs):
        """
        Utility function to send a message to the user via telegram.

        """

        await self.context.bot.send_message(chat_id = self.id_chat,
                                            text    = str_text,
                                            **kwargs)

    # -------------------------------------------------------------------------
    @t000_wtp.harmonica.telegram.logutil.trace
    async def telegram_reply(self, str_text, **kwargs):
        """
        Utility function to send a reply message to the user via telegram.

        """

        await self.update.message.reply_text(text = str_text,
                                             **kwargs)

    # -------------------------------------------------------------------------
    @t000_wtp.harmonica.telegram.logutil.trace
    async def telegram_options(self, str_text, iter_str_opt, **kwargs):
        """
        Utility function to present options to the user via telegram.

        """

        keyboard = [[telegram.KeyboardButton(opt) for opt in iter_str_opt]]
        markup   = telegram.ReplyKeyboardMarkup(keyboard,
                                                resize_keyboard   = True,
                                                one_time_keyboard = True)
        await self.update.message.reply_text(text         = str_text,
                                             reply_markup = markup,
                                             **kwargs)

    # -------------------------------------------------------------------------
    async def _new_conv(self, topic):
        """
        Utility function to create a new conversation on the chatserver.

        """

        pass

    # -------------------------------------------------------------------------
    async def _reply(self, reply):
        """
        Utility function to add a reply to a conversation on the chatserver.

        """

        pass