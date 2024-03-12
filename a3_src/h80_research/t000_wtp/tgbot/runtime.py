# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot runtime context module."

description:
    "This module contains a class based context
    manager to help manage the runtime life cycle
    of a Telegram bot that is implemented using
    the python-telegram-bot library."

id:
    "9ed01adb-c72d-4255-a0ef-9e283c3e684e"

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
import logging
import os.path
import typing

import dill
import sqlitedict
import telegram
import telegram.ext  # pylint: disable=import-error,no-name-in-module


# =============================================================================
class Context():
    """
    Runtime context for a telegram bot.

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

        dirpath_self   = os.path.dirname(os.path.realpath(__file__))
        filename_db    = 'bot.db'
        filepath_db    = os.path.join(dirpath_self, filename_db)
        self.db        = sqlitedict.SqliteDict(filepath_db,
                                               encode = dill.dumps,
                                               decode = dill.loads)

        app_builder    = telegram.ext.ApplicationBuilder().token(str_token)
        self.app       = app_builder.build()

        # [(str_command, str_doc)], for help text.
        self.list_cmd  = []

        # id_chat -> coroutine
        #
        self.map_chat  = {}

        # id_chat -> asyncio.queue
        #
        self.map_queue = {}

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
    def handle_member_update(self, fcn_callback):
        """
        Add a new chat member update handler to the bot.

        """

        self.app.add_handler(
            telegram.ext.ChatMemberHandler(
                callback          = functools.partial(fcn_callback, self),
                chat_member_types = telegram.ext.ChatMemberHandler.CHAT_MEMBER,
                block             = True))

    # -------------------------------------------------------------------------
    def handle_command(self, fcn_callback):
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
    def handle_messages(self, fcn_callback):
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
