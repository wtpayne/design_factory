# -*- coding: utf-8 -*-
"""
---

title:
    "Epistematic data persistence stableflow-edict component."

description:
    "Epistematic data persistence component."

id:
    "5199ed68-0c42-4ab2-a656-e2ed391fb18f"

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
    Epistematic data persistence component coroutine.

    """

    tup_key_in      = tuple(inputs.keys())
    tup_key_out     = tuple(outputs.keys())
    tup_key_msg_in  = tuple((k for k in tup_key_in  if k not in ('ctrl',)))
    tup_key_msg_out = tuple((k for k in tup_key_out))
    list_fileinfo   = list()
    timestamp       = dict()

    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Process inputs
        #
        for str_key in tup_key_msg_in:
            if not inputs[str_key]['ena']:
                continue
            list_fileinfo.clear()
            list_fileinfo.extend(inputs[str_key]['list'])

        # Store in database
        #
        pass

        # Retrieve from database
        #
        pass

        if list_fileinfo:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(timestamp)
                outputs[id_out]['list'][:] = list_fileinfo
