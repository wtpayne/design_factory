# -*- coding: utf-8 -*-
"""
---

title:
    "dm014_macro demo commands."

description:
    "This module defines commands for the
    dm014_macro demonstration."

id:
    "4ac71a47-af96-4096-9338-aa18bab95d20"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2024 William Payne"

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


"""


import os.path
import sys



# -----------------------------------------------------------------------------
def start():
    """
    Start the dm014 macro system.

    """

    import da.env.run
    import key

    tup_overrides = (
        'node.synth.config.filepath_cache',      _filepath_cache('synth'),
        'node.synth.config.apikey_model',        key.load('APIKEY_GROQ_DEV'),
        'node.gspread.config.g_project_id',      key.load('GOOGLE_PROJECT_ID'),
        'node.gspread.config.g_priv_key_id',     key.load('GOOGLE_PRIVATE_KEY_ID'),
        'node.gspread.config.g_priv_key',        key.load('GOOGLE_PRIVATE_KEY'),
        'node.gspread.config.g_cli_email',       key.load('GOOGLE_CLIENT_EMAIL'),
        'node.gspread.config.g_cli_id',          key.load('GOOGLE_CLIENT_ID'),
        'node.gspread.config.g_auth_uri',        key.load('GOOGLE_AUTH_URI'),
        'node.gspread.config.g_token_uri',       key.load('GOOGLE_TOKEN_URI'),
        'node.gspread.config.g_prov_x509_url',   key.load('GOOGLE_AUTH_PROVIDER_X509_CERT_URL'),
        'node.gspread.config.g_cli_x509_url',    key.load('GOOGLE_CLIENT_X509_CERT_URL'),
        'node.gspread.config.g_univ_domain',     key.load('GOOGLE_UNIVERSE_DOMAIN'),
        'node.continuity.config.filepath_cache', _filepath_cache('continuity'),
        'node.continuity.config.apikey_model',   key.load('APIKEY_GROQ_DEV'),
        'node.static.config.list.0.filepath',    _static('htmx/v2.0.3/htmx.js'),
        'node.static.config.list.1.filepath',    _static('htmx/v2.0.3/htmx.min.js'),
        'node.static.config.list.2.filepath',    _static('htmx-ext-sse/v2.2.2/sse.js'),
        'node.static.config.list.3.filepath',    _static('htmx-ext-sse/v2.2.2/sse.min.js'))
    sys.exit(da.env.run.stableflow_start(path_cfg      = _filepath_cfg(),
                                         tup_overrides = tup_overrides))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop the dm014 macro system.

    """

    import da.env.run
    sys.exit(da.env.run.stableflow_stop(path_cfg = _filepath_cfg()))


# -----------------------------------------------------------------------------
def _static(relpath_file):
    """
    Return the filepath to a static HTMX resource.

    """

    return _macropath('static', relpath_file)


# -----------------------------------------------------------------------------
def _filepath_cfg():
    """
    Return the filepath to the backend server stableflow configuration file.

    """

    return _macropath('macro.stableflow.cfg.yaml')



# -----------------------------------------------------------------------------
def _filepath_cache(id_node):
    """
    Return the filepath to the cache database.

    """

    return _macropath(f'{id_node}.cache.sqlite', is_tmp = True)


# -----------------------------------------------------------------------------
def _macropath(*args, is_tmp = False):
    """
    Return a path in the macro workspace.

    """

    import da.env

    if is_tmp:
        process_area = 'a4_tmp'
    else:
        process_area = 'a3_src'

    dirpath_macro = da.env.path(process_area = process_area,
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/macro')

    return os.path.join(dirpath_macro, *args)

