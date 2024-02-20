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


URL_CHATSERVER    = 'https://chatserver.paideia.ai'
UUID_BEARER       = 'C6046DB3-18B4-44AA-A876-96B303378D3F'
KEY_TOKEN         = 'TOKEN_TELEGRAM_PAIDEIA_ROBOT'
STR_TOPIC_DEFAULT = 'Ask the question about the pros and cons of capitalism.'
STR_TOPIC_ZUZALU  = ('What software principles should we follow for Zuzalu '
                     'technologies? Should anything be added? What should be '
                     'done first? What are the highest priorities?')
STR_TOPIC_VITALEA = ('Ask a controversial and creative question about '
                     'longevity that is not about ethics.')


# id_chat -> coroutine
map_logic = dict()


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
    app:       telegram.ext._application.Application
    db:        sqlitedict.SqliteDict
    list_cmd:  list[tuple[str]] = []

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
        else:
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

        str_command = fcn_callback.__name__
        if str_command.startswith('_'):
            str_command = str_command[1:]

        str_doc = fcn_callback.__doc__.strip().splitlines()[0]
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

        str_help_text = 'The following commands are available:\n\n'
        for (str_command, str_doc) in self.list_cmd:
            str_help_text += f'/{str_command}: {str_doc}\n'
        return str_help_text


# =============================================================================
class BotInteractionContext():
    """
    Interaction context for the telegram bot.

    This context will be exited when the
    current interaction with the bot is
    complete.

    An interaction consists of zero or one
    inputs from the user and zero or more
    responses from the bot.

    """

    bot:             BotRuntimeContext
    update:          typing.Any
    context:         typing.Any
    id_chat:         int
    id_conversation: str
    id_message_last: str

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
            state = bot.db[self.id_chat]
        except KeyError:
            self.id_conversation = ''
            self.id_message_last = ''
        else:
            self.id_conversation = state['id_conversation']
            self.id_message_last = state['id_message_last']
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

        self.bot.db[self.id_chat] = dict(
                                        id_conversation = self.id_conversation,
                                        id_message_last = self.id_message_last)
        self.bot.db.commit()

    # -------------------------------------------------------------------------
    async def reset(self, str_topic = None):
        """
        Reset the interaction state.

        """

        logic = self._logic()
        map_logic[self.id_chat] = logic
        await logic.asend(None)
        await logic.asend(str_topic)

    # -------------------------------------------------------------------------
    async def step(self, command = None):
        """
        Step the coroutine.

        """

        # Ensure that we have some logic instantiated.
        #
        try:
            logic = map_logic[self.id_chat]
        except KeyError:
            logic = self._logic()
            map_logic[self.id_chat] = logic
            await logic.asend(None)

        # Single step the logic
        #
        print('step: ' + repr(logic))
        await logic.asend(None)

    # -------------------------------------------------------------------------
    async def _logic(self):
        """
        Program logic.

        """

        # Start the conversation.
        #
        print('START')
        topic = yield
        while topic is None:
            await self.telegram('What topic do you want to discuss?')
            yield
            topic = self.update.message.text

        # Set the topic of the conversation.
        #
        print('TOPIC = ' + repr(topic))
        response = await self.new_conversation(topic)
        await self.telegram(response)

        # Carry out the conversation.
        #
        while True:

            yield
            message = await self.reply(self.update.message.text)
            await self.telegram(message)


    # -------------------------------------------------------------------------
    async def new_conversation(self, topic):
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
        is_ok = response.status_code == http.HTTPStatus.OK
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
        is_ok = response.status_code == http.HTTPStatus.OK
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


# -----------------------------------------------------------------------------
def main():
    """
    Set up command and message handlers and run the telegram bot main loop.

    """

    str_token = key.load(id_value = KEY_TOKEN)

    with BotRuntimeContext(str_token) as bot:

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
