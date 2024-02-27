# -*- coding: utf-8 -*-
"""
---

title:
    "Sticky menu UI components."

description:
    "This package defines the menu UI
    components for the Sticky app."

id:
    "bf21471d-330e-4bfe-b1a0-a3aa2ced65ab"

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
def menu(**kwargs) -> reflex.Component:
    """
    Menu component.

    """

    return reflex.hstack(

                reflex.heading(
                    sticky.const.NAME_APP,
                    height = sticky.const.SIZE_MENU_BTN),

                reflex.spacer(),

                reflex.icon(
                    'menu',
                    on_click = sticky.state.App.on_toggle_color_mode,
                    width    = sticky.const.SIZE_MENU_BTN,
                    height   = sticky.const.SIZE_MENU_BTN),

                **kwargs)
