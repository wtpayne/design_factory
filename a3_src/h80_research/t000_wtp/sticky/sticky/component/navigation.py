# -*- coding: utf-8 -*-
"""
---

title:
    "Sticky navigation UI components."

description:
    "This package defines the navigation UI
    components for the Sticky app."

id:
    "4b19fcb0-b2c8-467f-92cb-a5259934f859"

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
def navigation(**kwargs) -> reflex.Component:
    """
    Navigation component.

    """

    return reflex.hstack(

                _btn_prev(
                    flex          = 'none',
                    width         = sticky.const.SIZE_NAV_BTN,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                reflex.spacer(),

                reflex.card(
                    sticky.state.App.view_month_name,
                    flex          = 'none',
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN,
                    background    = sticky.const.RGB_PASSIVE_BG_ACCENT),

                reflex.card(
                    sticky.state.App.view_year,
                    flex          = 'none',
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN,
                    background    = sticky.const.RGB_PASSIVE_BG_ACCENT),

                reflex.spacer(),

                _btn_next(
                    flex          = 'none',
                    width         = sticky.const.SIZE_NAV_BTN,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN,
                    background    = sticky.const.RGB_ACTIVE_BTN),

                **kwargs)


# -----------------------------------------------------------------------------
def _btn_prev(**kwargs) -> reflex.Component:
    """
    """

    return reflex.button(

                reflex.icon(
                    'arrow-left',
                    stroke_width = sticky.const.STROKE_NAV_ICON),

                on_click = sticky.state.App.on_click_nav_month_prev(),

                **kwargs)


# -----------------------------------------------------------------------------
def _btn_next(**kwargs) -> reflex.Component:
    """
    """

    return reflex.button(

                reflex.icon(
                    'arrow-right',
                    stroke_width = sticky.const.STROKE_NAV_ICON),

                on_click = sticky.state.App.on_click_nav_month_next(),

                **kwargs)

