# -*- coding: utf-8 -*-
"""
---

title:
    "Amox menubar UI components."

description:
    "This package defines the menubar UI
    components for the Amox app."

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


import functools

import reflex

import amox.component.button
import amox.const
import amox.state


# -----------------------------------------------------------------------------
def menubar(**kwargs) -> reflex.Component:
    """
    Menubar component.

    """

    return reflex.hstack(

                reflex.heading(
                    amox.const.NAME_APP,
                    color  = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                    height = amox.const.SIZE_MENUBAR_BTN),

                reflex.spacer(),

                _button_mainmenu(
                    on_click = amox.state.App.on_click_mainmenu,
                    tag_icon = 'menu'),

                reflex.cond(
                    amox.state.App.is_ena_mainmenu,
                    _mainmenu(
                        tag_icon    = 'menu',
                        iter_values = amox.state.App.iter_tup_menuitem,
                        on_click    = amox.state.App.on_click_mainmenu_item),
                    reflex.fragment()),

                **kwargs)


# -----------------------------------------------------------------------------
def _button_mainmenu(tag_icon, *args, **kwargs) -> reflex.Component:
    """
    A standard button with an icon and dark/light mode functionality.

    """

    return reflex.button(

                reflex.icon(
                    tag_icon,
                    stroke_width = amox.const.STROKE_BTN_ICON,
                    width        = amox.const.SIZE_MAINMENU_ICON,
                    height       = amox.const.SIZE_MAINMENU_ICON),

                *args,
                color      = reflex.cond(amox.state.App.is_ena_lightmode,
                                         amox.const.RGB_LT_FG_PASSIVE,
                                         amox.const.RGB_DK_FG_PASSIVE),
                background = reflex.cond(amox.state.App.is_ena_lightmode,
                                         amox.const.RGB_LT_BG_PASSIVE,
                                         amox.const.RGB_DK_BG_PASSIVE),
                **kwargs)


# -----------------------------------------------------------------------------
def _mainmenu(tag_icon, iter_values, on_click, **kwargs) -> reflex.Component:
    """
    Main menu for the app.

    """

    return reflex.hstack(

                reflex.spacer(
                    display = amox.const.SPACE_RESPONSIVE_TOPLEVEL),

                reflex.hstack(

                    reflex.spacer(),

                    reflex.box(
                        _mainmenu_content(
                            tag_icon    = tag_icon,
                            iter_values = iter_values,
                            on_click    = on_click),
                        background  = reflex.cond(
                                        amox.state.App.is_ena_lightmode,
                                        amox.const.RGB_LT_BG_PASSIVE,
                                        amox.const.RGB_DK_BG_PASSIVE),
                        width      = amox.const.SIZE_RESPONSIVE_MAINMENU,
                        height     = '100%'),
                    width      = amox.const.WIDTH_RESPONSIVE_TOPLEVEL,
                    height     = '100%'),

                reflex.spacer(
                    display = amox.const.SPACE_RESPONSIVE_TOPLEVEL),

                background = amox.const.RGBA_DIMMING,
                position   = 'absolute',
                z_index    = '5',
                left       = amox.const.SIZE_ZERO,
                right      = amox.const.SIZE_ZERO,
                top        = amox.const.SIZE_ZERO,
                bottom     = amox.const.SIZE_MENUBAR)


# -----------------------------------------------------------------------------
def _mainmenu_content(
            tag_icon, iter_values, on_click, **kwargs) -> reflex.Component:
    """
    """

    return reflex.vstack(

                reflex.spacer(),

                reflex.foreach(
                    iter_values,
                    functools.partial(
                        _mainmenu_item, on_click)),

                width  = amox.const.SIZE_FULL,
                height = '100%',
                align  = 'end')


# -----------------------------------------------------------------------------
def _mainmenu_item(on_click, tup_value, **kwargs) -> reflex.Component:
    """
    """

    return reflex.button(
                _mainmenu_item_content(tag_icon  = tup_value[0],
                                       str_label = tup_value[1]),
                on_click    = functools.partial(
                                    amox.state.App.on_click_mainmenu_item,
                                    tup_value[1]),
                color       = reflex.cond(
                                amox.state.App.is_ena_lightmode,
                                amox.const.RGB_LT_FG_PASSIVE,
                                amox.const.RGB_DK_FG_PASSIVE),
                background  = reflex.cond(
                                amox.state.App.is_ena_lightmode,
                                amox.const.RGB_LT_BG_PASSIVE,
                                amox.const.RGB_DK_BG_PASSIVE),
                size        = amox.const.SIZE_MAINMENU_ITEM,
                radius      = 'none',
                margin      = amox.const.SIZE_ZERO,
                padding     = amox.const.SIZE_ZERO,
                width       = amox.const.SIZE_FULL,
                height      = amox.const.SIZE_MAINMENU_BTN,
                **kwargs)


# -----------------------------------------------------------------------------
def _mainmenu_item_content(tag_icon, str_label) -> reflex.Component:
    """
    """

    return reflex.hstack(

                reflex.match(
                    tag_icon,
                    ('settings', _mainmenu_item_icon('settings')),
                    ('plus',     _mainmenu_item_icon('plus'))),

                str_label,

                padding_left = amox.const.SIZE_MAINMENU_ITEM_LPAD,
                align        = 'center',
                width        = amox.const.SIZE_FULL)

# -----------------------------------------------------------------------------
def _mainmenu_item_icon(tag_icon) -> reflex.Component:
    """
    """

    return reflex.icon(
                tag_icon,
                width  = amox.const.SIZE_MAINMENU_ITEM_ICON,
                height = amox.const.SIZE_MAINMENU_ITEM_ICON)
