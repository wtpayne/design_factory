# -*- coding: utf-8 -*-
"""
---

title:
    "dm007_northstar demo commands."

description:
    "This module defines commands for the
    dm007_northstar demonstration."

id:
    "e556bc3f-0824-478b-ac2b-f8a8491b6e6c"

type:
    dt003_python_module

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


"""


import getpass
import os
import sys


# -----------------------------------------------------------------------------
def start():
    """
    Start an instance of the dm007 system.

    """

    import da.env.run
    sys.exit(da.env.run.stableflow_start(
                                path_cfg      = _filepath_cfg(),
                                is_local      = False,
                                tup_overrides = _overrides(stage = 'DEV')))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop any running instances of the dm006 system.

    """

    import da.env.run
    sys.exit(da.env.run.stableflow_stop(
                                path_cfg      = _filepath_cfg(),
                                tup_overrides = _overrides(stage = 'DEV')))


# -----------------------------------------------------------------------------
def _overrides(stage = 'PRD'):
    """
    Return the standard tuple of configuration overrides.

    """

    return ('host.localhost.acct_run', _username())


# -----------------------------------------------------------------------------
def _filepath_cfg():
    """
    Return the filepath to the backend server stableflow configuration file.

    """

    import da.env
    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h60_system',
                relpath      = 'northstar/northstar.stableflow.cfg.yaml')


# -----------------------------------------------------------------------------
def _username():
    """
    Return the current username.

    """

    try:
        username = getpass.getuser()
    except Exception:
        raise RuntimeError('Could not find username.')
    else:
        return username
