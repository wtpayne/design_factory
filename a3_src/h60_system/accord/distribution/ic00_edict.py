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

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if not inputs['result']['ena']:
            continue

        timestamp = inputs['result']['ts']
        list_msg  = list()
        for item in inputs['result']['list']:

            list_response_choices = item['response']['choices']
            if not list_response_choices:
                continue

            content = list_response_choices[0]['message']['content']
            if not content:
                continue

            # Send a message with the summary in to the channel.
            #
            list_msg.append(dict(type       = 'msg',
                                 id_channel = item['state']['id_channel'],
                                 content    = content))

            # Send a message with the summary in to each user.
            #
            for id_user in item['state']['list_id_user']:
                list_msg.append(dict(type    = 'dm',
                                     id_user = id_user,
                                     content = content))

        outputs['msg']['ena']     = True
        outputs['msg']['ts']      = timestamp
        outputs['msg']['list'][:] = list_msg
