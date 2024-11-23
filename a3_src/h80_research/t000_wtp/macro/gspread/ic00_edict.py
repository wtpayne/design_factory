# -*- coding: utf-8 -*-
"""
---

title:
    "Google spreadsheets integration."

description:
    "This module provides a generic integration with the Google spreadsheets
    API."

id:
    "de2a76e4-8a0a-40fb-82da-13480c172a31"

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
import typing

import gspread
import gspread_formatting
import pydantic


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Google sheets integration coroutine.

    """

    client = gspread.service_account_from_dict(dict(
        type                        = 'service_account',
        project_id                  = cfg['g_project_id'],
        private_key_id              = cfg['g_priv_key_id'],
        private_key                 = cfg['g_priv_key'].replace("\\n", "\n"),
        client_email                = cfg['g_cli_email'],
        client_id                   = cfg['g_cli_id'],
        auth_uri                    = cfg['g_auth_uri'],
        token_uri                   = cfg['g_token_uri'],
        auth_provider_x509_cert_url = cfg['g_prov_x509_url'],
        client_x509_cert_url        = cfg['g_cli_x509_url'],
        universe_domain             = cfg['g_univ_domain']))

    signal         = None
    id_spreadsheet = None
    spreadsheet    = None
    idx_worksheet  = None
    worksheet      = None

    for key in outputs:
        outputs[key]['ena']  = False
        outputs[key]['list'] = list()

    while True:

        inputs = yield (outputs, signal)
        for key in outputs:
            outputs[key]['ena'] = False
            outputs[key]['list'].clear()
        if not inputs['ctrl']['ena']:
            continue

        for key in inputs:
            if key in ('ctrl',):
                continue
            if not inputs[key]['ena']:
                continue

            for rpcdata in sorted(inputs[key]['list'], key = _sortkey_rpcdata):

                rpcdata = copy.deepcopy(rpcdata)

                try:
                    if rpcdata['id_spreadsheet'] != id_spreadsheet:
                        id_spreadsheet = rpcdata['id_spreadsheet']
                        spreadsheet = client.open_by_key(id_spreadsheet)
                except KeyError:
                    pass

                try:
                    if rpcdata['idx_worksheet'] != idx_worksheet:
                        idx_worksheet = rpcdata['idx_worksheet']
                        worksheet = spreadsheet.get_worksheet(idx_worksheet)
                except KeyError:
                    pass

                match rpcdata['id_api']:

                    case 'worksheet':
                        callable = getattr(worksheet, rpcdata['id_method'])
                        callable(*rpcdata['args'], **rpcdata['kwargs'])

                    case 'format-column-width':
                        gspread_formatting.set_column_width(
                            worksheet, *rpcdata['args'], **rpcdata['kwargs'])

        # TODO:- Listen for changes in the spreadsheet.
        #        This will require the insertion of an Apps Script
        #        function in the spreadsheet.

        # Outputs.
        # 
        for key in outputs:
            outputs[key]['ena'] = True
            outputs[key]['list'].extend([])


# -----------------------------------------------------------------------------
def _sortkey_rpcdata(item):
    """
    Sort key for a batch update specification.

    """

    return (item['id_spreadsheet'], 
            item['idx_worksheet'])


# =========================================================================
class WorksheetOperationSpec(pydantic.BaseModel):
    """
    Specification for a worksheet operation.

    """

    id_spreadsheet: str
    idx_worksheet:  int
    id_method:      str
    args:           list[typing.Any]
    kwargs:         dict[str, typing.Any]
