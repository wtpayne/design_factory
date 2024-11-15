# -*- coding: utf-8 -*-
"""
---

title:
    "File resource support."

description:
    "File resource support."

id:
    "6a06e8c5-51fa-4584-bab8-a8b921862bd5"

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


import os.path

import fl.ui.web.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine to serve file based resources.

    """

    # Initialize outputs.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    # Initialize state.
    #
    state['list'] = list()
    for cfg_item in cfg['list']:
        state_item = dict()
        state_item.update(cfg_item)
        state_item['last_modified'] = 0
        state['list'].append(state_item)

    signal = None
    while True:

        inputs = yield (outputs, signal)

        if not inputs['ctrl']['ena']:
            continue

        map_ts  = inputs['ctrl']['ts']
        map_res = fl.ui.web.util.ResMap()
        for state_item in state['list']:

            # If the file has been modified,
            # output an updated version of
            # the resource.
            #
            mtime      = os.path.getmtime(state_item['filepath'])
            is_changed = mtime > state_item['last_modified']
            if is_changed:
                state_item['last_modified'] = mtime
                media_type  = state_item['media_type']
                id_resource = state_item['id_resource']
                content     = _read_item_content(state_item)
                kwargs      = {'media_type': media_type, id_resource: content}
                map_res.add(**kwargs)

        if map_res:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'].append(dict(map_res))


# -----------------------------------------------------------------------------
def _read_item_content(state_item):
    """
    Read the file and return its contents.

    """
    if state_item['is_binary']:
        mode_file = 'rb'
    else:
        mode_file = 'rt'
    with open(state_item['filepath'], mode_file) as file:
        data = file.read()
    return data
