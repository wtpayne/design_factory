# -*- coding: utf-8 -*-
"""
---

title:
    "Discord HTTP API integration support module."

description:
    "This Python module is designed to interact
    with the Discord API using a separate process
    for handling requests and responses."

id:
    "08a41d6d-9b21-4248-b87a-9f4c7a003648"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

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

...
"""


import asyncio
import collections
import multiprocessing
import os
import queue

import fl.util


BOT_COMMAND_PREFIX = '/'


# -----------------------------------------------------------------------------
FileData = collections.namedtuple(
                'FileData', ['filename', 'spoiler', 'description', 'buffer'])


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro(cfg_bot):
    """
    Yield results for workflow coroutines sent to the OpenAI web API.

    Start the client in a separate process.

    """

    tup_key_required = ('str_token',)
    for str_key in tup_key_required:
        if str_key not in cfg_bot:
            raise ValueError(
                'Missing required configuration: {key}'.format(key = str_key))
    if not isinstance(cfg_bot['str_token'], str):
        raise ValueError(
                'cfg_bot["str_token"] must be a string.')
    cfg_bot['secs_sleep'] = cfg_bot.get('secs_sleep', 0.5)
    if not isinstance(cfg_bot['secs_sleep'], (int, float)):
        raise ValueError(
                'cfg_bot["secs_sleep"] must be an integer or float value.')

    str_name_process   = 'discord-bot'
    fcn_bot            = _discord_bot
    queue_msg_to_bot   = multiprocessing.Queue()  # msg system  --> discord
    queue_cmd_to_bot   = multiprocessing.Queue()  # cmd system  --> discord
    queue_msg_from_bot = multiprocessing.Queue()  # msg discord --> system
    queue_cmd_from_bot = multiprocessing.Queue()  # cmd discord --> system
    queue_log_from_bot = multiprocessing.Queue()  # log discord --> system
    tup_args           = (cfg_bot,
                          queue_msg_to_bot,
                          queue_cmd_to_bot,
                          queue_msg_from_bot,
                          queue_cmd_from_bot,
                          queue_log_from_bot)
    proc_bot           = multiprocessing.Process(
                                        target = fcn_bot,
                                        args   = tup_args,
                                        name   = str_name_process,
                                        daemon = True)  # So we get terminated
    proc_bot.start()

    list_msg_to_bot   = list()
    list_cmd_to_bot   = list()
    list_msg_from_bot = list()
    list_cmd_from_bot = list()
    list_log_from_bot = list()

    while True:

        list_msg_to_bot.clear()
        list_cmd_to_bot.clear()

        (list_msg_to_bot,
         list_cmd_to_bot) = yield (list_msg_from_bot,
                                   list_cmd_from_bot,
                                   list_log_from_bot)

        list_msg_from_bot.clear()
        list_cmd_from_bot.clear()
        list_log_from_bot.clear()

        # If the rest of the system sends us
        # any system messages or new commands
        # to configure, then forward them
        # on to the discord client process
        # to either be sent to the relevant
        # channel (in the case of messages),
        # or to use to configure new commands
        # (in the case of command configuration).
        #
        for tup_msg in list_msg_to_bot:
            try:
                queue_msg_to_bot.put(tup_msg, block = False)
            except queue.Full as err:
                list_log_from_bot.append(
                        'Message dropped: queue_msg_to_bot is full.')

        for cfg_cmd in list_cmd_to_bot:
            try:
                queue_cmd_to_bot.put(cfg_cmd, block = False)
            except queue.Full as err:
                list_log_from_bot.append(
                        'Command config dropped: queue_cmd_to_bot is full.')

        # Retrieve any user messages, command
        # invocations or log messages from the
        # discord client and forward them to
        # the rest of the system for further
        # processing.
        #
        while True:
            try:
                list_msg_from_bot.append(queue_msg_from_bot.get(block = False))
            except queue.Empty:
                break

        while True:
            try:
                list_cmd_from_bot.append(queue_cmd_from_bot.get(block = False))
            except queue.Empty:
                break

        while True:
            try:
                list_log_from_bot.append(queue_log_from_bot.get(block = False))
            except queue.Empty:
                break


