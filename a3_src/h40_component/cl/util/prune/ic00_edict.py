# -*- coding: utf-8 -*-
"""
---

title:
    "Data item pruning component."

description:
    "Remove unwanted fields from each data item
    in the batch."

id:
    "3aed1bdd-a339-4cbe-9c50-ee30fe31a520"

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


import copy
import functools

import fl.util
import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Pruning component coroutine.

    """

    tup_tup_key_prune = _configure(cfg)
    tup_id_in         = tuple(inputs.keys())
    tup_id_out        = tuple(outputs.keys())
    tup_id_msg_in     = tuple((k for k in tup_id_in if k not in ('ctrl',)))

    list_pruned = list()
    timestamp   = dict()
    signal      = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Prune specified fields from data items.
        #
        list_pruned.clear()
        for id_in in tup_id_msg_in:
            pkt_in = inputs[id_in]
            if pkt_in['ena']:
                timestamp.update(pkt_in['ts'])
                for item in pkt_in['list']:
                    list_pruned.append(_prune(item, tup_tup_key_prune))

        # Output pruned data.
        #
        if list_pruned:
            for id_out in tup_id_out:
                pkt_out = outputs[id_out]
                pkt_out['ena'] = True
                pkt_out['ts'].update(timestamp)
                pkt_out['list'][:] = list_pruned


# -----------------------------------------------------------------------------
def _configure(cfg):
    """
    Read and validate configuration.

    """

    configdata = cfg.get('path_prune', list())
    if isinstance(configdata, str):
        list_path_prune = [configdata]
    elif isinstance(configdata, list):
        list_path_prune = configdata
    else:
        raise RuntimeError('Bad config value for key_prune')

    _iter = functools.partial(fl.util._iter_path, delim = '.')
    return tuple(tuple(_iter(path)) for path in list_path_prune)


# -----------------------------------------------------------------------------
def _prune(map_in, tup_tup_key_prune):
    """
    Remove the specified fields from the provided dict.

    """

    map_out = copy.deepcopy(map_in)

    for tup_key_prune in tup_tup_key_prune:
        cursor = map_out

        for key_prune in tup_key_prune[:-1]:
            cursor = cursor[key_prune]

        key_prune = tup_key_prune[-1]
        try:
            del cursor[key_prune]
        except KeyError:
            pass

    return map_out