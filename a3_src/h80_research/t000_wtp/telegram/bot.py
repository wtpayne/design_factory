# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot module."

description:
    "This module contains functions to run
    a telegram bot."

id:
    "3544902d-6575-424b-b53c-80fa215dea69"

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
import contextlib
import enum
import functools
import http
import importlib.metadata
import itertools
import logging
import os
import os.path
import typing
import urllib.parse

import aiochannel
import requests
import dill
import pydantic
import sqlitedict
import telegram
import telegram.ext

import key


try:
    __version__ = importlib.metadata.version('paideia.telegram')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'

URL_CHATSERVER = 'https://chatserver.paideia.ai'
UUID_BEARER    = 'C6046DB3-18B4-44AA-A876-96B303378D3F'
KEY_TOKEN      = 'TOKEN_TELEGRAM_PAIDEIA_ROBOT'


# -----------------------------------------------------------------------------
def main():
    """
    Set up command and message handlers and run the telegram bot main loop.

    """

    str_token = key.load(id_value = KEY_TOKEN)

    with _bot_context(str_token) as bot:

        bot.command(_start)
        bot.command(_zuzalu)
        bot.command(_vitalia)
        bot.command(_help)
        bot.command(_about)
        bot.command(_resume)
        bot.message(_msg)


# -----------------------------------------------------------------------------
async def _start(
            bot:     typing.Any,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for the start command.

    """

    str_topic = 'Ask the question about the pros and cons of capitalism.'

    with _action(bot     = bot,
                 id_chat = update.effective_chat.id,
                 update  = update,
                 context = context) as action:

        response = await action.new(topic = str_topic)
        await action.telegram(response)


# -----------------------------------------------------------------------------
async def _zuzalu(
            bot:     typing.Any,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for the zuzalu command.

    """

    with _action(bot     = bot,
                 id_chat = update.effective_chat.id,
                 update  = update,
                 context = context) as action:
        print('ZUZALU')



# -----------------------------------------------------------------------------
async def _vitalia(
            bot:     typing.Any,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for the vitalia command.

    """

    with _action(bot     = bot,
                 id_chat = update.effective_chat.id,
                 update  = update,
                 context = context) as action:
        print('VITALIA')



# -----------------------------------------------------------------------------
async def _help(
            bot:     typing.Any,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for the help command.

    """

    with _action(bot     = bot,
                 id_chat = update.effective_chat.id,
                 update  = update,
                 context = context) as action:

        await session.telegram('HELP')


# -----------------------------------------------------------------------------
async def _about(
            bot:     typing.Any,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for the about command.

    """

    with _action(bot     = bot,
                 id_chat = update.effective_chat.id,
                 update  = update,
                 context = context) as action:

        await session.telegram(f'Paideia bot version {__version__}')


# -----------------------------------------------------------------------------
async def _resume(
            bot:     typing.Any,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for the resume command.

    """

    with _action(bot     = bot,
                 id_chat = update.effective_chat.id,
                 update  = update,
                 context = context) as action:
        print('RESUME')



# -----------------------------------------------------------------------------
async def _msg(
            bot:     typing.Any,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for non-command messages.

    """

    with _action(bot     = bot,
                 id_chat = update.effective_chat.id,
                 update  = update,
                 context = context) as action:
        print('MSG')


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _bot_context(str_token):
    """
    Return a runtime context for the telegram bot.

    Ensures transactions are committed and
    the database is closed on program
    termination.

    Also provides convenience functions for
    adding command handlers and message
    handlers.

    Automatically runs the main event loop
    once the bot has been configured.

    """

    str_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format = str_format,
                        level  = logging.INFO)

    app_builder  = telegram.ext.ApplicationBuilder().token(str_token)
    app          = app_builder.build()
    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    filename_db  = 'bot.db'
    filepath_db  = os.path.join(dirpath_self, filename_db)
    db           = sqlitedict.SqliteDict(filepath_db,
                                         encode = dill.dumps,
                                         decode = dill.loads)
    bot          = BotContext(app = app,
                              db  = db)

    try:
        yield bot
    except:
        db.close()
        raise
    else:
        try:
            bot.run()
        finally:
            db.commit()
            db.close()
            db = None


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _action(bot, id_chat, update, context):
    """
    Return an action context for a command or message handler.

    Ensures state is loaded/saved from disk as
    needed.

    """

    try:
        session         = SessionState(**bot.db[id_chat])
        session.update  = update
        session.context = context
    except KeyError:
        session = SessionState(id_chat  = id_chat,
                               id_state = StateEnum.DEFAULT,
                               update   = update,
                               context  = context)

    try:
        yield session
    finally:
        session.update  = None
        session.context = None
        bot.db[id_chat]     = session.dict()
        bot.db.commit()


# =============================================================================
class BotContext(pydantic.BaseModel):
    """
    Runtime context for the telegram bot.

    """

    # =========================================================================
    class Config:
        arbitrary_types_allowed = True

    app: telegram.ext._application.Application
    db:  sqlitedict.SqliteDict

    # -------------------------------------------------------------------------
    def command(self, fcn_callback):
        """
        Add a new command handler to the bot.

        """

        str_command = fcn_callback.__name__
        if str_command.startswith('_'):
            str_command = str_command[1:]

        self.app.add_handler(
            telegram.ext.CommandHandler(
                        command  = str_command,
                        callback = functools.partial(fcn_callback, self)))

    # -------------------------------------------------------------------------
    def message(self, fcn_callback):
        """
        Add a new message handler to the bot.

        """

        filter_txt        = telegram.ext.filters.TEXT
        filter_cmd        = telegram.ext.filters.COMMAND
        select_if_not_cmd = filter_txt & ~filter_cmd

        self.app.add_handler(
            telegram.ext.MessageHandler(
                        filters  = select_if_not_cmd,
                        callback = functools.partial(fcn_callback, self)))

    # -------------------------------------------------------------------------
    def run(self):
        """
        Run the main loop for the bot.

        """

        self.app.run_polling()


# =============================================================================
class StateEnum(enum.IntEnum):
    """
    """
    DEFAULT = 0
    ZUZALU  = 1
    VITALIA = 2
    HELP    = 3
    ABOUT   = 4
    RESUME  = 5


# =============================================================================
class SessionState(pydantic.BaseModel):
    """
    Session state.

    """

    # =========================================================================
    class Config:
        arbitrary_types_allowed = True

    id_chat:         int
    id_state:        StateEnum
    update:          typing.Any
    context:         typing.Any
    id_conversation: str = ''
    id_message_last: str = ''

    # -------------------------------------------------------------------------
    async def new(self, topic):
        """
        Create a new conversation on the chatserver.

        """

        response = requests.post(
                    url     = urllib.parse.urljoin(URL_CHATSERVER, 'new'),
                    json    = { 'name':          'dfs_v1',
                                'request':       { 'topic': topic }},
                    headers = { 'accept':        'application/json',
                                'Content-Type':  'application/json',
                                'Authorization': f'Bearer {UUID_BEARER}'})
        is_ok = response.status_code == HTTPStatus.OK
        if is_ok:
            payload = response.json()
            self.id_conversation = payload['conversation_id']
            self.id_message_last = payload['message_id']
            return payload['message']
        else:
            str_error = f'Error: {response.status_code} - {response.text}'
            print(str_error)
            return str_error

    # -------------------------------------------------------------------------
    async def reply(self, reply):
        """
        Add a user reply to a conversation on the chatserver

        """

        response = requests.post(
                    url     = urllib.parse.urljoin(URL_CHATSERVER, 'reply'),
                    json    = { 'conversation_id': self.id_conversation,
                                'message_id':      self.id_message_last,
                                'message':         reply },
                    headers = { 'accept':          'application/json',
                                'Content-Type':    'application/json',
                                'Authorization':   f'Bearer {UUID_BEARER}'})
        is_ok = response.status_code == HTTPStatus.OK
        if is_ok:
            payload = response.json()
            self.id_message_last = payload['id']
            return payload['message']
        else:
            str_error = f'Error: {response.status_code} - {response.text}'
            print(str_error)
            return str_error

    # -------------------------------------------------------------------------
    async def telegram(self, str_text):
        """
        Send a message to telegram to be shown to the user.

        """
        await self.context.bot.send_message(chat_id = self.id_chat,
                                            text    = str_text)


