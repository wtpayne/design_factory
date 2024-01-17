# -*- coding: utf-8 -*-
"""
---

title:
    "PDF reading stableflow-edict component."

description:
    "Nougat OCR component."

id:
    "f9e8cbab-5341-4d03-9f1e-e6945340508c"

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
    Nougat OCR stableflow-edict component coroutine.

    """

    tup_id_in      = tuple(inputs.keys())
    tup_id_out     = tuple(outputs.keys())
    tup_id_msg_in  = tuple((k for k in tup_id_in  if k not in ('ctrl',)))

    list_processed = list()
    timestamp      = dict()
    signal         = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Extract text from all pages from all inputs.
        #
        list_processed.clear()
        for str_key in tup_id_msg_in:

            if not inputs[str_key]['ena']:
                continue

            for fileinfo in inputs[str_key]['list']:



                fileinfo['mmd'] = '\n\n'.join(list_mmd)
                list_processed.append(fileinfo)

        # If we have any processed documents,
        # output them.
        #
        if list_processed:
            for str_key in tup_id_out:
                outputs[str_key]['ena'] = True
                outputs[str_key]['ts'].update(timestamp)
                outputs[str_key]['list'][:] = list_processed