# -----------------------------------------------------------------------------
def _discord_bot(cfg_bot,
                 queue_msg_to_bot,
                 queue_cmd_to_bot,
                 queue_msg_from_bot,
                 queue_cmd_from_bot,
                 queue_log_from_bot):
    """
    Run the discord client.

    This function is expected to be run in a separate daemon process.

    """

    import collections.abc
    import functools
    import io
    import logging
    import os

    import discord
    import discord.ext
    import discord.ext.commands

    intents                 = discord.Intents.default()
    intents.guilds          = True
    intents.dm_messages     = True
    intents.dm_reactions    = True
    intents.message_content = True
    intents.messages        = True
    intents.reactions       = True
    bot                     = discord.ext.commands.Bot(
                                        command_prefix = BOT_COMMAND_PREFIX,
                                        intents        = intents)

    buffer_log = io.StringIO()
    loghandler = logging.StreamHandler(buffer_log)
    log        = logging.getLogger('discord')


    # -------------------------------------------------------------------------
    @bot.event
    async def on_ready():
        """
        Create worker tasks once the client is ready.

        This callback is invoked once the
        client is done preparing the data
        that has been received from Discord.
        This usually happens after login
        is successful and the Client.guilds
        and similar data structures are
        filled up.

        """

        task_msg = bot.loop.create_task(coro = _service_all_queues(
                                                        cfg_bot,
                                                        queue_msg_to_bot,
                                                        queue_cmd_to_bot,
                                                        queue_log_from_bot))


    # -------------------------------------------------------------------------
    async def _service_all_queues(cfg_bot,
                                  queue_msg_to_bot,
                                  queue_cmd_to_bot,
                                  queue_log_from_bot):
        """
        Message queue servicing coroutine.

        This coroutine is intended to
        run continuously, servicing
        the multiprocessing.queue
        instance that feeds messages
        from the rest of the system to
        the discord bot.

        This coroutine is started from
        the on_ready callback - i.e as
        soon as the discord bot is
        ready.

        """

        # This is a redundant sanity check, as
        # the service task should be created in
        # the on_ready callback.
        #
        await bot.wait_until_ready()

        map_chan               = dict()
        map_cmd                = dict()
        count_attempt_send_log = 0

        while True:

            do_sleep = True

            # Service outbound messages from the system to discord.
            # =====================================================
            #
            try:
                tup_msg = queue_msg_to_bot.get(block = False)
            except queue.Empty:
                pass

            else:

                # Don't sleep if data is ready.
                #
                do_sleep = False

                # Validate tup_msg
                #
                valid_id_chan = (int,)
                valid_msg     = (str, collections.abc.Mapping)
                if (    (not isinstance(tup_msg, tuple))
                     or (not len(tup_msg) == 2)
                     or (not isinstance(tup_msg[0], valid_id_chan))
                     or (not isinstance(tup_msg[1], valid_msg))):

                    raise RuntimeError(
                            'Invalid message recieved: {msg}'.format(
                                                        msg = repr(tup_msg)))

                # If we have a new message to
                # handle, then simply send it
                # to the specified channel.
                #
                (id_chan, msg) = tup_msg
                if id_chan not in map_chan.keys() or map_chan[id_chan] is None:
                    map_chan[id_chan] = bot.get_channel(id_chan)

                # Messages are either a string
                # or they are a dict with fields
                # that correspond to the keyword
                # args of the discord channel
                # send function.
                #
                # https://discordpy.readthedocs.io/en/stable/api.html#channels
                #
                # We want to be able to send files
                # without requiring access to the
                # local filesystem, so we add
                # special handling for 'file'
                # fields to support the use of
                # a FileData named tuple, which
                # allows us to encode the file
                # in an in-memory buffer rather
                # than as a file handle.
                #
                if map_chan[id_chan] is None:

                    log.critical(
                        'Unable to access channel: {id}. ' \
                        'Please check permissions.'.format(id = str(id_chan)))

                elif isinstance(msg, str):

                    await map_chan[id_chan].send(msg)

                elif isinstance(msg, collections.abc.Mapping):

                    if 'file' in msg and isinstance(msg['file'], FileData):
                        file_data   = msg['file']
                        msg['file'] = discord.File(
                                    fp          = io.BytesIO(file_data.buffer),
                                    filename    = file_data.filename,
                                    spoiler     = file_data.spoiler,
                                    description = file_data.description)

                    await map_chan[id_chan].send(**msg)

                else:

                    raise RuntimeError(
                            'Message type not handled: {type}. ' \
                            'Expecting a string or dict.'.format(
                                                        type = type(msg)))

            # Service command configuration from the system to discord.
            # =========================================================
            #
            try:
                cfg_cmd = queue_cmd_to_bot.get(block = False)
            except queue.Empty:
                pass

            else:

                # Don't sleep if data is ready.
                #
                do_sleep = False

                # Validate cfg_cmd.
                #
                tup_key_required = ('name', 'description')
                for str_key in tup_key_required:
                    if str_key not in cfg_cmd:
                        raise ValueError(
                                'Command configuration is '\
                                'Missing key: {key}.'.format(key = str_key))
                    if not isinstance(cfg_cmd[str_key], str):
                        raise ValueError(
                                'Command configuration {key} should be '\
                                'a string. Got {typ} instead.'.format(
                                                key = str_key,
                                                typ = type(cfg_cmd[str_key])))

                # -------------------------------------------------------------
                async def on_command_generic(ctx, *args):
                    """
                    Generic command callback.

                    """

                    try:
                        map_cmd = dict(args         = ctx.args[1:],
                                       kwargs       = ctx.kwargs,
                                       prefix       = ctx.prefix,
                                       name_command = ctx.command.name,
                                       id_guild     = ctx.guild.id,
                                       name_guild   = ctx.guild.name,
                                       id_channel   = ctx.channel.id,
                                       name_channel = ctx.channel.name,
                                       id_author    = ctx.author.id,
                                       name_author  = ctx.author.name,
                                       nick_author  = ctx.author.nick)
                        queue_cmd_from_bot.put(map_cmd, block = False)
                    except queue.Full:
                        log.error('Command input dropped. ' \
                                  'queue_cmd_from_bot is full.')

                map_cmd[cfg_cmd['name']] = discord.ext.commands.Command(
                                                on_command_generic,
                                                name = cfg_cmd['name'],
                                                help = cfg_cmd['description'])
                bot.add_command(map_cmd[cfg_cmd['name']])

            # Send log data from the discord bot to the rest of the system.
            # =============================================================
            #
            # If there is any log data in the
            # buffer, then enqueue it to be
            # sent back to the rest of the
            # system.
            #
            str_log = buffer_log.getvalue()
            if str_log:
                try:
                    queue_log_from_bot.put(str_log, block = False)
                except queue.Full:
                    count_attempt_send_log += 1
                    log.error(
                        'Log message dropped. ' \
                        'queue_log_from_bot is full.')
                    if count_attempt_send_log > 10:
                        print(str_log)
                else:
                    loghandler.flush()
                    count_attempt_send_log = 0

            if do_sleep:
                await asyncio.sleep(cfg_bot['secs_sleep'])


    # -------------------------------------------------------------------------
    @bot.event
    async def on_command_error(ctx, error):
        """
        Handle errors in commands.

        """

        raise RuntimeError('Command error: {err}.'.format(err = error))


    # -------------------------------------------------------------------------
    @bot.event
    async def on_message(message):
        """
        Handle messages that are sent to the client.

        This coroutine is invoked
        whenever a message is created
        and sent.

        This coroutine is intended to
        simply forward the content of
        the message to the rest of the
        system via the queue_msg_from_bot
        queue.

        """

        await bot.process_commands(message)

        if message.author.bot:
            return

        if message.content.startswith(BOT_COMMAND_PREFIX):
            return

        msg = dict(msg_type     = 'message',
                   id_prev      = None,
                   id_msg       = message.id,
                   id_author    = message.author.id,
                   name_author  = message.author.name,
                   nick_author  = message.author.nick,
                   id_channel   = message.channel.id,
                   name_channel = message.channel.name,
                   content      = message.content)

        try:
            queue_msg_from_bot.put(msg, block = False)
        except queue.Full:
            log.error('Message dropped. queue_msg_from_bot is full.')

    # -------------------------------------------------------------------------
    @bot.event
    async def on_message_edit(msg_before, msg_after):
        """
        Handle message-edits that are sent to the client.

        This coroutine is invoked
        whenever a message receives
        an update event. If the
        message is not found in the
        internal message cache, then
        these events will not be
        called.

        Messages might not be in
        cache if the message is
        too old or the client is
        participating in high
        traffic guilds.

        This coroutine is intended to
        simply forward the content of
        the message to the rest of the
        system via the queue_msg_from_bot
        queue.

        """

        if msg_after.author.bot:
            return

        if msg_after.content.startswith(BOT_COMMAND_PREFIX):
            return

        msg = dict(msg_type     = 'message',
                   id_prev      = msg_before.id,
                   id_msg       = msg_after.id,
                   id_author    = msg_after.author.id,
                   name_author  = msg_after.author.name,
                   nick_author  = msg_after.author.nick,
                   id_channel   = msg_after.channel.id,
                   name_channel = msg_after.channel.name,
                   content      = msg_after.content)

        try:
            queue_msg_from_bot.put(msg, block = False)
        except queue.Full:
            log.error('Message dropped. queue_msg_from_bot is full.')

    # Run the client.
    #
    # bot.run(token       = cfg_bot['str_token'],
    #         reconnect   = False,
    #         log_level   = logging.INFO,
    #         log_handler = loghandler)
    bot.run(token       = cfg_bot['str_token'],
            reconnect   = False,
            log_level   = logging.INFO)
