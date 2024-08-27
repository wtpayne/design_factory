# -*- coding: utf-8 -*-
"""
---

title:
    "dm009_pnyx demo commands."

description:
    "This module defines commands for the
    dm009_pnyx demonstration."

id:
    "da6fd692-707b-481a-8ddc-9a8dcb4465e6"

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
def kazul():
    """
    Run dm009 kazul UI.

    """

    import da.env
    import da.env.run

    ID_ENV = 'e004_reflex'
    _path  = da.env.path
    _run   = da.env.run.shell_command
    return _run('reflex run',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/kazul'),
                id_env      = ID_ENV)

# -----------------------------------------------------------------------------
def kazul_init():
    """
    Run dm009 kazul UI.

    """

    import da.env
    import da.env.run

    ID_ENV = 'e004_reflex'
    _path  = da.env.path
    _run   = da.env.run.shell_command
    return _run('reflex init',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/kazul'),
                id_env      = ID_ENV)

# -----------------------------------------------------------------------------
def sticky():
    """
    Run dm009 sticky UI.

    """

    import da.env
    import da.env.run

    ID_ENV = 'e004_reflex'
    _path  = da.env.path
    _run   = da.env.run.shell_command
    return _run('reflex run',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/sticky'),
                id_env      = ID_ENV)

# -----------------------------------------------------------------------------
def sticky_init():
    """
    Init dm009 sticky UI.

    """

    import da.env
    import da.env.run

    ID_ENV = 'e004_reflex'
    _path  = da.env.path
    _run   = da.env.run.shell_command
    return _run('reflex init',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/sticky'),
                id_env      = ID_ENV)


# -----------------------------------------------------------------------------
def amox_init():
    """
    Init dm009 amox UI.

    """

    import da.env
    import da.env.run

    ID_ENV = 'e004_reflex'
    _path  = da.env.path
    _run   = da.env.run.shell_command
    return _run('reflex init',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/amox'),
                id_env      = ID_ENV)


# -----------------------------------------------------------------------------
def treats():
    """
    Run dm009 treats UI.

    """

    import da.env
    import da.env.run

    map_envvar = os.environ.copy()
    map_envvar['AMOX_CONFIG'] = 'treats.amox.cfg.yaml'
    ID_ENV     = 'e004_reflex'
    _path      = da.env.path
    _run       = da.env.run.shell_command
    return _run('reflex run',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/amox'),
                id_env      = ID_ENV,
                map_envvar  = map_envvar)


# -----------------------------------------------------------------------------
def chimiadao():
    """
    Run dm009 chimiadao UI.

    """

    import da.env
    import da.env.run

    map_envvar = os.environ.copy()
    map_envvar['AMOX_CONFIG'] = 'chimiadao.amox.cfg.yaml'
    ID_ENV     = 'e004_reflex'
    _path      = da.env.path
    _run       = da.env.run.shell_command
    return _run('reflex run',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/amox'),
                id_env      = ID_ENV,
                map_envvar  = map_envvar)


# -----------------------------------------------------------------------------
def functionary():
    """
    Run dm009 functionary UI.

    """

    import da.env
    import da.env.run

    map_envvar = os.environ.copy()
    map_envvar['AMOX_CONFIG'] = 'functionary.amox.cfg.yaml'
    ID_ENV     = 'e004_reflex'
    _path      = da.env.path
    _run       = da.env.run.shell_command
    return _run('reflex run',
                working_dir = _path(
                                process_area = 'a3_src',
                                control_tier = 'h80_research',
                                relpath      = 't000_wtp/amox'),
                id_env      = ID_ENV,
                map_envvar  = map_envvar)

