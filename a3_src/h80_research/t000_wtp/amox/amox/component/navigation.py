# -*- coding: utf-8 -*-
"""
---

title:
    "Amox navigation UI components."

description:
    "This package defines the navigation UI
    components for the Amox app."

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

import amox.component.button
import amox.component.dropdown
import amox.const
import amox.state


# -----------------------------------------------------------------------------
def navigation(**kwargs) -> reflex.Component:
    """
    Navigation component.

    """

    return reflex.hstack(

                amox.component.button.button_with_icon(
                    on_click      = amox.state.App.on_click_nav_month_prev,
                    tag_icon      = 'arrow-left',
                    flex          = 'none',
                    width         = amox.const.SIZE_NAV_BTN,
                    height        = amox.const.SIZE_NAV_BTN,
                    border_radius = amox.const.RADIUS_BTN),

                reflex.spacer(),

                amox.component.dropdown.menu(
                    iter_values   = amox.state.App.iter_str_month_nav,
                    value_default = amox.state.App.str_month_selected,
                    on_select     = amox.state.App.on_select_nav_month,
                    flex          = 'none',
                    width         = amox.const.WIDTH_NAV_SELECT,
                    height        = amox.const.SIZE_NAV_BTN,
                    border_radius = amox.const.RADIUS_BTN),

                amox.component.dropdown.menu(
                    iter_values   = amox.state.App.iter_str_year_nav,
                    value_default = amox.state.App.str_year_selected,
                    on_select     = amox.state.App.on_select_nav_year,
                    flex          = 'none',
                    width         = amox.const.WIDTH_NAV_SELECT,
                    height        = amox.const.SIZE_NAV_BTN,
                    border_radius = amox.const.RADIUS_BTN),

                reflex.spacer(),

                amox.component.button.button_with_icon(
                    on_click      = amox.state.App.on_click_nav_month_next,
                    tag_icon      = 'arrow-right',
                    flex          = 'none',
                    width         = amox.const.SIZE_NAV_BTN,
                    height        = amox.const.SIZE_NAV_BTN,
                    border_radius = amox.const.RADIUS_BTN),

                **kwargs)
