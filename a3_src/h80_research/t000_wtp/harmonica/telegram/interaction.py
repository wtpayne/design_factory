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
import telegram  # pylint: disable=wrong-import-order
import yaml

import t000_wtp.harmonica.logic.track   as track
import t000_wtp.harmonica.telegram.bot  as tg_bot
import t000_wtp.harmonica.telegram.chat as tg_chat
import t000_wtp.harmonica.util.log      as log_util


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

    chat:   tg_chat.Adapter
    _track: track.Track

    # -------------------------------------------------------------------------
    def __init__(self,
                 bot:     tg_bot.Context,
                 update:  typing.Any,
                 context: typing.Any):
        """
        Return an instance of BotInteractionContext.

        Gets called at the start of each interaction.

        """

        self.chat   = tg_chat.Adapter(
                                tg_update  = update,
                                tg_context = context)
        self._track = bot.track_table.load(
                                update  = update,
                                context = context)

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

        self._track.commit()

    # -------------------------------------------------------------------------
    @log_util.trace
    async def handle_message(self):
        """
        Handle a new message from the user.

        """

        pass

        # self._track.update(
        #     type_chat  = str(self.update.message.chat.type),
        #     type_input = 'message',
        #     str_input  = self.update.message.text)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def handle_callback_query(self):
        """
        Handle a new callback query.

        """

        pass

        # await self.update.callback_query.answer()
        # self._track.update(
        #     type_input          = 'callback_query',
        #     str_input           = self.update.callback_query.data,
        #     callback_query_last = self.update.callback_query)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def handle_command(self, command = None):
        """
        Handle a new command.

        """

        pass

        # self._track.update(
        #     type_chat  = str(self.update.message.chat.type),
        #     type_input = 'command',
        #     str_input  = self.update.message.text)
