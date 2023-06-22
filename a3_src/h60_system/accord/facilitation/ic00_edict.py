# -*- coding: utf-8 -*-
"""
---

title:
    "Accprd app command handler for the question command."

description:
    "Handle invocations of the question command."

id:
    "c3c64fce-acd3-4477-8686-45cdaf699e20"

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
    Noop component coroutine.

    """

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if inputs['cmd']['ena']:
            for cmd in inputs['cmd']['list']:
                id_cmd = cmd['name_command']

                if id_cmd == 'ask':
                    question                  = ' '.join(cmd['args'])
                    outputs['msg']['ena']     = True
                    outputs['msg']['list'][:] = [
                                        (1115744295845118032, question),
                                        (1115744329131106325, question),
                                        (1115744378623893675, question),
                                        (1115744396005097592, question),
                                        (1115744413751185570, question)]

