# -*- coding: utf-8 -*-
"""
---

title:
    "dm016_demo demo commands."

description:
    "This module defines commands for the
    dm015_hyperview demonstration."

id:
    "8b0a4ecb-8d7b-413b-98de-61fe5ef4c742"

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
    Start stableflow demo.

    """

    import da.env
    import da.env.run

    filepath_cfg = da.env.path(
        process_area = 'a3_src',
        control_tier = 'h80_research',
        relpath      = f't000_wtp/demo/demo.stableflow.cfg.yaml')
    sys.exit(da.env.run.stableflow_start(path_cfg = filepath_cfg))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop stableflow demo.

    """

    import da.env
    import da.env.run

    filepath_cfg = da.env.path(
        process_area = 'a3_src',
        control_tier = 'h80_research',
        relpath      = f't000_wtp/demo/demo.stableflow.cfg.yaml')
    sys.exit(da.env.run.stableflow_stop(path_cfg = filepath_cfg))
