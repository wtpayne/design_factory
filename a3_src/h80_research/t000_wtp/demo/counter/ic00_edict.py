# -*- coding: utf-8 -*-
"""
---

title:
    "Simple counter demo."

description:
    "Simple counter demo."

id:
    "e65a8382-495d-4eec-afaa-6a358c13b64b"

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


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine to assemble web resources from a graph of fragments.

    """

    # Initialize the inputs and outputs
    # that are owned by this component.
    #
    for key in outputs.keys():
        outputs[key]['ena']  = False
        outputs[key]['list'] = []

    # Signal is used to control the system
    # as a whole, stop it, restart it, etc.
    #
    signal = None

    while True:

        # Get the next set of inputs to
        # work on.
        # 
        inputs = yield (outputs, signal)

        # The enable flag on the control input
        # enables us to switch on and off
        # functionality without halting the
        # flow of data through the system.
        #
        if not inputs['ctrl']['ena']:
            continue

        idx_step = inputs['ctrl']['ts']['idx']
        print(f'COUNTER: {idx_step:03d}')
