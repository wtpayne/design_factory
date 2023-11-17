# -*- coding: utf-8 -*-
"""
---

title:
    "Process assistant service commands package."

description:
    "This package provides commands to start
    and stop design check service."

id:
    "a25a6ffe-db4c-47d1-8d04-7f78122d973f"

type:
    dt002_python_package

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

...
"""


import getpass
import os
import sys

import da.env.run


# -----------------------------------------------------------------------------
def start():
    """
    Start the process assistant service.

    This function will create the database directory
    if it doesn't already exist and then launch the
    stableflow service with some context dependent
    runtime configuration.

    """

    filepath_db = _filepath_db()
    dirpath_db  = os.path.dirname(filepath_db)
    if not os.path.exists(dirpath_db):
        os.makedirs(dirpath_db)

    tup_overrides = (
        'node.filesystem_watcher.config.iter_dirpath_root', [_dirpath_src(),],
        'node.ui_discord_client.config.filepath_env',        _filepath_dotenv(),
        'node.design_index_db.config.filepath_db',           _filepath_db(),
        'host.localhost.acct_run',                           _username())

    da.env.run.stableflow_start(
        path_cfg      = _filepath_system_cfg(),
        tup_overrides = tup_overrides)


# -----------------------------------------------------------------------------
def stop():
    """
    Stop the process assistant service.

    """

    da.env.run.stableflow_stop(path_cfg = _filepath_system_cfg())


# -----------------------------------------------------------------------------
def _filepath_db():
    """
    Return the file path of the design index database file.

    """

    return os.path.join(_dirpath_tmp(), 'main/design_index.db')


# -----------------------------------------------------------------------------
def _dirpath_tmp():
    """
    Return the path of the root directory of the temporary document filesystem.

    """

    return os.path.join(_dirpath_root(), 'a4_tmp')


# -----------------------------------------------------------------------------
def _dirpath_src():
    """
    Return the path of the root directory of the design document filesystem.

    The source design documents which are
    monitored by the process assistant are
    all stored in a single large filesystem
    hierarchy.

    This function returns the directory path
    of the root directory of this filesystem
    hierarchy.

    """

    return os.path.join(_dirpath_root(), 'a3_src')


# -----------------------------------------------------------------------------
def _dirpath_root():
    """
    Return the path of the root directory of the design factory filesystem.

    """

    return os.path.normpath(os.path.join(_dirpath_self(), '../../../../../..'))


# -----------------------------------------------------------------------------
def _filepath_dotenv():
    """
    Return the file path of the .env file.

    The .env file is used to store secrets for
    the process asssistant tool, such as API keys
    and passwords for different integrations.

    """

    return os.path.join(_dirpath_self(), '.env')


# -----------------------------------------------------------------------------
def _filepath_system_cfg():
    """
    Return the file path of the configuration data.

    """

    dirpath_self = _dirpath_self()
    filename_cfg = '{name_system}.stableflow.cfg.yaml'.format(
                                name_system = os.path.basename(dirpath_self))

    return os.path.join(dirpath_self, filename_cfg)


# -----------------------------------------------------------------------------
def _dirpath_self():
    """
    Return the directory path to the current module.

    """

    return os.path.dirname(os.path.realpath(__file__))


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
