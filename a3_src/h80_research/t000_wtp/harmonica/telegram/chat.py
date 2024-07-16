# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot chat adapter module."

description:
    "This module provides functions for
    interacting with telegram chat using
    an interface that is common with other
    chat apps like Discord or Slack or WhatsApp."

id:
    "9b419e6f-dfc4-40e1-9165-296364c763b2"

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


import typing

import t000_wtp.harmonica.util.log          as log_util


# =============================================================================
class Adapter():
    """
    Chat adapter for Telegram bots.

    """

    update:  typing.Any
    context: typing.Any

    # -------------------------------------------------------------------------
    def __init__(self, tg_update = None, tg_context = None):
        """
        Ctor.

        """

        self.update  = tg_update
        self.context = tg_context

    # -------------------------------------------------------------------------
    @log_util.trace
    async def message(self, str_text, **kwargs):
        """
        Send a message to the user via telegram.

        """

        await self.context.bot.send_message(
                                    chat_id = self.update.effective_chat.id,
                                    text    = str_text,
                                    **kwargs)

    # -------------------------------------------------------------------------
    @log_util.trace
    async def reply(self, str_text, **kwargs):
        """
        Send a reply message to the user via telegram.

        """

        if self.update.message is not None:
            await self.update.message.reply_text(text = str_text,
                                                 **kwargs)
        else:
            await self.context.bot.send_message(
                                        chat_id = self.update.effective_chat.id,
                                        text    = str_text,
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

