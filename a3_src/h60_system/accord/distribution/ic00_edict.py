# -*- coding: utf-8 -*-
"""
---

title:
    "Discord summary distribution component."

description:
    "Formats summary messages."

id:
    "04fff1bb-ea23-4dc7-a49e-ee3d49415eac"

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
    Distribution component coroutine.

    """

    id_channel_admin     = 1115744080907997204
    id_channel_room_01   = 1115744295845118032
    id_channel_room_02   = 1115744329131106325
    id_channel_room_03   = 1115744378623893675
    id_channel_room_04   = 1115744396005097592
    id_channel_room_05   = 1115744413751185570
    set_channel_broacast = { id_channel_admin,
                             id_channel_room_01,
                             id_channel_room_02,
                             id_channel_room_03,
                             id_channel_room_04,
                             id_channel_room_05 }

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if not inputs['result']['ena']:
            continue

        timestamp = inputs['result']['ts']

        for item in inputs['result']['list']:

            list_response_choices = item['response']['choices']
            if not list_response_choices:
                continue

            content = list_response_choices[0]['message']['content']
            if not content:
                continue

            outputs['msg']['ena']  = True
            outputs['msg']['ts']   = timestamp
            for id_channel in sorted(set_channel_broacast):
                outputs['msg']['list'].append((id_channel, content))
