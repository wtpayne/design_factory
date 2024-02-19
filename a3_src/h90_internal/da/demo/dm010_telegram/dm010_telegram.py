# -*- coding: utf-8 -*-
"""
---

title:
    "dm010_telegram demo commands."

description:
    "This module defines commands for the
    dm010_telegram demonstration."

id:
    "d738f591-f2a9-4f9a-b2d5-5e625e883e5c"

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
def run():
    """
    Run dm010 telegram bot.

    """

    import da.env.run
    return da.env.run.python_function(spec   = 't000_wtp.telegram.bot.main',
                                      id_env = 'e009_telegram')
