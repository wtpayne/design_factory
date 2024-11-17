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
        'node.static.config.list.0.filepath', _static('htmx/v2.0.3/htmx.js'),
        'node.static.config.list.1.filepath', _static('htmx/v2.0.3/htmx.min.js'),
        'node.static.config.list.2.filepath', _static('htmx-ext-sse/v2.2.2/sse.js'),
        'node.static.config.list.3.filepath', _static('htmx-ext-sse/v2.2.2/sse.min.js'),
        'node.synth.config.apikey_groq',      key.load('GROQ_API_KEY'),
        'node.continuity.config.apikey_groq', key.load('GROQ_API_KEY'))

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

    return os.path.join(_dirpath_static(), relpath_file)


# -----------------------------------------------------------------------------
def _dirpath_static():
    """
    Return the directory path to the static web resources directory.

    """

    import da.env
    return da.env.path(process_area = 'a3_src',
                       control_tier = 'h80_research',
                       relpath      = 't000_wtp/macro/static')


# -----------------------------------------------------------------------------
def _filepath_cfg():
    """
    Return the filepath to the backend server stableflow configuration file.

    """

    import da.env

    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h80_research',
                relpath      = 't000_wtp/macro/macro.stableflow.cfg.yaml')

