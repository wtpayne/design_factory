# -*- coding: utf-8 -*-
"""
---

title:
    "Memoization cache component."

description:
    "This module documents the design of
    a stableflow-edict component which is
    intended to function as a memoization
    cache for a computationally expensive
    pipeline, allowing results to be cached
    to persistent storage (disk) and reducing
    the need to repeat time consuming and
    computationally expensive processing steps.

    We can't simply wrap a component pipeline
    in a memoization decorator as we can with
    a regular Python function, so to achieve
    the same effect in a dataflow/component
    oriented manner, we need to have a little
    feedback loop to send raw data to the
    component pipeline being memoized and
    then recieve any processed results back
    again so that they can be written to the
    cache.

    This component recieves raw data items
    from upstream components, and then checks
    to see if processed results exist in the
    cache for each of those raw data items.

    If a corresponding processed result data
    item is present in the cache, the cache
    item is sent downstream. Otherwise, the
    raw data item is output to the processing
    component or pipeline.

    Any processed data that is recieved is stored
    in the cache for future use.

    Processed data, whether retrieved from the
    cache or computed on-demand, is then
    handed off to downstream components.

    This component has the side effect of
    altering the order of data items, dependent
    on whether they are found in the cache or
    not, so it CAN affect the functional
    behaviour of the system if that functional
    behaviour is dependent on order-of-arrival
    of data items."

id:
    "5199ed68-0c42-4ab2-a656-e2ed391fb18f"

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


import sqlitedict

import fl.util.edict
import fl.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Data cache component coroutine.

    Raw data items come in from upsream
    components. We check the cache for
    the corresponding processed data items.
    If present, those items get sent
    downstream. If not present, the raw
    data items get sent for processing
    by the pipeline being memoized. Once
    they are recieved back again from
    the pipeline, they are stored in
    the cache and also sent downstream.

    """

    # Configure I/O identifier sets.
    #
    # tup_id_in_raw        - Incoming raw data from upstream components.
    # tup_id_out_raw       - Outgoing raw data to PIPELINE.
    # tup_id_in_processed  - Incoming processed data from PIPELINE.
    # tup_id_out_processed - Outgoing processed data to downstream components.
    # tup_id_in            - All configured component inputs
    # tup_id_out           - All configured component outputs.
    #
    tup_id_in_raw        = tuple(cfg.get('id_in_raw',        tuple()))
    tup_id_out_raw       = tuple(cfg.get('id_out_raw',       tuple()))
    tup_id_in_processed  = tuple(cfg.get('id_in_processed',  tuple()))
    tup_id_out_processed = tuple(cfg.get('id_out_processed', tuple()))

    tup_id_in  =  ('ctrl',)  # Control signal from system controller.
    tup_id_in  += tup_id_in_raw
    tup_id_in  += tup_id_in_processed

    tup_id_out =  tuple()
    tup_id_out += tup_id_out_raw
    tup_id_out += tup_id_out_processed

    # Sanity check.
    #
    assert tup_id_in  == tuple(inputs.keys())
    assert tup_id_out == tuple(outputs.keys())

    # Open a connection to the cache.
    #
    filepath_cache = cfg.get('filepath_cache_db')
    cache          = sqlitedict.SqliteDict(filepath_cache, autocommit = False)

    # Path to the unique ID used as the cache key.
    #
    str_path_uid = cfg.get('path_uid', 'uid')
    tup_path_uid = tuple(fl.util._iter_path(str_path_uid, delim = '.'))

    # Lists to accumulate raw and processed items.
    #
    timestamp           = dict()
    list_item_raw       = list() # List of raw data items.
    list_item_processed = list() # List of processed data items.

    # Main loop.
    #
    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Build a list of processed items that
        # have been pulled from the cache as well
        # as a list of items that were not found
        # in the cache and need to be processed.
        #
        # list_item_processed - Retrieved from the cache.
        # list_item_raw       - Not found in cache.
        #
        list_item_processed.clear()
        list_item_raw.clear()

        for id_in_raw in tup_id_in_raw:
            pkt_in_raw = inputs[id_in_raw]
            if not pkt_in_raw['ena']:
                continue

            # Try to retrieve processed data
            # items from the cache.
            #
            for item_raw in pkt_in_raw['list']:
                uid = _get(item_raw, tup_path_uid)
                try:
                    item_processed = cache[uid]
                except KeyError:
                    list_item_raw.append(item_raw)
                else:
                    list_item_processed.append(item_processed)

        # Cache processed data items, trimming things like
        # page images and OCR model weights.
        #
        for id_in_processed in tup_id_in_processed:
            if not inputs[id_in_processed]['ena']:
                continue
            for fileinfo_ocr in inputs[id_in_processed]['list']:
                uid        = _get(fileinfo_ocr, tup_path_uid)
                cache[uid] = fileinfo_ocr
                list_item_processed.append(fileinfo_ocr)
            cache.commit()

        # Send raw items for prcessing.
        #
        if list_item_raw:
            for id_out_raw in tup_id_out_raw:
                outputs[id_out_raw]['ena'] = True
                outputs[id_out_raw]['ts'].update(timestamp)
                outputs[id_out_raw]['list'][:] = list_item_raw

        # Send processed items downstream.
        #
        if list_item_processed:
            for id_out_processed in tup_id_out_processed:
                outputs[id_out_processed]['ena'] = True
                outputs[id_out_processed]['ts'].update(timestamp)
                outputs[id_out_processed]['list'][:] = list_item_processed


# -----------------------------------------------------------------------------
def _get(item, tup_key):
    """
    Get the item at the specified path.

    """

    cursor = item
    for name in tup_key:
        cursor = cursor[name]
    return cursor
