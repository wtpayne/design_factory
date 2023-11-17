# -*- coding: utf-8 -*-
"""
---

title:
    "Interactive design index REPL module."

description:
    "This module provides an interactive
    read-eval-print-loop for the design
    index database."

id:
    "65d5d64d-1d72-4d49-bd77-f46e973c75ac"

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


import pycozo.client

import os.path
import pprint


# -----------------------------------------------------------------------------
def _dirpath_self():
    """
    Return the directory path to the current module.

    """

    return os.path.dirname(os.path.realpath(__file__))


# -----------------------------------------------------------------------------
def _dirpath_df():
    """
    Return the path of the root directory of the design factory filesystem.

    """

    return os.path.normpath(os.path.join(_dirpath_self(), '../../../../..'))


# -----------------------------------------------------------------------------
def run():
    """
    Run the interactive design index REPL.

    """

    filepath_db = os.path.join(_dirpath_df(), 'a4_tmp/main/design_index.db')

    str_engine  = 'sqlite'
    filepath_db = '/media/wtp/Data/dev/df/ws00_pri/a4_tmp/main/design_index.db'
    db          = pycozo.client.Client(
                            engine    = str_engine,
                            path      = filepath_db,
                            options   = None,
                            dataframe = False)

    while True:

        try:
            res = db.run(script = input())
        except Exception as err:
            print(repr(err))
        else:
            pprint.pprint(res)

    return 0
