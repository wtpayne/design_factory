# -*- coding: utf-8 -*-
"""
---

title:
    "Kazul menu UI components."

description:
    "This package defines the menu UI component."

id:
    "603c9d1d-ce1a-4b9e-9ecf-2612919809f3"

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

import kazul.const
import kazul.state


# -----------------------------------------------------------------------------
def menu() -> reflex.Component:
    """
    Navigation menu component.

    This is the navigation block that runs down
    the left hand side of each page.

    """

    return reflex.vstack(

                reflex.heading(
                    kazul.const.NAME_APP,
                    size  = 'lg'),

                _button('Add data source'),
                _button('Add document type'),
                _button('Add document'),

                reflex.spacer(),

                color      = kazul.const.RGB_ACTIVE_FG,
                bg         = kazul.const.RGB_ACTIVE_BG,
                position   = 'fixed',
                top        = kazul.const.SIZE_ZERO,
                left       = kazul.const.SIZE_ZERO,
                width      = kazul.const.SIZE_LEFT_NAVIGATION,
                height     = kazul.const.SIZE_FULL,
                padding    = kazul.const.PADDING_TOPLEVEL,
                spacing    = kazul.const.SPACING_TOPLEVEL,
                margin     = kazul.const.MARGIN_TOPLEVEL,
                box_shadow = kazul.const.CSS_ACTIVE_SHADOW)


# -----------------------------------------------------------------------------
def _button(name: str) -> reflex.Component:
    """
    Menu button component.

    """

    return reflex.button(
                    name,
                    color         = kazul.const.RGB_ACTIVE_BTN_FG,
                    border_radius = kazul.const.RADIUS_BTN,
                    bg            = kazul.const.RGB_ACTIVE_BTN,
                    width         = kazul.const.SIZE_LEFT_BTN)
