# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot script."

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


import importlib.metadata
import os
import os.path
import sys

import dotenv
import telegram
import telegram.ext  # pylint: disable=import-error,no-name-in-module

import t000_wtp.tgbot.interaction as tgbot_interaction
import t000_wtp.tgbot.logutil     as tgbot_logutil
import t000_wtp.tgbot.runtime     as tgbot_runtime


NAME_PACKAGE = 't000_wtp.tgbot'
try:
    __version__ = importlib.metadata.version(NAME_PACKAGE)
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


KEY_TOKEN         = 'TOKEN_TELEGRAM_PAIDEIA_ROBOT'
STR_TOPIC_ZUZALU  = ('What software principles should we follow for Zuzalu '
                     'technologies? Should anything be added? What should be '
                     'done first? What are the highest priorities?')
STR_TOPIC_VITALEA = ('Ask a controversial and creative question about '
                     'longevity that is not about ethics.')


# -----------------------------------------------------------------------------
def main():
    """
    Set up command and message handlers and run the telegram bot main loop.

    """

    dotenv.load_dotenv()
    with tgbot_runtime.Context(os.getenv(KEY_TOKEN)) as bot:
        bot.handle_command(_start)
        bot.handle_command(_help)
        bot.handle_command(_about)
        bot.handle_messages(_msg)


# -----------------------------------------------------------------------------
@tgbot_logutil.trace
async def _start(
            bot:     tgbot_runtime.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Welcome the user to the Paideia copilot.

    Called at the beginning of an interaction with the bot.

    """

    with tgbot_interaction.Context(bot     = bot,
                                   update  = update,
                                   context = context) as interaction:

        await interaction.reset()


# -----------------------------------------------------------------------------
@tgbot_logutil.trace
async def _help(
            bot:     tgbot_runtime.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print a list of commands.

    """

    with tgbot_interaction.Context(bot     = bot,
                                   update  = update,
                                   context = context) as interaction:

        await interaction.telegram_msg(bot.help_text())


# -----------------------------------------------------------------------------
@tgbot_logutil.trace
async def _about(
            bot:     tgbot_runtime.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print information about the bot.

    """

    with tgbot_interaction.Context(bot     = bot,
                                   update  = update,
                                   context = context) as interaction:

        await interaction.telegram_msg(f'Paideia bot version {__version__}')


# -----------------------------------------------------------------------------
@tgbot_logutil.trace
async def _msg(
            bot:     tgbot_runtime.Context,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for non-command messages.

    """

    with tgbot_interaction.Context(bot     = bot,
                                   update  = update,
                                   context = context) as interaction:

        await interaction.step()


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
