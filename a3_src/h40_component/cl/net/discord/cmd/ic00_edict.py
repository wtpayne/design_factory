# -*- coding: utf-8 -*-
"""
---

title:
    "Discord command configurator/demultiplexer stableflow-edict component."

description:
    "This component enables Discord bot commands
    to be configured and then demultiplexed to be
    routed to different downstream components."

id:
    "a3f6c422-66ff-48e5-b7b6-56b322522904"

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


import collections

import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord command configurator and demultiplexer component coroutine.

    """

    # Validate configuration.
    #
    fl.util.edict.validate(cfg        = cfg,
                           must_equal = ('cmd',))
    for cfg_cmd in cfg['cmd']:
        for key in ('id_cmd', 'desc'):
            if key not in cfg_cmd:
                raise RuntimeError(
                        'Missing command configuration key: {key}'.format(
                                                                    key = key))
    # Validate inputs and outputs.
    #
    fl.util.edict.validate(inputs       = inputs,
                           must_equal   = ('cmd', 'ctrl'))
    fl.util.edict.validate(outputs      = outputs,
                           must_contain = ('cmd', 'cfg_cmd'))

    # Configure commands from configuration.
    #
    list_cfg_cmd = list()
    for cfg_cmd in cfg['cmd']:
        id_cmd          = cfg_cmd['id_cmd']
        str_description = cfg_cmd['desc']
        list_cfg_cmd.append(dict(name        = id_cmd,
                                 description = str_description))

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Handle control inputs.
        #
        timestamp = None
        if not inputs['ctrl']['ena']:
            continue
        timestamp = inputs['ctrl']['ts']

        # Process incoming commands.
        #
        if inputs['cmd']['ena']:
            outputs['cmd']['ena']     = True
            outputs['cmd']['ts']      = timestamp
            outputs['cmd']['list'][:] = inputs['cmd']['list']

        # Process command configuration.
        #
        if list_cfg_cmd:
            outputs['cfg_cmd']['ena']     = True
            outputs['cfg_cmd']['ts']      = timestamp
            outputs['cfg_cmd']['list'][:] = list_cfg_cmd
            list_cfg_cmd.clear()
