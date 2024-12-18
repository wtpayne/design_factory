# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot configuration and runtime lifecycle context module."

description:
    "This module contains a class based context
    manager to help manage the configuration and
    runtime lifecycle of a Telegram bot that is
    implemented using the python-telegram-bot
    library."

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
import os.path
import typing
import weakref

import telegram.ext  # pylint: disable=import-error,no-name-in-module

import t000_wtp.harmonica.logic.track as track


# =============================================================================
class Context():
    """
    Configuration and runtime lifecycle context for a telegram bot.

    Enter this context before any configuration
    commands are called on it.

    The bot event loop (or polling) will
    automatically start running at the point
    where the context exits, and will stop
    when the program instance terminates.

    The role of this context manager is to
    hold configuration information and to
    ensure that transactions are committed
    and that all databases are closed on
    program termination.

    """

    str_token:   str
    app:         typing.Any
    list_cmd:    list[tuple[str, str]] = []
    track_table: track.Table

    # -------------------------------------------------------------------------
    def __init__(self, str_token) -> None:
        """
        Return an instance of the telegram bot configuration Context.

        """

        self.str_token   = str_token
        app_builder      = telegram.ext.ApplicationBuilder().token(str_token)
        self.app         = app_builder.build()
        self.list_cmd    = [] # [(str_command, str_doc)], for help text.
        self.track_table = track.Table(proxy_bot = weakref.proxy(self))

    # -------------------------------------------------------------------------
    def __enter__(self) -> 'Context':
        """
        Enter the configuration context for the telegram bot instance.

        """

        return self

    # -------------------------------------------------------------------------
    def __exit__(self, type_exc, value_exc, tb_exc) -> None:
        """
        Exit the configuration context for the telegram bot instance.

        This also runs the bot event loop.

        """

        # Check to see if an exception has been
        # thrown while configuring the bot.
        #
        if type_exc is not None:

            self.track_table.close(do_commit = False)
            raise type_exc(value_exc)

        # If the bot has been configured
        # successfully, then run the bot's
        # main loop (polling or events) and
        # ensure we close the db at the end.
        #
        try:

            self.app.run_polling()

        finally:

            self.track_table.close(do_commit = True)


    # -------------------------------------------------------------------------
    def add_message_handler(self, fcn_callback) -> None:
        """
        Add a new message handler to the bot.

        """

        filter_txt        = telegram.ext.filters.TEXT
        filter_cmd        = telegram.ext.filters.COMMAND
        select_if_not_cmd = filter_txt & ~filter_cmd

        self.app.add_handler(
            telegram.ext.MessageHandler(
                filters  = select_if_not_cmd,
                callback = functools.partial(fcn_callback,
                                             weakref.proxy(self)),
                block    = True))

    # -------------------------------------------------------------------------
    def add_callback_query_handler(self, fcn_callback) -> None:
        """
        Add a new callback query handler to the bot.

        """

        self.app.add_handler(
            telegram.ext.CallbackQueryHandler(
                callback = functools.partial(fcn_callback,
                                             weakref.proxy(self)),
                block    = True))

    # -------------------------------------------------------------------------
    def add_member_update_handler(self, fcn_callback) -> None:
        """
        Add a new chat member update handler to the bot.

        """

        self.app.add_handler(
            telegram.ext.ChatMemberHandler(
                callback          = functools.partial(fcn_callback,
                                                      weakref.proxy(self)),
                chat_member_types = telegram.ext.ChatMemberHandler.CHAT_MEMBER,
                block             = True))

    # -------------------------------------------------------------------------
    def add_command_handler(self, fcn_callback) -> None:
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
                callback = functools.partial(fcn_callback,
                                             weakref.proxy(self)),
                block    = True))

    # -------------------------------------------------------------------------
    def help_text(self) -> str:
        """
        Return help text for the bot.

        """

        str_help_text: str = 'The following commands are available:\n\n'
        for (str_command, str_doc) in self.list_cmd:
            str_help_text += f'/{str_command}: {str_doc}\n'
        return str_help_text


