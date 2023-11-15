# -*- coding: utf-8 -*-
"""
---

title:
    "dm008_epistematic demo commands."

description:
    "This module defines commands for the
    dm008_epistematic demonstration."

id:
    "1e326fd3-9c9d-487d-917a-cbc0c112f255"

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
def test():
    """
    Run all dm008 tests.

    """

    import da.env
    import da.test

    _run   = da.test.run
    _path  = da.env.path
    ID_ENV = 'e005_pdf'

    return _run(id_env        = ID_ENV,
                verbose_level = 0,
                iter_path     = (_path(control_tier = 'h20_functionality',
                                       relpath      = 'fl/load',
                                       id_env       = ID_ENV)),)


# -----------------------------------------------------------------------------
def start():
    """
    Start an instance of the dm008 system.

    """

    import da.env.run
    sys.exit(da.env.run.stableflow_start(
                                path_cfg      = _filepath_cfg(),
                                is_local      = False,
                                tup_overrides = _overrides(stage = 'DEV')))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop any running instances of the dm008 system.

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
    Return the filepath to the system stableflow configuration file.

    """

    import da.env
    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h60_system',
                relpath      = 'epistematic/epistematic.stableflow.cfg.yaml')


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