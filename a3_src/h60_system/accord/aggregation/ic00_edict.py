# -*- coding: utf-8 -*-
"""
---

title:
    "Discord message aggregation component."

description:
    "Aggregates messages."

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
import key

import fl.net.openai.client


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Noop component coroutine.

    """

    list_request    = list()
    list_transcript = list()

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if inputs['msg']['ena']:
            list_transcript.extend(inputs['msg']['list'])

        list_request.clear()
        if inputs['cmd']['ena']:
            timestamp = inputs['cmd']['ts']
            for cmd in inputs['cmd']['list']:
                id_cmd = cmd['name_command']

                print('COMMAND: ' + id_cmd)

                if id_cmd == 'summarize':
                    list_request.append({
                        'model':       'gpt-3.5-turbo',
                        'messages':    [{
                            'role':    'system',
                            'content': 'Tell me a limerick about algorithms and decision support systems.'}]})

        if list_request:
            outputs['request']['ena'] = True
            outputs['request']['ts'].update(timestamp)
            outputs['request']['list'][:] = list_request
