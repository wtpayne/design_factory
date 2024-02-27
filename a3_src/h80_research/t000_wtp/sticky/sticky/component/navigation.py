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


import functools

import reflex

import sticky.const
import sticky.state


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

                _menu(
                    iter_values   = ['January', 'February', 'March', 'April'],
                    value_default = 'February',
                    on_select     = sticky.state.App.on_select_month,
                    flex          = 'none',
                    width         = '7rem',
                    height        = sticky.const.SIZE_NAV_BTN,
                    border_radius = sticky.const.RADIUS_BTN),

                _menu(
                    iter_values   = ['2024', '2023', '2022'],
                    value_default = '2024',
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
def _menu(iter_values, value_default, on_select, **kwargs) -> reflex.Component:
    """
    Menu component with dark/light mode.

    """

    return reflex.menu.root(

                _menu_trigger(
                    value_default,
                    **kwargs),

                _menu_content(
                    iter_values,
                    on_select = on_select,
                    width     = kwargs['width']),

                default_value = value_default)



# -----------------------------------------------------------------------------
def _menu_trigger(value_default, **kwargs) -> reflex.Component:
    """
    Menu trigger component with dark/light mode.

    """

    return reflex.cond(

                sticky.state.App.is_lightmode,

                reflex.menu.trigger(
                    reflex.button(
                        value_default,
                        color      = sticky.const.RGB_LT_FG_ACTIVE_BTN,
                        background = sticky.const.RGB_LT_BG_ACTIVE_BTN,
                        **kwargs),
                    color      = sticky.const.RGB_LT_FG_ACTIVE_BTN,
                    background = sticky.const.RGB_LT_BG_ACTIVE_BTN),

                reflex.menu.trigger(
                    reflex.button(
                        value_default,
                        color      = sticky.const.RGB_DK_FG_ACTIVE_BTN,
                        background = sticky.const.RGB_DK_BG_ACTIVE_BTN,
                        **kwargs),
                    color      = sticky.const.RGB_DK_FG_ACTIVE_BTN,
                    background = sticky.const.RGB_DK_BG_ACTIVE_BTN))


# -----------------------------------------------------------------------------
def _menu_content(iter_values, on_select, width, **kwargs) -> reflex.Component:
    """
    Menu content group component with dark/light mode functionality.

    """

    return reflex.menu.content(
                reflex.foreach(
                    iter_values,
                    functools.partial(
                        _menuitem,
                        on_select = on_select)),
                width      = width,
                color      = reflex.cond(sticky.state.App.is_lightmode,
                                         sticky.const.RGB_LT_FG_ACTIVE_BTN,
                                         sticky.const.RGB_DK_FG_ACTIVE_BTN),
                background = reflex.cond(sticky.state.App.is_lightmode,
                                         sticky.const.RGB_LT_BG_ACTIVE_BTN,
                                         sticky.const.RGB_DK_BG_ACTIVE_BTN),
                **kwargs)


# -----------------------------------------------------------------------------
def _menuitem(value, on_select) -> reflex.Component:
    """
    Menu item component as a single function.

    """

    return reflex.menu.item(
                value,
                on_select = on_select,
                value     = value)


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
