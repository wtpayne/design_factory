# -*- coding: utf-8 -*-
"""
---

title:
    "Discord bot stableflow-edict component."

description:
    "This component enables integration with the
    Discord HTTP API."

id:
    "8747de1c-76ac-4f63-a88d-f67a60515571"

type:
    dt004_python_stableflow_edict_component

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


import dotenv
import os
import logging

import fl.net.discord.bot
import fl.util.edict
import key


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    fl.util.edict.validate(inputs = inputs,  must_contain = ('ctrl',))

    str_token    = cfg.get('str_token',     None)
    filepath_env = cfg.get('filepath_env',  None)
    key_token    = cfg.get('key_token',     'TOKEN_DISCORD_DEFAULT')
    secs_sleep   = cfg.get('secs_sleep',    0.5)
    log_level    = cfg.get('log_level',     logging.WARNING)
    list_cfg_msg = cfg.get('msg',           list())
    map_id       = runtime.get('id',        dict())
    id_system    = map_id.get('id_system',  None)
    id_node      = map_id.get('id_node',    None)

    if str_token is None:
        str_token = key.load(id_value     = key_token,
                             filepath_env = filepath_env)
    bot = fl.net.discord.bot.coro(cfg_bot = dict(id_log_event = 'discord',
                                                 str_token    = str_token,
                                                 secs_sleep   = secs_sleep,
                                                 id_system    = id_system,
                                                 id_node      = id_node))

    set_type_in = set((
                'cfg_msgcmd',  # Configuration for message commands.
                'cfg_appcmd',  # Configuration for application commands.
                'msg_guild',   # Messages to a guild channel.
                'msg_dm'))     # Messages to a DM channel.

    # If there are one or more outputs which are
    # named after a message type, then we will
    # route messages of that type to the
    # corresponding output.
    #
    set_type_out = set((
                'log_event',     # Error messages and log messages.
                'log_metric',    # Quantitative metrics for KPIs etc...
                'log_data',      # Raw data for resimulation.
                'msgcmd_dm',     # Msg command invocations from DM channels.
                'msgcmd_guild',  # Msg command invocations from guild channels.
                'appcmd_dm',     # App command invocations from DM channels.
                'appcmd_guild',  # App command invocations from guild channels.
                'msg_dm',        # Messages from DM channels.
                'msg_guild',     # Messages from guild channels.
                'edit_dm',       # Message edits from DM channels.
                'edit_guild',    # Message edits from guild channels.
                'btn'))          # Button press events.

    tup_key_in       = tuple(inputs.keys())
    tup_key_out      = tuple(outputs.keys())
    tup_key_msg_in   = tuple((k for k in tup_key_in  if k not in ('ctrl',)))
    tup_key_msg_out  = tuple((k for k in tup_key_out if k not in set_type_out))
    tup_key_type_out = tuple((k for k in tup_key_out if k in set_type_out))
    list_to_bot      = list()
    list_to_bot[:]   = list_cfg_msg
    list_from_bot    = list()
    timestamp        = dict()
    signal           = fl.util.edict.init(outputs)

    while True:

        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Pass messages and command
        # configuration to the discord
        # bot.
        #
        for str_key in tup_key_msg_in:
            list_to_bot.extend(inputs[str_key]['list'])

        # Recieve messages, command
        # invocations and log items
        # from the doscord bot.
        #
        list_from_bot.clear()
        list_from_bot[:] = bot.send(list_to_bot)
        list_to_bot.clear()
        if not list_from_bot:
            continue

        # Route messages to type-specific
        # outputs.
        #
        list_msg     = list_from_bot
        list_include = list()
        list_exclude = list()
        for key_type in tup_key_type_out:
            list_include.clear()
            list_exclude.clear()

            for msg in list_msg:
                if msg['type'] == key_type:
                    list_include.append(msg)
                else:
                    list_exclude.append(msg)

            if list_include:
                outputs[key_type]['ena'] = True
                outputs[key_type]['ts'].update(timestamp)
                outputs[key_type]['list'][:] = list_include

            if list_exclude:
                list_msg[:] = list_exclude
                continue
            else:
                break

        # If we have any remaining unrouted
        # output, then we copy that to every
        # other output channel.
        #
        if list_msg:
            for str_key in tup_key_msg_out:
                outputs[str_key]['ena'] = True
                outputs[str_key]['ts'].update(timestamp)
                outputs[str_key]['list'][:] = list_msg
