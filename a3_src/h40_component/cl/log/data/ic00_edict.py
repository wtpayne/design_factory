# -*- coding: utf-8 -*-
"""
---

title:
    "Data logging stableflow-edict component."

description:
    "Data logging component."

id:
    "711d384c-d12f-4b9e-bd04-7f3d1875d2f4"

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


import fl.log.data
import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Data log persistence component coroutine.

    """

    set_key_all   = set(inputs.keys())
    set_key_ctrl  = set(('ctrl', ))
    set_key_event = set_key_all - set_key_ctrl

    writer = fl.log.data.writer(id_system   = runtime['id']['id_system'],
                                dirpath_log = cfg.get('dirpath_log', None))

    # Main loop.
    #
    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if not inputs['ctrl']['ena']:
            continue

        timestamp = inputs['ctrl']['ts']

        for key in set_key_event:
            packet = inputs[key]

            if not packet['ena']:
                continue

            for item in packet['list']:
                writer.send(item)
