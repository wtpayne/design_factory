# -*- coding: utf-8 -*-
"""
---

title:
    "Dropdown menu UI components."

description:
    "This package defines a generic dropdown menu
    UI component for the Sticky app."

id:
    "0576cce8-3f8b-4b4d-b54d-1ba183547038"

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
def menu(iter_values, value_default, on_select, **kwargs) -> reflex.Component:
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

                sticky.state.App.is_ena_lightmode,

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
                reflex.vstack(
                    reflex.foreach(
                        iter_values,
                        functools.partial(
                            _menuitem,
                            on_select = on_select))),
                width      = width,
                color      = reflex.cond(sticky.state.App.is_ena_lightmode,
                                         sticky.const.RGB_LT_FG_ACTIVE_BTN,
                                         sticky.const.RGB_DK_FG_ACTIVE_BTN),
                background = reflex.cond(sticky.state.App.is_ena_lightmode,
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
                on_select = functools.partial(on_select, value),
                value     = value)