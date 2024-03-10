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

import sticky.component.button
import sticky.component.dropdown
import sticky.const
import sticky.state






# -----------------------------------------------------------------------------
def navigation(**kwargs) -> reflex.Component:
    """
    Navigation component.

    """

    return reflex.hstack(

                sticky.component.button.button_with_icon(
                    on_click      = sticky.state.App.on_month_prev,
                    id_icon       = 'arrow-left',
                    flex          = 'none',
                    width         = sticky.const.SIZE_NAV_BTN,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                reflex.spacer(),

                sticky.component.dropdown.menu(
                    iter_values   = sticky.state.App.iter_str_month_nav,
                    value_default = sticky.state.App.str_month_selected,
                    on_select     = sticky.state.App.on_month_select,
                    flex          = 'none',
                    width         = sticky.const.WIDTH_NAV_SELECT,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                sticky.component.dropdown.menu(
                    iter_values   = sticky.state.App.iter_str_year_nav,
                    value_default = sticky.state.App.str_year_selected,
                    on_select     = sticky.state.App.on_year_select,
                    flex          = 'none',
                    width         = sticky.const.WIDTH_NAV_SELECT,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                reflex.spacer(),

                sticky.component.button.button_with_icon(
                    on_click      = sticky.state.App.on_month_next,
                    id_icon       = 'arrow-right',
                    flex          = 'none',
                    width         = sticky.const.SIZE_NAV_BTN,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                **kwargs)
