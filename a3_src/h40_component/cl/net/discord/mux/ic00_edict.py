# -*- coding: utf-8 -*-
"""
---

title:
    "Multiplexer stableflow-edict component."

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


import fl.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Enabled dictionary multiplexer component coroutine.

    """

    map_ts   = dict()
    list_msg = list()

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        map_ts.clear()
        list_msg.clear()

        for (id_in, pkt_in) in inputs.items():
            if not pkt_in['ena']:
                continue
            if id_in == 'ctrl':
                map_ts = pkt_in['ts']
                continue
            list_msg.extend(pkt_in['list'])

        if list_msg:
            for (id_out, pkt_out) in outputs.items():
                pkt_out['ena'] = True
                pkt_out['ts'].update(map_ts)
                pkt_out['list'][:] = list_msg