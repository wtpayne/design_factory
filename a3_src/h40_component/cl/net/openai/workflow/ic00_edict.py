# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI client stableflow-edict component."

description:
    "This component enables integration with
    the OpenAI HTTP API."

id:
    "f7d19f59-cb0f-4a51-9c08-3bc5e653765e"

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


import fl.net.openai.client
import fl.util.edict
import key


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    OpenAI agent coroutine.

    """
    default_args = dict(id_endpoint = 'chat_completions',
                        model       = 'gpt-3.5-turbo')

    (_, _, workflow_handler) = init_openai_client(
                filepath_env  = cfg.get('filepath_env',  None),
                envvar_key    = cfg.get('envvar_key',    'OPENAI_API_KEY'),
                api_key       = cfg.get('api_key',       None),
                is_bit        = cfg.get('is_bit',        True),  # Builtin test
                is_async      = cfg.get('is_async',      False), # Asynchronous
                secs_interval = cfg.get('secs_interval', 2),
                default       = cfg.get('default',       default_args))

    timestamp     = dict()
    list_workflow = list()
    list_param    = list()
    list_result   = list()
    list_error    = list()

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        timestamp.clear()
        list_workflow.clear()
        list_param.clear()
        list_result.clear()
        list_error.clear()

        if inputs['workflow']['ena']:
            timestamp.update(inputs['workflow']['ts'])
            list_workflow = inputs['workflow']['list']

        if inputs['param']['ena']:
            timestamp.update(inputs['param']['ts'])
            list_param.extend(inputs['param']['list'])

        (list_result,
         list_error) = workflow_handler.send((list_workflow,
                                              list_param))

        if list_result:
            outputs['result']['ena'] = True
            outputs['result']['ts'].update(timestamp)
            outputs['result']['list'][:] = list_result

        if list_error:
            outputs['error']['ena'] = True
            outputs['error']['ts'].update(timestamp)
            outputs['error']['list'][:] = list_error


# -----------------------------------------------------------------------------
def init_openai_client(filepath_env  = None,
                       envvar_key    = 'OPENAI_API_KEY',
                       api_key       = None,
                       is_bit        = True,  # Built-in-test
                       is_async      = False, # Asynchronous API access.
                       secs_interval = 2,
                       default       = None):
    """
    Return initialized handler coroutines for the OpenAI client.

    """

    if api_key is None:
        api_key = key.load(id_value     = envvar_key,
                           filepath_env = filepath_env)

    cfg_handler = dict(api_key       = api_key,
                       secs_interval = secs_interval,
                       is_bit        = is_bit,
                       is_async      = is_async,
                       default       = default)

    request_handler  = fl.net.openai.client.coro_request_handler(
                                        cfg             = cfg_handler)

    template_handler = fl.net.openai.client.coro_template_handler(
                                        cfg             = cfg_handler,
                                        request_handler = request_handler)

    workflow_handler = fl.net.openai.client.coro_workflow_handler(
                                        cfg              = cfg_handler,
                                        request_handler  = request_handler,
                                        template_handler = template_handler)

    return (request_handler, template_handler, workflow_handler)
