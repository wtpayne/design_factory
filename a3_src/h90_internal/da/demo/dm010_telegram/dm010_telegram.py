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

    # Load environment variables from .env file.
    #
    import key
    key.load_all(do_load = True)

    import da.env.run
    return da.env.run.python_module(module = 't000_wtp.tgbot',
                                    id_env = 'e009_telegram')


# -----------------------------------------------------------------------------
def isort():
    """
    Run isort tool on the dm010 telegram bot.

    """

    import da.env
    import da.env.run
    import key

    key.load_all(do_load = True)
    ID_ENV       = 'e009_telegram'
    dirpath_work = da.env.path(
                            control_tier = 'h80_research',
                            relpath      = 't000_wtp',
                            id_env       = ID_ENV)
    return da.env.run.shell_command(
                            command      = 'isort tgbot',
                            id_env       = ID_ENV,
                            working_dir  = dirpath_work)


# -----------------------------------------------------------------------------
def pyright():
    """
    Run pyright tool on the dm010 telegram bot.

    """

    import da.env
    import da.env.run
    import key

    key.load_all(do_load = True)
    ID_ENV       = 'e009_telegram'
    dirpath_work = da.env.path(
                            control_tier = 'h80_research',
                            relpath      = 't000_wtp/tgbot',
                            id_env       = ID_ENV)
    return da.env.run.shell_command(
                            command      = 'pyright .',
                            id_env       = ID_ENV,
                            working_dir  = dirpath_work)


# -----------------------------------------------------------------------------
def pylint():
    """
    Run pylint tool on the dm010 telegram bot.

    """

    import da.env
    import da.env.run
    import key

    key.load_all(do_load = True)
    ID_ENV       = 'e009_telegram'
    dirpath_work = da.env.path(
                            control_tier = 'h80_research',
                            relpath      = 't000_wtp',
                            id_env       = ID_ENV)
    return da.env.run.shell_command(
                            command      = 'pylint tgbot',
                            id_env       = ID_ENV,
                            working_dir  = dirpath_work)