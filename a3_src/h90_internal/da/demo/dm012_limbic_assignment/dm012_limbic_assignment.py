# -*- coding: utf-8 -*-
"""
---

title:
    "dm012_limbic_assignment demo commands."

description:
    "This module defines commands for the
    dm012_limbic_assignment demonstration."

id:
    "61f1f7fe-ddd2-4788-8d45-789f574545d0"

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


import getpass
import os
import sys


# -----------------------------------------------------------------------------
def task_1():
    """
    Run dm012 Limbic assignment task 1.

    """

    import da.env
    import da.env.run
    return da.env.run.shell_command(
                        command     = 'uvicorn task_1:app --reload',
                        id_env      = 'e010_dspy',
                        working_dir = da.env.path(
                                            process_area = 'a3_src',
                                            control_tier = 'h80_research',
                                            relpath      = 't000_wtp/limbic'))


# -----------------------------------------------------------------------------
def task_2():
    """
    Run dm012 Limbic assignment task 2.

    """

    import da.env
    import da.env.run
    return da.env.run.shell_command(
                        command     = 'uvicorn task_2:app --reload',
                        id_env      = 'e010_dspy',
                        working_dir = da.env.path(
                                            process_area = 'a3_src',
                                            control_tier = 'h80_research',
                                            relpath      = 't000_wtp/limbic'))

