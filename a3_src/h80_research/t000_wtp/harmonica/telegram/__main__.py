# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot entry point script."

description:
    "This script contains functionality for
    configuring and running a Telegram bot
    using the python-telegram-bot library."

id:
    "3544902d-6575-424b-b53c-80fa215dea69"

type:
    dt001_python_script

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
import os
import os.path
import sys
import time

import dotenv
import telegram
import telegram.ext  # pylint: disable=import-error,no-name-in-module

import t000_wtp.harmonica                      as harmonica
import t000_wtp.harmonica.telegram.bot         as tg_bot
import t000_wtp.harmonica.telegram.interaction as tg_interaction
import t000_wtp.harmonica.util.log             as log_util


# -----------------------------------------------------------------------------
def main():
    """
    Set up command and message handlers and run the telegram bot main loop.

    """

    log_util.setup()
    with tg_bot.Context(_token_telegram()) as bot_context:
        bot_context.add_message_handler(_msg)
        bot_context.add_callback_query_handler(_callback_query)
        bot_context.add_command_handler(_start)
        bot_context.add_command_handler(_join)
        bot_context.add_command_handler(_help)
        bot_context.add_command_handler(_about)


# -----------------------------------------------------------------------------
def _token_telegram():
    """
    Return the telegram API token.

    This is obtained from environment variables.

    """

    dotenv.load_dotenv()
    stage_deployment  = os.getenv(f'HARMONICA_STAGE_DEPLOYMENT',
                                  default = 'DEV')
    map_key_token_api = { 'DEV': f'HARMONICA_TOKEN_TELEGRAM_DEV',
                          'UAT': f'HARMONICA_TOKEN_TELEGRAM_UAT',
                          'PRD': f'HARMONICA_TOKEN_TELEGRAM_PRD' }
    key_token_api     = map_key_token_api[stage_deployment]
    token_api         = os.getenv(key_token_api)

    return token_api


# -----------------------------------------------------------------------------
@log_util.trace
async def _msg(
            bot:     tg_bot.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for non-command messages.

    """

    with tg_interaction.Context(bot     = bot,
                                update  = update,
                                context = context) as interaction_context:
        await interaction_context.handle_message()


# -----------------------------------------------------------------------------
@log_util.trace
async def _callback_query(
            bot:     tg_bot.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Generic callback query handler.

    """

    with tg_interaction.Context(bot     = bot,
                                update  = update,
                                context = context) as interaction_context:
        await interaction_context.handle_callback_query()


# -----------------------------------------------------------------------------
@log_util.trace
async def _start(
            bot:     tg_bot.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Start a new session.

    """

    with tg_interaction.Context(bot     = bot,
                                update  = update,
                                context = context) as interaction_context:
        await interaction_context.reset()


# -----------------------------------------------------------------------------
@log_util.trace
async def _join(
            bot:     tg_bot.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Join an existing session.

    """

    with tg_interaction.Context(bot     = bot,
                                update  = update,
                                context = context) as interaction_context:
        await interaction_context.handle_command()


# -----------------------------------------------------------------------------
@log_util.trace
async def _help(
            bot:     tg_bot.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print a list of commands.

    """

    with tg_interaction.Context(bot     = bot,
                                update  = update,
                                context = context) as interaction_context:
        await interaction_context.chat_message(str_text = bot.help_text())


# -----------------------------------------------------------------------------
@log_util.trace
async def _about(
            bot:     tg_bot.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print information about the bot.

    """

    with tg_interaction.Context(bot     = bot,
                                update  = update,
                                context = context) as interaction_context:
        str_name    = f'{harmonica.name_app}'
        str_version = f'{harmonica.__version__}'
        str_about   = f'{str_name} bot version {str_version}'
        await interaction_context.chat_message(str_text = str_about)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
