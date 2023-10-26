# -*- coding: utf-8 -*-
"""
---

title:
    "Text interpretation component."

description:
    "Text interpretation."

id:
    "64b2cd26-4723-4ac3-a9af-fa90276e29c9"

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


import fl.load.unstructured
import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Text interpretation coroutine.

    """

    fl.util.edict.validate(inputs = inputs,  must_contain = ('ctrl',))

    tup_id_in      = tuple(inputs.keys())
    tup_id_out     = tuple(outputs.keys())
    tup_id_in_data = tuple((id_in for id_in in tup_id_in
                                                    if id_in not in ('ctrl',)))

    partitioner = fl.load.unstructured.coro()
    signal      = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if not inputs['ctrl']['ena']:
            continue
        timestamp = inputs['ctrl']['ts']

        list_partitions = list()
        for id_in in tup_id_in_data:
            packet_in = inputs[id_in]
            if not packet_in['ena']:
                continue
            list_partitions.extend(packet_in['list'])

        for partition in list_partitions:
            print(partition)

        list_interpretations = None

        if list_interpretations:
            for id_out in tup_id_out:
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(timestamp)
                outputs[id_out]['list'][:] = list_interpretations
