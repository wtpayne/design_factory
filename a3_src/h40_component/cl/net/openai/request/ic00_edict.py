# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI client stableflow-edict component."

description:
    "This component enables integration with
    the OpenAI HTTP API."

id:
    "ea1d2286-0a0f-4cbf-b621-5f5ae205ab98"

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


import logging

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
    map_id    = runtime.get('id',       dict())
    id_system = map_id.get('id_system', None)
    id_node   = map_id.get('id_node',   None)

    (request_handler, _, _) = init_openai_client(
                filepath_env  = cfg.get('filepath_env',  None),
                envvar_key    = cfg.get('envvar_key',    'APIKEY_OPENAI'),
                api_key       = cfg.get('api_key',       None),
                is_bit        = cfg.get('is_bit',        True),  # Builtin test
                is_async      = cfg.get('is_async',      False), # Asynchronous
                secs_interval = cfg.get('secs_interval', 2),
                default       = cfg.get('default',       default_args),
                level_log     = cfg.get('level_log',     logging.INFO),
                id_system     = id_system,
                id_node       = id_node)

    # If there are one or more outputs which are
    # named after a message type, then we will
    # route messages of that type to the
    # corresponding output.
    #
    set_type_out = set((
                'log_event',      # Error messages and log messages.
                'log_metric',     # Quantitative metrics for KPIs etc...
                'log_data',       # Raw data for resimulation.
                'openai_result')) # Results from the OpenAI API.

    tup_key_in       = tuple(inputs.keys())
    tup_key_out      = tuple(outputs.keys())
    tup_key_msg_in   = tuple((k for k in tup_key_in  if k not in ('ctrl',)))
    tup_key_msg_out  = tuple((k for k in tup_key_out if k not in set_type_out))
    tup_key_type_out = tuple((k for k in tup_key_out if k in set_type_out))
    list_to_api      = list()
    list_from_api    = list()
    timestamp        = dict()
    signal           = fl.util.edict.init(outputs)

    while True:

        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Pass requests to the openai api.
        #
        for str_key in tup_key_msg_in:
            list_to_api.extend(inputs[str_key]['list'])

        # Recieve responses and
        # log messages from the
        # openai API.
        #
        list_from_api.clear()
        list_from_api[:] = request_handler.send(list_to_api)
        list_to_api.clear()
        if not list_from_api:
            continue

        # Route messages to type-specific
        # outputs.
        #
        list_msg     = list_from_api
        list_include = list()
        list_exclude = list()
        for key_type in tup_key_type_out:
            list_include.clear()
            list_exclude.clear()

            for msg in list_msg:
                if msg['type'] == key_type:
                    list_include.append(msg)
                else:
                    list_exclude.append(msg)

            if list_include:
                outputs[key_type]['ena'] = True
                outputs[key_type]['ts'].update(timestamp)
                outputs[key_type]['list'][:] = list_include

            if list_exclude:
                list_msg[:] = list_exclude
                continue
            else:
                break

        # If we have any remaining unrouted
        # output, then we copy that to every
        # other output channel.
        #
        if list_msg:
            for str_key in tup_key_msg_out:
                outputs[str_key]['ena'] = True
                outputs[str_key]['ts'].update(timestamp)
                outputs[str_key]['list'][:] = list_msg


# -----------------------------------------------------------------------------
def init_openai_client(filepath_env  = None,
                       envvar_key    = 'APIKEY_OPENAI',
                       api_key       = None,
                       is_bit        = True,  # Built-in-test
                       is_async      = False, # Asynchronous API access.
                       secs_interval = 2,
                       default       = None,
                       id_system     = None,
                       id_node       = None,
                       level_log     = None):
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
                       default       = default,
                       id_system     = id_system,
                       id_node       = id_node,
                       level_log     = level_log)

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
