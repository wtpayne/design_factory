# -*- coding: utf-8 -*-
"""
---

title:
    "Nougat OCR stableflow-edict component."

description:
    "Nougat OCR component."

id:
    "6095efad-a54d-4888-b29a-c7e257f79828"

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


import fl.io.ocr.nougat
import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Nougat OCR stableflow-edict component coroutine.

    """

    ocr             = fl.io.ocr.nougat.coro()
    tup_key_in      = tuple(inputs.keys())
    tup_key_out     = tuple(outputs.keys())
    tup_key_msg_in  = tuple((k for k in tup_key_in  if k not in ('ctrl',)))
    tup_key_msg_out = tuple((k for k in tup_key_out))
    list_processed  = list()
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

        # OCR all pages from all inputs.
        #
        list_processed.clear()
        for str_key in tup_key_msg_in:

            if not inputs[str_key]['ena']:
                continue

            for fileinfo in inputs[str_key]['list']:
                for pageinfo in fileinfo['list_pageinfo']:
                    pageinfo.update(ocr.send(pageinfo['pil_image']))
                list_processed.append(fileinfo)

        # If we have any processed documents,
        # output them.
        #
        if list_processed:
            for str_key in tup_key_msg_out:
                outputs[str_key]['ena'] = True
                outputs[str_key]['ts'].update(timestamp)
                outputs[str_key]['list'][:] = list_processed
