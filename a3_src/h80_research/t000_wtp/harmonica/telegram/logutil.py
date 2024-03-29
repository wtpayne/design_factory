# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot logging utilities module."

description:
    "This module contains logging utility
    functions to help with configuring
    and running a Telegram bot using the
    python-telegram-bot library."

id:
    "3faff4d4-3057-43e8-99f1-37d35978aa32"

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


import functools
import logging


# -----------------------------------------------------------------------------
def setup():
    """
    Setup logging.

    """

    str_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format = str_format,
                        level  = logging.INFO)


# -----------------------------------------------------------------------------
def trace(fcn_wrapped):
    """
    Add trace logging calls to the wrapped function.

    """

    @functools.wraps(fcn_wrapped)
    def fcn_wrapper(*args, **kwargs):
        """
        Trace logging wrapper.

        """

        logging.debug('Call: %s()', fcn_wrapped.__name__)
        return fcn_wrapped(*args, **kwargs)

    return fcn_wrapper
