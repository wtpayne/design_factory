# -*- coding: utf-8 -*-
"""
---

title:
    "Unstructured data partitioning component."

description:
    "Provides functionality for extracting
    text from unstructured data."

id:
    "6e3f0a39-2389-4a42-86c4-4080284051d7"

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


import fl.io.unstructured
import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Unstructured data ETL coroutine.

    """

    fl.util.edict.validate(inputs = inputs,  must_contain = ('ctrl',))

    tup_id_in      = tuple(inputs.keys())
    tup_id_out     = tuple(outputs.keys())
    tup_id_in_data = tuple((id_in for id_in in tup_id_in
                                                    if id_in not in ('ctrl',)))

    partitioner = fl.io.unstructured.coro()
    signal      = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if not inputs['ctrl']['ena']:
            continue
        timestamp = inputs['ctrl']['ts']

        list_filedata = list()
        for id_in in tup_id_in_data:
            packet_in = inputs[id_in]
            if not packet_in['ena']:
                continue
            list_filedata.extend(packet_in['list'])

        list_partitions = partitioner.send(list_filedata)

        if list_partitions:
            for id_out in tup_id_out:
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(timestamp)
                outputs[id_out]['list'][:] = list_partitions
