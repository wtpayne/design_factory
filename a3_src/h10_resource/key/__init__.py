# -*- coding: utf-8 -*-
"""
---

title:
    "Key loading functions module."

description:
    "This module contains utility functions for
    handling secrets."

id:
    "967d1d7d-d5da-4522-9dbf-e6b4615d5d80"

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

...
"""


import os
import os.path

import dotenv


# -----------------------------------------------------------------------------
def load(id_value, filepath_env = None):
    """
    Load a value from an environment variable or a .env file.

    This function first attempts to load the value
    from the system's environment variables. If
    the value is not found and a path to a .env
    file is provided (`filepath_env`), it will
    try to load the value from this file. If no
    path is provided, the function will look for
    a 'default.env' file in the same directory as
    the script. If the 'default.env' file does not
    exist, it uses the dotenv.find_dotenv method
    to locate it.

    Parameters
    ----------
    id_value : str                  The key to be retrieved. This key could
                                    be present in the system's environment
                                    variables or in the specified/default
                                    .env file.

    filepath_env : str, optional    The explicit path to the .env file where
                                    the key might be located. If not provided,
                                    the function will look for a 'default.env'
                                    file in the same directory as the script,
                                    or it will try to locate it using
                                    dotenv.find_dotenv method.

    Returns
    -------
    str     The value associated with the `id_value`. If the `id_value`
            is not found, a KeyError will be raised.

    Raises
    ------
    KeyError    If the `id_value` is not found in both the system's
                environment variables and the .env file.

    IOError     If the 'default.env' file is not found when no
                `filepath_env` is provided.

    """

    value = os.getenv(id_value, default = None)
    if value is not None:
        return value

    map_value = load_all(filepath_env = filepath_env)

    return map_value[id_value]


# -----------------------------------------------------------------------------
def load_all(filepath_env = None, do_load = False):
    """
    Load all dotenv values.

    """

    if filepath_env is None:
        filename_env = 'default.env'
        dirpath_self = os.path.dirname(os.path.realpath(__file__))
        filepath_env = os.path.join(dirpath_self, filename_env)
        if not os.path.isfile(filepath_env):
            filepath_env = dotenv.find_dotenv(
                                    filename                 = filename_env,
                                    raise_error_if_not_found = True,
                                    usecwd = True)

    if do_load:
        dotenv.load_dotenv(dotenv_path = filepath_env)

    map_value = dotenv.dotenv_values(dotenv_path = filepath_env,
                                     verbose     = True)

    return map_value
