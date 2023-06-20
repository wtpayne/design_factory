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


import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord command configurator and demultiplexer component coroutine.

    """

    signal     = None
    tup_id_cmd = tuple(cfg['cmd'].keys())
    set_id_cmd = set(tup_id_cmd)
    tup_id_in  = ('cmd', 'ctrl')
    tup_id_out = tup_id_cmd + ('cmd',)
    fl.util.edict.validate(inputs  = inputs,  must_equal = tup_id_in)
    fl.util.edict.validate(outputs = outputs, must_equal = tup_id_out)
    fl.util.edict.init(outputs)

    # Configure commands from configuration.
    #
    list_cfg_cmd = list()
    for id_cmd in tup_id_cmd:
        list_cfg_cmd.append(dict(name        = id_cmd,
                                 description = cfg['cmd'][id_cmd]))

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
            for map_cmd in inputs['cmd']['list']:
                id_cmd = map_cmd['name_command']

                if id_cmd not in set_id_cmd:
                    raise RuntimeError(
                            'Did not recognize command: {id_cmd}'.format(
                                                            id_cmd = id_cmd))

                outputs[id_cmd]['ena'] = True
                outputs[id_cmd]['ts']  = timestamp
                outputs[id_cmd]['list'].append(map_cmd)

        # Process command configuration.
        #
        if list_cfg_cmd:

            import pprint
            pprint.pprint(list_cfg_cmd)

            outputs['cmd']['ena']     = True
            outputs['cmd']['ts']      = timestamp
            outputs['cmd']['list'][:] = list_cfg_cmd
            list_cfg_cmd.clear()
