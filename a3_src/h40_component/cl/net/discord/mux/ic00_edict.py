# -*- coding: utf-8 -*-
"""
---

title:
    "Discord message multiplexer stableflow-edict component."

description:
    "."

id:
    "6ffedbc1-d2d1-4731-bf64-30ecaed26c85"

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

# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    list_cfg_cmd = list()
    for cfg_cmd in cfg['command']:
        name =

    # set_id_out = set(outputs.keys())
    # set_id_in  = set(outputs.keys())

    # if 'cmd' not in set_id_in:
    #     raise RuntimeError('cmd must be in input')

    # if 'cmd' not in set_id_out:
    #     raise RuntimeError('cmd must be in output')

    # list_cfg_cmd = list()
    # set_id_cmd   = set_id_out - {'cmd'}
    # for id_cmd in set_id_cmd:
    #     list_cfg_cmd.append(dict(name        = id_cmd,
    #                              description = cfg[id_cmd]['description'])


    # Initialize outputs.
    #
    signal = None
    for id_out in set_id_out:
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    # Loop forever, sending messages
    # to and from the discord client
    # via the two message queues.
    #
    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in tup_id_out:
            if id_out in outputs:
                outputs[id_out]['ena'] = False
                outputs[id_out]['ts'].clear()
                outputs[id_out]['list'].clear()

        # Pass messages and command
        # configuration to the discord
        # bot.
        #
        map_ts          = dict()
        list_msg_to_bot = list()
        list_cmd_to_bot = list()
        for (id_in, list_in) in (('msg', list_msg_to_bot),
                                 ('cmd', list_cmd_to_bot)):

            if id_in in inputs:
                pkt_in = inputs[id_in]
                map_ts = pkt_in['ts']
                list_in.extend(pkt_in['list'])

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
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_out
