# -*- coding: utf-8 -*-
"""
---

title:
    "Button UI component."

description:
    "This package defines generic button UI
    components for the Amox app."

id:
    "9c6ae731-36e6-4039-b771-642ead42f6fc"

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

import amox.const
import amox.state


# -----------------------------------------------------------------------------
def button(*args, **kwargs) -> reflex.Component:
    """
    A standard button with dark/light mode functionality.

    """

    return reflex.button(

                *args,
                color      = reflex.cond(amox.state.App.is_ena_lightmode,
                                         amox.const.RGB_LT_FG_ACTIVE_BTN,
                                         amox.const.RGB_DK_FG_ACTIVE_BTN),
                background = reflex.cond(amox.state.App.is_ena_lightmode,
                                         amox.const.RGB_LT_BG_ACTIVE_BTN,
                                         amox.const.RGB_DK_BG_ACTIVE_BTN),
                **kwargs)


# -----------------------------------------------------------------------------
def button_with_icon(tag_icon, *args, **kwargs) -> reflex.Component:
    """
    A standard button with an icon and dark/light mode functionality.

    """

    return reflex.button(

                reflex.icon(
                    tag_icon,
                    stroke_width = amox.const.STROKE_BTN_ICON),

                *args,
                color      = reflex.cond(amox.state.App.is_ena_lightmode,
                                         amox.const.RGB_LT_FG_ACTIVE_BTN,
                                         amox.const.RGB_DK_FG_ACTIVE_BTN),
                background = reflex.cond(amox.state.App.is_ena_lightmode,
                                         amox.const.RGB_LT_BG_ACTIVE_BTN,
                                         amox.const.RGB_DK_BG_ACTIVE_BTN),
                **kwargs)
