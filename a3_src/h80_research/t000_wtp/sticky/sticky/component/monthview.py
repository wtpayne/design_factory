# -*- coding: utf-8 -*-
"""
---

title:
    "Sticky monthview UI components."

description:
    "This package defines the monthview UI
    component for the sticky app."

id:
    "da9cd82e-6069-420f-8ba3-ccb4fa6469eb"

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


import reflex

import sticky.const
import sticky.state


# -----------------------------------------------------------------------------
def monthview() -> reflex.Component:
    """
    Monthview component.

    """

    return reflex.grid(
        reflex.foreach(
            sticky.state.App.list_days,
            _monthbox),
        template_columns="repeat(7, 1fr)",
        template_rows="repeat(5, 1fr)",
        h="100vh",
        width="100%",
        gap='0.1em',
)


# -----------------------------------------------------------------------------
def _monthbox(idx: int) -> reflex.Component:
    """
    Monthbox component.

    """
    return reflex.grid_item(
                        row_span=1,
                        col_span=1,
                        border_radius = '0.1rem',
                        border_color  = 'black',
                        border = 'thin',
                        bg="white")
