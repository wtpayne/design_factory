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

import sticky.component.menu
import sticky.const
import sticky.state


ITER_STR_MONTH = ['January', 'February', 'March',
                  'April',   'May',      'June',
                  'July',    'August',   'September',
                  'October', 'November', 'December']

ITER_STR_YEAR = ['2020','2021','2022','2023','2024']


# -----------------------------------------------------------------------------
def navigation(**kwargs) -> reflex.Component:
    """
    Navigation component.

    """

    return reflex.hstack(

                _btn_icon(
                    id_icon       = 'arrow-left',
                    flex          = 'none',
                    width         = sticky.const.SIZE_NAV_BTN,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                reflex.spacer(),

                sticky.component.menu.menu(
                    iter_values   = ITER_STR_MONTH,
                    value_default = 'February',
                    on_select     = sticky.state.App.on_select_month,
                    flex          = 'none',
                    width         = '7rem',
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                sticky.component.menu.menu(
                    iter_values   = ITER_STR_YEAR,
                    value_default = ITER_STR_YEAR[-1],
                    on_select     = sticky.state.App.on_select_year,
                    flex          = 'none',
                    width         = '7rem',
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                reflex.spacer(),

                _btn_icon(
                    id_icon       = 'arrow-right',
                    flex          = 'none',
                    width         = sticky.const.SIZE_NAV_BTN,
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                **kwargs)


# -----------------------------------------------------------------------------
def _btn_icon(id_icon, *args, **kwargs) -> reflex.Component:
    """
    A standard button with an icon and dark/light mode functionality.

    """

    return reflex.button(

                reflex.icon(
                    id_icon,
                    stroke_width = sticky.const.STROKE_NAV_ICON),

                *args,
                color      = reflex.cond(sticky.state.App.is_lightmode,
                                         sticky.const.RGB_LT_FG_ACTIVE_BTN,
                                         sticky.const.RGB_DK_FG_ACTIVE_BTN),
                background = reflex.cond(sticky.state.App.is_lightmode,
                                         sticky.const.RGB_LT_BG_ACTIVE_BTN,
                                         sticky.const.RGB_DK_BG_ACTIVE_BTN),
                **kwargs)
