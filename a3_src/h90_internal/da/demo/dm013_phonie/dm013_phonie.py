# -*- coding: utf-8 -*-
"""
---

title:
    "dm013_phonie demo commands."

description:
    "This module defines commands for the
    dm013_phonie demonstration."

id:
    "bc8b262c-5750-4b21-ba60-27655c368d09"

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


import sys


# -----------------------------------------------------------------------------
def start():
    """
    Start the dm013 phonie system.

    """

    import da.env.run

    sys.exit(da.env.run.stableflow_start(path_cfg = _filepath_cfg()))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop the dm013 phonie system.

    """

    import da.env.run

    sys.exit(da.env.run.stableflow_stop(path_cfg = _filepath_cfg()))


# -----------------------------------------------------------------------------
def _filepath_cfg():
    """
    Return the filepath to the backend server stableflow configuration file.

    """

    import da.env

    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h80_research',
                relpath      = 't000_wtp/phonie/phonie.stableflow.cfg.yaml')

