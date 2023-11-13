# -*- coding: utf-8 -*-
"""
---

title:
    "dm002_civilization demo commands."

description:
    "This module defines commands for the
    dm002_civilization demonstration."

id:
    "7fc0be3e-10a6-478f-bf0f-994417b9d36d"

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


import sys

import da.env
import da.env.run


# -----------------------------------------------------------------------------
def start():
    """
    Start the app on the desktop.

    """

    filepath_app = da.env.path(control_tier = 'h60_system',
                               relpath      = 'civilization/app/main.py',
                               id_env       = 'e002_general_research')

    command = 'python3 {filepath}'.format(filepath = filepath_app)

    sys.exit(da.env.run.shell_command(command = command,
                                      id_env  = 'e002_general_research'))


# -----------------------------------------------------------------------------
def build():
    """
    Build and deploy to the device.

    """

    dirpath_app = da.env.path(control_tier = 'h60_system',
                              relpath      = 'civilization/app',
                              id_env       = 'e002_general_research')

    command = 'cd {dirpath} && buildozer android release deploy run'.format(
                                                        dirpath = dirpath_app)

    sys.exit(da.env.run.shell_command(command = command,
                                      id_env  = 'e002_general_research'))
#
