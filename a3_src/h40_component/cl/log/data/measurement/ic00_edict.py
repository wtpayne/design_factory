# -*- coding: utf-8 -*-
"""
---

title:
    "Data logging measurement stableflow-edict component."

description:
    "Measurement component. Performs measurement for datalogging."

id:
    "451f261a-63f7-4cf4-bcb7-ed5eff5bb35c"

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


import copy

import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Noop component coroutine.

    """

    set_key_in         = set(inputs.keys())
    set_key_out        = set(outputs.keys())
    set_key_in_and_out = set_key_out & set_key_in
    set_key_out_only   = set_key_out - set_key_in
    tup_key_in_and_out = tuple(sorted(set_key_in_and_out))
    tup_key_out_only   = tuple(sorted(set_key_out_only))
    signal             = fl.util.edict.init(outputs)

    while True:

        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        map_measurement = dict()
        for id_key in tup_key_in_and_out:
            item = copy.deepcopy(inputs[id_key])
            outputs[id_key].update(item)
            if item['ena']:
                map_measurement[id_key] = item

        if map_measurement:
            for id_key in tup_key_out_only:
                outputs[id_key]['ena']     = True
                outputs[id_key]['list'][:] = [map_measurement]
