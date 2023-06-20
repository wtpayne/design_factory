# -*- coding: utf-8 -*-
"""
---

title:
    "Utility debug functions module."

description:
    "This module contains various utility
    debug functions."

id:
    "4f768de3-10cd-4ff9-a20e-2541f2790cfc"

type:
    dt003_python_module

validation_level:
    v00_minimums

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


import contextlib
import sys

import rich.console


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def rich_exception_printing_context(debug = True, show_locals = False):
    """
    Context manager for printing nice exception stack traces.

    Uses the rich.console.Console print_exception method.

    """

    if debug:
        try:
            yield
        except Exception as err:
            console = rich.console.Console()
            console.print_exception(show_locals = show_locals)
            sys.exit(1)
    else:
        yield
