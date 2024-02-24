# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot module."

description:
    "This module contains functions for
    configuring and running a Telegram bot
    using the python-telegram-bot library."

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


import functools
import http
import importlib.metadata
import logging
import os
import os.path
import sys
import typing
import urllib.parse

import dill
import dotenv
import pydantic
import requests
import sqlitedict
import telegram
import telegram.ext  # pylint: disable=import-error,no-name-in-module


name_package = 't000_wtp.telegram.bot'
try:
    __version__ = importlib.metadata.version(name_package)
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


URL_CHATSERVER    = 'https://chatserver.paideia.ai'
KEY_TOKEN         = 'TOKEN_TELEGRAM_PAIDEIA_ROBOT'
STR_TOPIC_DEFAULT = 'Ask the question about the pros and cons of capitalism.'
STR_TOPIC_ZUZALU  = ('What software principles should we follow for Zuzalu '
                     'technologies? Should anything be added? What should be '
                     'done first? What are the highest priorities?')
STR_TOPIC_VITALEA = ('Ask a controversial and creative question about '
                     'longevity that is not about ethics.')


# id_chat -> coroutine
map_logic = {}


# =============================================================================
class BotRuntimeContext():
    """
    Runtime context for the telegram bot.

    Enter this context before any configuration
    commands are called on it.

    The bot event loop (or polling) will
    automatically start running at the point
    where the context exits, and will stop
    when the program instance terminates.

    The role of this context manager is to
    ensure that transactions are committed
    and that the database is closed on
    program termination.

    Convenience functions are also provided
    to support adding command handlers and
    message handlers.

    """

    str_token: str
    app:       typing.Any
    db:        sqlitedict.SqliteDict
    list_cmd:  list[tuple[str, str]] = []

    # -------------------------------------------------------------------------
    def __init__(self, str_token):
        """
        Return an instance of BotRuntimeContext.

        """

        self.str_token = str_token

        str_format     = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format = str_format,
                            level  = logging.INFO)

        dirpath_self  = os.path.dirname(os.path.realpath(__file__))
        filename_db   = 'bot.db'
        filepath_db   = os.path.join(dirpath_self, filename_db)
        self.db       = sqlitedict.SqliteDict(filepath_db,
                                              encode = dill.dumps,
                                              decode = dill.loads)

        app_builder   = telegram.ext.ApplicationBuilder().token(str_token)
        self.app      = app_builder.build()

        self.list_cmd = []

    # -------------------------------------------------------------------------
    def __enter__(self):
        """
        Enter the run-time context for the telegram bot instance.

        """

        return self

    # -------------------------------------------------------------------------
    def __exit__(self, type_exc, value_exc, tb_exc):
        """
        Exit the run-time context for the telegram bot instance.

        """

        # Check to see if an exception has been
        # thrown while configuring the bot.
        #
        if type_exc is not None:
            self.db.close()
            raise type_exc(value_exc)

        # If the bot has been configured
        # successfully, then run the bot's
        # main loop (polling or events) and
        # ensure we close the db at the end.
        #
        try:
            self.app.run_polling()
        finally:
            self.db.commit()
            self.db.close()
            self.db = None

    # -------------------------------------------------------------------------
    def command_handler(self, fcn_callback):
        """
        Add a new command handler to the bot.

        """

        str_command: str = fcn_callback.__name__
        if str_command.startswith('_'):
            str_command = str_command[1:]

        str_doc: str = fcn_callback.__doc__.strip().splitlines()[0]
        self.list_cmd.append((str_command, str_doc))

        self.app.add_handler(
            telegram.ext.CommandHandler(
                        command  = str_command,
                        callback = functools.partial(fcn_callback, self)))

    # -------------------------------------------------------------------------
    def message_handler(self, fcn_callback):
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
    def help_text(self):
        """
        Return help text for the bot.

        """

        str_help_text: str = 'The following commands are available:\n\n'
        for (str_command, str_doc) in self.list_cmd:
            str_help_text += f'/{str_command}: {str_doc}\n'
        return str_help_text


# =========================================================================
class BotInteractionState(pydantic.BaseModel):
    """
    Bot interaction state.

    """

    version:          int = 1
    id_conversation:  str = ''
    id_message_last:  str = ''
    str_message_last: str = ''
    str_topic:        str = ''


