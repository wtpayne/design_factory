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

import fl.net.discord.bot
import fl.util.edict
import key


DEFAULT_ENVVAR = 'TOKEN_DISCORD_BOT_DEFAULT'


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    tup_id_in  = ('ctrl', 'cmd', 'msg')
    tup_id_out = ('cmd', 'msg', 'log')
    fl.util.edict.validate(inputs  = inputs,  must_equal = tup_id_in)
    fl.util.edict.validate(outputs = outputs, must_equal = tup_id_out)

    bot = init_discord_bot(
                    filepath_env = cfg.get('filepath_env',  None),
                    envvar_key   = cfg.get('envvar_key',    DEFAULT_ENVVAR),
                    str_token    = cfg.get('str_token',     None),
                    secs_sleep   = cfg.get('secs_sleep',    0.5))

    timestamp = dict()
    signal    = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Pass messages and command
        # configuration to the discord
        # bot.
        #
        list_msg_to_bot = list()
        list_cmd_to_bot = list()
        for (id_in, list_in) in (('msg', list_msg_to_bot),
                                 ('cmd', list_cmd_to_bot)):

            timestamp.update(inputs[id_in]['ts'])
            list_in.extend(inputs[id_in]['list'])

        (list_msg_from_bot,
         list_cmd_from_bot,
         list_log_from_bot) = bot.send((list_msg_to_bot,
                                       list_cmd_to_bot))

        # Recieve messages, command
        # invocations and log items
        # from the doscord bot and
        # pass them on to the rest
        # of the system.
        #
        for (id_out, list_out) in (('msg', list_msg_from_bot),
                                   ('cmd', list_cmd_from_bot),
                                   ('log', list_log_from_bot)):

            if id_out in outputs and list_out:
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(timestamp)
                outputs[id_out]['list'][:] = list_out


# -----------------------------------------------------------------------------
def init_discord_bot(filepath_env = None,
                     envvar_key   = DEFAULT_ENVVAR,
                     str_token    = None,
                     secs_sleep   = 0.5):
    """
    Return the discord client coroutine.

    """

    if str_token is None:
        str_token = key.load(id_value     = envvar_key,
                             filepath_env = filepath_env)

    cfg_bot = { 'secs_sleep': secs_sleep,
                'str_token':  str_token  }
    discord    = fl.net.discord.bot.coro(cfg_bot)

    return discord
