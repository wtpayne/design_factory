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


import uuid

import gspread.utils


# https://github.com/robin900/gspread-formatting
# https://docs.gspread.org/en/v6.1.3/

# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Synthetic data to gspread adapter coroutine.

    """

    signal = None

    for key in outputs:
        outputs[key]['ena']  = False
        outputs[key]['list'] = list()

    ord_col_lo = 1
    ord_row_lo = 1

    id_spreadsheet = '1bfUefa-0cMIzGkxsMXhlJGKZo1ZxWKo1KTl_y5AoMBk'
    idx_worksheet  = 0

    map_key = dict(output = 'synth')

    count_cols = 2

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
        list_input = list()
        for key in inputs:
            if key in ('ctrl',):
                continue
            if not inputs[key]['ena']:
                continue
            list_input.extend(inputs[key]['list'])

        # TODO: Add a uuid for each row and store in a database.
        # 

        # Format synthetic data for gspread.
        # 
        count_items = len(list_input)
        ord_row_hi  = ord_row_lo + (count_items - 1)
        ord_col_hi  = ord_col_lo + (count_cols - 1)
        a1_cell_lo  = gspread.utils.rowcol_to_a1(ord_row_lo, ord_col_lo)
        a1_cell_hi  = gspread.utils.rowcol_to_a1(ord_row_hi, ord_col_hi)
        a1_range    = f"{a1_cell_lo}:{a1_cell_hi}"
        ord_row_lo  = ord_row_hi + 1

        list_row     = [_build_row(item) for item in list_input]
        list_spec    = [dict(range  = a1_range, values = list_row )]
        list_rpcdata = [
            dict(id_api         = 'worksheet',
                 id_spreadsheet = id_spreadsheet,
                 idx_worksheet  = idx_worksheet,
                 id_method      = 'batch_update',
                 args           = [list_spec],
                 kwargs         = {})]

        list_rpcdata.append(
            dict(id_api         = 'format-column-width',
                 id_spreadsheet = id_spreadsheet,
                 idx_worksheet  = idx_worksheet,
                 args           = ['A', 200],
                 kwargs         = {}))

        list_rpcdata.append(
            dict(id_api         = 'format-column-width',
                 id_spreadsheet = id_spreadsheet,
                 idx_worksheet  = idx_worksheet,
                 args           = ['B', 400],
                 kwargs         = {}))

        list_rpcdata.append(
            dict(id_api         = 'format-column-width',
                 id_spreadsheet = id_spreadsheet,
                 idx_worksheet  = idx_worksheet,
                 args           = ['C', 200],
                 kwargs         = {}))

        # Outputs.
        # 
        if list_rpcdata:
            for key in outputs:
                outputs[key]['ena'] = True
                outputs[key]['list'].extend(list_rpcdata)


# -----------------------------------------------------------------------------
def _build_row(item_input):
    """
    Build a row of cells from a synthetic data item.

    """

    key_row    = uuid.uuid4().hex
    spec_synth = item_input['output']

    return [key_row, spec_synth]