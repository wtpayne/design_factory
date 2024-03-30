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

import t000_wtp.harmonica.telegram.interaction   as tg_interaction
import t000_wtp.harmonica.telegram.configuration as tg_config
import t000_wtp.harmonica.util.log               as log_util

NAME_APP     = 'Harmonica'
NAME_PACKAGE = f't000_wtp.{NAME_APP.lower()}'
try:
    __version__ = importlib.metadata.version(NAME_PACKAGE)
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


# -----------------------------------------------------------------------------
def main():
    """
    Set up command and message handlers and run the telegram bot main loop.

    """

    log_util.setup()
    token = _token_telegram()
    with tg_config.Context(token) as cfg:
        cfg.add_command_handler(_start)
        cfg.add_command_handler(_join)
        cfg.add_command_handler(_help)
        cfg.add_command_handler(_about)
        cfg.add_message_handler(_msg)


# -----------------------------------------------------------------------------
def _token_telegram():
    """
    Return the telegram API token in the environment.

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
async def _start(cfg:     tg_config.Context,
                 update:  telegram.Update,
                 context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Start a new session.

    """

    with tg_interaction.Context(cfg     = cfg,
                                update  = update,
                                context = context) as interaction:

        await interaction.reset()


# -----------------------------------------------------------------------------
@log_util.trace
async def _join(cfg:     tg_config.Context,
                update:  telegram.Update,
                context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Join an existing session.

    """

    with tg_interaction.Context(cfg     = cfg,
                                update  = update,
                                context = context) as interaction:

        await interaction.step()


# -----------------------------------------------------------------------------
@log_util.trace
async def _help(cfg:     tg_config.Context,
                update:  telegram.Update,
                context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print a list of commands.

    """

    with tg_interaction.Context(cfg     = cfg,
                                update  = update,
                                context = context) as interaction:

        await interaction.chat_msg(cfg.help_text())


# -----------------------------------------------------------------------------
@log_util.trace
async def _about(cfg:     tg_config.Context,
                 update:  telegram.Update,
                 context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print information about the bot.

    """

    with tg_interaction.Context(cfg     = cfg,
                                update  = update,
                                context = context) as interaction:

        await interaction.chat_msg(f'{NAME_APP} bot version {__version__}')


# -----------------------------------------------------------------------------
@log_util.trace
async def _msg(cfg:     tg_config.Context,
               update:  telegram.Update,
               context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for non-command messages.

    """

    with tg_interaction.Context(cfg     = cfg,
                                update  = update,
                                context = context) as interaction:

        await interaction.step()


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
