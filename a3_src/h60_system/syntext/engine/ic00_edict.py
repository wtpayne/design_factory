# -*- coding: utf-8 -*-
"""
---

title:
    "Syntext synthetic text generation engine component."

description:
    "Syntext synthetic text generation engine."

id:
    "336ab2f3-170c-44ff-8904-bbc1d82db962"

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

import fl.net.openai.client


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Noop component coroutine.

    """

    # SETUP ...........

    cfg = dict() # ....
    coro = fl.net.openai.client.coro_request_handler(cfg)

    signal = None
    fl.util.edict.init(outputs)

    while True:

        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # FUNCTIONALITY .........
        result = coro.send (prompt)

        outputs['text']['ena'] = True
        outputs['text']['list'] = list()
        outputs['text']['list'].append('foo')
        outputs['text']['list'].append('bar')
