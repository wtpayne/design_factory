# -*- coding: utf-8 -*-
"""
---

title:
    "ACE text simplification stableflow-edict component."

description:
    "This component simplifies text to the
    Attempto Controlled English constrained
    natural language."

id:
    "276555b5-98a5-400e-a547-e978b80a2661"

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


import os
import textwrap

import dotenv

import cl.net.openai.client.ic00_edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    ACE text simplification agent coroutine.

    """

    default_args = dict(id_endpoint = 'chat_completions',
                        model       = 'gpt-3.5-turbo')

    (request_handler,
     template_handler,
     workflow_handler) = cl.net.openai.client.ic00_edict.init_handlers(
                filepath_env  = cfg['filepath_env'],
                envvar_key    = cfg.get('envvar_key',    'OPENAI_API_KEY'),
                is_bit        = cfg.get('is_bit',        True),  # Builtin test
                is_async      = cfg.get('is_async',      False), # Asynchronous
                secs_interval = cfg.get('secs_interval', 2),
                default       = cfg.get('default',       default_args))

    str_template = textwrap.dedent("""
        Please simplify the following engineering process document excerpt from
        unconstrained English to Attempto Controlled English (ACE). Make sure
        the simplified text is clear, concise, and retains the original meaning.

        Excerpt:

        "{text}"

        Simplified Text (ACE):

        """)

    map_template = {
        'id_endpoint':      'chat_completions',
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     'rpa-etl-simplify',     # Process step.
        'uid_variant':      '1.0.0',                # Improvement.
        'uid_workflow':     'rpa-etl-simplify',     # Process id.
        'kwargs_req':       {'model':           'gpt-3.5-turbo-0301'},
        'messages':         [{'role':           'user',
                              'content':        str_template}] }

    (_, _) = template_handler.send(([map_template], []))

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

        # Grab any new text inputs.
        #
        map_ts       = dict()
        list_text_in = list()
        if inputs['text']['ena']:
            map_ts       = inputs['text']['ts']
            list_text_in = inputs['text']['list']

        # Pack params.
        #
        list_param = list()
        for text_in in list_text_in:
            list_param.append({
                'type':             {'id': 'prompt_params', 'ver': '1.0'},
                'uid_params':       'rpa-etl-simplify',
                'uid_template':     'rpa-etl-simplify',
                'uid_workflow':     'rpa-etl-simplify',
                'kwargs_tmpl':      dict(text = text_in), # <-- For template
                'kwargs_req':       dict(),               # <-- For OAI request
                'state':            dict()})              # <-- Process state

        (list_result,
         list_error) = template_handler.send(([], list_param))

        if list_result:
            import pprint
            pprint.pprint(list_result)

        # Unpack result.
        #
        list_text_out = list()
        for result in list_result:
            list_choices = result['response']['choices']
            str_content  = list_choices[0]['message']['content']
            list_text_out.append(str_content)

        # Update error-reporting outputs.
        #
        if list_text_out:
            outputs['text']['ena'] = True
            outputs['text']['ts'].update(map_ts)
            outputs['text']['list'][:] = list_text_out
