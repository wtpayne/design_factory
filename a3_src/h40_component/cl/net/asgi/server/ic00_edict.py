# -*- coding: utf-8 -*-
"""
---

title:
    "ASGI server stableflow-edict component."

description:
    "This stableflow component is designed to
    support the use of an embedded ASGI server
    to serve web resources and provide simple
    HTTP APIs."

id:
    "d26eb7b1-6048-4dc7-9e45-306b2f5a9ce8"

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

import fl.net.asgi.server
import fl.util.edict
import key


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    ASGI server coroutine.

    """

    fl.util.edict.validate(inputs = inputs,  must_contain = ('ctrl',))

    filepath_env      = cfg.get('filepath_env',       None)
    key_sessionsecret = cfg.get('key_sessionsecret',  'HTTP_SESSION_SECRET')
    sessionsecret     = cfg.get('sessionsecret',      None)
    host              = cfg.get('host',               '0.0.0.0')
    port              = cfg.get('port',               8080)
    debug             = cfg.get('debug',              False)
    log_level         = cfg.get('log_level',          'WARNING')
    ssl_keyfile       = cfg.get('ssl_keyfile',        None)
    ssl_certfile      = cfg.get('ssl_certfile',       None)
    map_id            = runtime.get('id',             dict())
    id_system         = map_id.get('id_system',       None)
    id_node           = map_id.get('id_node',         None)

    if isinstance(log_level, str):
        log_level = logging.getLevelName(log_level.upper())

    if sessionsecret is None:
        sessionsecret = key.load(id_value     = key_sessionsecret,
                                 filepath_env = filepath_env)

    server = fl.net.asgi.server.coro(cfg = dict(host          = host,
                                                port          = port,
                                                debug         = debug,
                                                sessionsecret = sessionsecret,
                                                log_level     = log_level,
                                                ssl_keyfile   = ssl_keyfile,
                                                ssl_certfile  = ssl_certfile,
                                                id_system     = id_system,
                                                id_node       = id_node))

    # If there are one or more outputs which are
    # named after a message type, then we will
    # route messages of that type to the
    # corresponding output.
    #
    set_type_out = set((
                'log_event',  # Error messages and log messages.
                'log_metric', # Quantitative metrics for KPIs etc...
                'log_data',   # Raw data for resimulation.
                'request'))   # Requests from frontend clients.

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
        unix_time = timestamp['unix_time']

        # Pass resources to the ASGI server.
        #
        for str_key in tup_key_msg_in:
            list_to_api.extend(inputs[str_key]['list'])

        # Recieve responses and
        # log messages from the
        # ASGI server.
        #
        list_from_api.clear()
        list_from_api[:] = server.send((list_to_api, unix_time))
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