# =============================================================================
class BotInteractionContext():
    """
    Interaction context for the telegram bot.

    This context will be exited when the
    current interaction with the bot is
    complete.

    An interaction consists of zero or one
    inputs from the user and zero or more
    responses from the bot. In other words
    any action taken by or to the bot.

    """

    id_chat: int
    bot:     BotRuntimeContext
    update:  typing.Any
    context: typing.Any
    state:   BotInteractionState

    # -------------------------------------------------------------------------
    def __init__(self,
                 bot:     BotRuntimeContext,
                 update:  typing.Any,
                 context: typing.Any):
        """
        Return an instance of BotInteractionContext.

        Gets called at the start of each interaction.

        """

        self.id_chat = update.effective_chat.id

        try:
            self.state   = BotInteractionState(**bot.db[self.id_chat])
        except KeyError:
            self.state   = BotInteractionState()
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
    async def telegram(self, str_text):
        """
        Send a message to telegram to be shown to the user.

        """

        await self.context.bot.send_message(chat_id = self.id_chat,
                                            text    = str_text)

    # -------------------------------------------------------------------------
    async def reset(self, str_topic = ''):
        """
        Reset the interaction state.

        """

        self.state.str_topic         = str_topic
        self.state.str_message_last  = ''
        map_logic[self.id_chat] = self._logic()
        await map_logic[self.id_chat].asend(None)
        await map_logic[self.id_chat].asend(self.state)

    # -------------------------------------------------------------------------
    async def step(self, command = None):
        """
        Single step the logic coroutine, creating it if necessary.

        """

        self.state.str_message_last = self.update.message.text
        try:
            await map_logic[self.id_chat].asend(self.state)
        except KeyError:
            map_logic[self.id_chat] = self._logic(self.state)
            await map_logic[self.id_chat].asend(None)
            await map_logic[self.id_chat].asend(self.state)

    # -------------------------------------------------------------------------
    async def _logic(self):
        """
        Program logic.

        """

        # Start the conversation.
        #
        state = yield
        while not state.str_topic:
            await self.telegram('What topic do you want to discuss?')
            state = yield
            state.str_topic = state.str_message_last

        await self.telegram(await self._new_conversation(state.str_topic))

        # Carry out the conversation.
        #
        while True:
            state   = yield
            message = await self._reply(state.str_message_last)
            if message:
                await self.telegram(message)

    # -------------------------------------------------------------------------
    async def _new_conversation(self, topic):
        """
        Create a new conversation on the chatserver.

        """

        response = requests.post(**self._post_params('new'),
                                 json = { 'name':    'dfs_v1',
                                          'request': { 'topic': topic }})
        if response.status_code != http.HTTPStatus.OK:
            return self._error_message(response)

        payload = response.json()
        self.state.id_conversation = payload['conversation_id']
        self.state.id_message_last = payload['message_id']
        return payload['message']

    # -------------------------------------------------------------------------
    async def _reply(self, reply):
        """
        Add a user reply to a conversation on the chatserver

        """

        id_conversation = self.state.id_conversation
        id_message_last = self.state.id_message_last
        response = requests.post(**self._post_params('reply'),
                                 json = { 'conversation_id': id_conversation,
                                          'message_id':      id_message_last,
                                          'message':         reply })
        if response.status_code != http.HTTPStatus.OK:
            return self._error_message(response)

        payload = response.json()
        self.state.id_message_last = payload['id']
        return payload['message']

    # -------------------------------------------------------------------------
    def _post_params(self, endpoint):
        """
        Return standard requests.post parameters.

        """

        uuid_bearer = os.getenv("UUID_BEARER_CHATSERVER")
        return { 'url':     urllib.parse.urljoin(URL_CHATSERVER, endpoint),
                 'headers': { 'accept':        'application/json',
                              'Content-Type':  'application/json',
                              'Authorization': f'Bearer {uuid_bearer}'},
                 'timeout': 10 }

    # -------------------------------------------------------------------------
    def _error_message(self, response):
        """
        Log an error and return a suitable user-facing error message.

        """

        logging.error(f'Error: {response.status_code} - {response.text}')
        is_not_found = response.status_code == http.HTTPStatus.NOT_FOUND # 404
        if is_not_found:
            return ('We have encountered an error. '
                    'Please restart the conversation.')
        return f'Internal error: {response.status_code}'


# -----------------------------------------------------------------------------
def main():
    """
    Set up command and message handlers and run the telegram bot main loop.

    """

    dotenv.load_dotenv()
    with BotRuntimeContext(os.getenv(KEY_TOKEN)) as bot:
        bot.command_handler(_start)
        bot.command_handler(_zuzalu)
        bot.command_handler(_vitalia)
        bot.command_handler(_help)
        bot.command_handler(_about)
        bot.message_handler(_msg)


# -----------------------------------------------------------------------------
async def _start(
            bot:     BotRuntimeContext,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Configure and start a new conversation.

    """

    with BotInteractionContext(bot     = bot,
                               update  = update,
                               context = context) as interaction:

        await interaction.reset()


# -----------------------------------------------------------------------------
async def _zuzalu(
            bot:     BotRuntimeContext,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Start a new conversation on the zuzalu topic.

    """

    with BotInteractionContext(bot     = bot,
                               update  = update,
                               context = context) as interaction:

        await interaction.reset(str_topic = STR_TOPIC_ZUZALU)


# -----------------------------------------------------------------------------
async def _vitalia(
            bot:     BotRuntimeContext,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Start a new conversation on the vitalia topic.

    """

    with BotInteractionContext(bot     = bot,
                               update  = update,
                               context = context) as interaction:

        await interaction.reset(str_topic = STR_TOPIC_VITALEA)


# -----------------------------------------------------------------------------
async def _help(
            bot:     BotRuntimeContext,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print a list of commands.

    """

    with BotInteractionContext(bot     = bot,
                               update  = update,
                               context = context) as interaction:

        await interaction.telegram(bot.help_text())


# -----------------------------------------------------------------------------
async def _about(
            bot:     BotRuntimeContext,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Print information about the bot.

    """

    with BotInteractionContext(bot     = bot,
                               update  = update,
                               context = context) as interaction:

        await interaction.telegram(f'Paideia bot version {__version__}')


# -----------------------------------------------------------------------------
async def _msg(
            bot:     BotRuntimeContext,
            update:  telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """
    Handler function for non-command messages.

    """

    with BotInteractionContext(bot     = bot,
                               update  = update,
                               context = context) as interaction:

        await interaction.step()


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
