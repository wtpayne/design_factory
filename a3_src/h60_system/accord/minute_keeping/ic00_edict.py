# -*- coding: utf-8 -*-
"""
---

title:
    "Accprd app minute taking task component."

description:
    "Handle invocations of the summary command."

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
    default_args  = dict(id_endpoint = 'chat_completions',
                         model       = 'gpt-3.5-turbo')
    filepath_env  = cfg.get('filepath_env',  None)
    envvar_key    = cfg.get('envvar_key',    'OPENAI_API_KEY')
    api_key       = cfg.get('api_key',       None)
    is_bit        = cfg.get('is_bit',        True)   # Builtin test
    is_async      = cfg.get('is_async',      False)  # Asynchronous
    secs_interval = cfg.get('secs_interval', 2)
    default       = cfg.get('default',       default_args)

    if api_key is None:
        api_key = key.load(id_value     = envvar_key,
                           filepath_env = filepath_env)

    cfg_handler = dict(api_key       = api_key,
                       secs_interval = secs_interval,
                       is_bit        = is_bit,
                       is_async      = is_async,
                       default       = default)

    request_handler  = fl.net.openai.client.coro_request_handler(
                                                            cfg = cfg_handler)

    list_transcript = list()
    list_summary    = list()

    list_result     = list()
    list_error      = list()
    list_request    = list()

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        list_result.clear()
        list_error.clear()
        (list_result, list_error) = request_handler.send(list_request)
        list_request.clear()

        if list_result:
            for item in list_result:
                list_choices = item['response']['choices']
                if not list_choices:
                    continue
                first_choice = list_choices[0]
                content      = first_choice['message']['content']
                if content:
                    outputs['msg']['ena']     = True
                    outputs['msg']['list'][:] = [
                                        (1115744080907997204, content)]

        if inputs['msg']['ena']:
            list_transcript.extend(inputs['msg']['list'])

        if inputs['cmd']['ena']:
            for cmd in inputs['cmd']['list']:
                id_cmd = cmd['name_command']

                if id_cmd == 'debug':
                    list_request.append({
                        'model':       'gpt-3.5-turbo',
                        'messages':    [{
                            'role':    'system',
                            'content': 'Tell me a limerick.'}]})

                    # str_debug = 'DEBUG'
                    # outputs['msg']['ena']     = True
                    # outputs['msg']['list'][:] = [
                    #                     (1115744080907997204, str_debug)]

                if id_cmd == 'summarize':
                    summary                   = 'SUMMARY'
                    outputs['msg']['ena']     = True
                    outputs['msg']['list'][:] = [
                                        (1115744295845118032, summary),
                                        (1115744329131106325, summary),
                                        (1115744378623893675, summary),
                                        (1115744396005097592, summary),
                                        (1115744413751185570, summary)]

# chair:      1115744080907997204
# room_01:    1115744295845118032
# room_02:    1115744329131106325
# room_03:    1115744378623893675
# room_04:    1115744396005097592
# room_05:    1115744413751185570
