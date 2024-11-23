# -*- coding: utf-8 -*-
"""
---

title:
    "Synthetic data to gspread adapter."

description:
    "This module formats synthetic data appropriately for the gspread node."

id:
    "82e1d0d3-2ea8-4bf0-8831-d0ba73a32793"

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


# https://docs.google.com/spreadsheets/d/1bfUefa-0cMIzGkxsMXhlJGKZo1ZxWKo1KTl_y5AoMBk/edit?gid=0#gid=0
# https://github.com/robin900/gspread-formatting
# https://docs.gspread.org/en/v6.1.3/


import os
import json
import uuid

import gspread.utils
import google.auth
import google_auth_oauthlib.flow
import googleapiclient.discovery


google_auth_oauthlib.flow.InstalledAppFlow
googleapiclient.discovery.build


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Synthetic data to gspread adapter coroutine.

    """

    signal = None

    for key in outputs:
        outputs[key]['ena']  = False
        outputs[key]['list'] = list()

    ord_row_lo = 1
    ord_col_lo = 1

    id_spreadsheet = '1bfUefa-0cMIzGkxsMXhlJGKZo1ZxWKo1KTl_y5AoMBk'
    idx_worksheet  = 0

    map_cache = dict()

    while True:

        # Check if the node is enabled on this step.
        #
        inputs = yield (outputs, signal)
        for key in outputs:
            outputs[key]['ena'] = False
            outputs[key]['list'].clear()
        if not inputs['ctrl']['ena']:
            continue

        # Collect all input data together into one list.
        #
        list_synth = list()
        for key in inputs:
            if key in ('ctrl',):
                continue
            if not inputs[key]['ena']:
                continue
            list_synth.extend(inputs[key]['list'])

        # Update the cache.
        #
        map_synth = {
            uuid.uuid4().hex: [synth['output']] for synth in list_synth}
        map_cache.update(map_synth)

        # Get RPC data for the gspread and gspread-formatting APIs.
        #
        list_rpcdata = _list_rpcdata(id_spreadsheet,
                                     idx_worksheet,
                                     map_synth,
                                     ord_row_lo,
                                     ord_col_lo)
        if not list_rpcdata:
            continue

        # Outputs.
        #
        for key in outputs:
            outputs[key]['ena'] = True
            outputs[key]['list'].extend(list_rpcdata)


# -----------------------------------------------------------------------------
def _list_rpcdata(id_spreadsheet,
                  idx_worksheet,
                  map_synth,
                  ord_row_lo,
                  ord_col_lo):
    """
    Return a list of RPC data for the gspread and gspread-formatting APIs.

    """

    count_cols  = len(next(iter(map_synth.values()))) + 1
    count_synth = len(map_synth)
    ord_row_hi  = ord_row_lo + (count_synth - 1)
    ord_col_hi  = ord_col_lo + (count_cols - 1)
    a1_cell_lo  = gspread.utils.rowcol_to_a1(ord_row_lo, ord_col_lo)
    a1_cell_hi  = gspread.utils.rowcol_to_a1(ord_row_hi, ord_col_hi)
    a1_range    = f"{a1_cell_lo}:{a1_cell_hi}"
    ord_row_lo  = ord_row_hi + 1

    list_row = list()
    for (key_synth, list_items) in map_synth.items():
        row = [key_synth] + list_items
        list_row.append(row)

    list_spec    = [dict(range = a1_range, values = list_row )]
    list_args    = [list_spec]

    list_rpcdata = [
        dict(id_api         = 'worksheet',
             id_spreadsheet = id_spreadsheet,
             idx_worksheet  = idx_worksheet,
             id_method      = 'batch_update',
             args           = list_args,
             kwargs         = {})]

    list_rpcdata.extend([
        dict(id_api         = 'format-column-width',
             id_spreadsheet = id_spreadsheet,
             idx_worksheet  = idx_worksheet,
             args           = ['A', 200],
             kwargs         = {}),
        dict(id_api         = 'format-column-width',
             id_spreadsheet = id_spreadsheet,
             idx_worksheet  = idx_worksheet,
             args           = ['B', 400],
             kwargs         = {}),
        dict(id_api         = 'format-column-width',
             id_spreadsheet = id_spreadsheet,
             idx_worksheet  = idx_worksheet,
             args           = ['C', 200],
             kwargs         = {})])

    return list_rpcdata
