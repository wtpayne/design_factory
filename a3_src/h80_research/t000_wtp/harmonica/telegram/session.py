# -*- coding: utf-8 -*-
"""
---

title:
    "Session logic module."

description:
    "This module contains session logic for
    the harmonica bot."

id:
    "af64c9a1-f34b-4396-8249-8db5085b7c68"

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


import pydantic


# =============================================================================
class State(pydantic.BaseModel):
    """
    Session state.

    """

    version:   int = 1
    str_name:  str = 'MySession'
    set_track: set = set()

