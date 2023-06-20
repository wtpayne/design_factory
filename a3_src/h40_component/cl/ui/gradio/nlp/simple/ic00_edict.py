# -*- coding: utf-8 -*-
"""
---

title:
    "Gradio text input stableflow-edict component."

description:
    "Ultra simple UI for text processing tasks."

id:
    "c917c7be-064d-43b0-adfd-2a057834d51e"

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


import fl.ui.gradio.nlp.simple


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Gradio simple NLP task control UI coroutine.

    """

    ui = fl.ui.gradio.nlp.simple.coro_ui(cfg)

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        map_ts = dict()
        if inputs['ctrl']['ena']:
            map_ts = inputs['ctrl']['ts']

        # Grab incoming automatically generated data.
        #
        list_str_generated = list()
        if inputs['text']['ena']:
            list_str_generated = inputs['text']['list']

        # Communicate with the UI.
        #
        (list_str_user_input) = ui.send(list_str_generated)

        # Update outputs with outgoing user provided data.
        #
        if list_str_user_input:
            outputs['text']['ena'] = True
            outputs['text']['ts'].update(map_ts)
            outputs['text']['list'][:] = list_str_user_input
