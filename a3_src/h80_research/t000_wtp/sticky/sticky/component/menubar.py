# -*- coding: utf-8 -*-
"""
---

title:
    "Sticky menubar UI components."

description:
    "This package defines the menubar UI
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


import functools

import reflex

import sticky.component.button
import sticky.const
import sticky.state


# -----------------------------------------------------------------------------
def menubar(**kwargs) -> reflex.Component:
    """
    Menubar component.

    """

    return reflex.hstack(

                reflex.heading(
                    sticky.const.NAME_APP,
                    color  = reflex.cond(
                                    sticky.state.App.is_ena_lightmode,
                                    sticky.const.RGB_LT_FG_PASSIVE,
                                    sticky.const.RGB_DK_FG_PASSIVE),
                    height = sticky.const.SIZE_MENU_BTN),

                reflex.spacer(),

                _mainmenu(
                    tag_icon    = 'menu',
                    iter_values = sticky.state.App.iter_str_menuitem,
                    on_click    = sticky.state.App.on_click_mainmenu_item),

                **kwargs)


# -----------------------------------------------------------------------------
def _mainmenu(tag_icon, iter_values, on_click, **kwargs) -> reflex.Component:
    """
    Main menu for the app.

    """

    return reflex.drawer.root(

                _mainmenu_trigger(
                    tag_icon = tag_icon,
                    color    = reflex.cond(
                                    sticky.state.App.is_ena_lightmode,
                                    sticky.const.RGB_LT_FG_PASSIVE,
                                    sticky.const.RGB_DK_FG_PASSIVE),
                    width    = sticky.const.SIZE_MENU_BTN,
                    height   = sticky.const.SIZE_MENU_BTN),

                _mainmenu_container(
                    tag_icon    = tag_icon,
                    iter_values = iter_values,
                    on_click    = on_click,
                    top         = 'auto',
                    left        = 'auto',
                    height      = sticky.const.SIZE_FULL,
                    width       = sticky.const.SIZE_MENU_MAIN,
                    padding     = sticky.const.PADDING_TOPLEVEL,
                    color       = reflex.cond(
                                    sticky.state.App.is_ena_lightmode,
                                    sticky.const.RGB_LT_FG_PASSIVE,
                                    sticky.const.RGB_DK_FG_PASSIVE),
                    background  = reflex.cond(
                                    sticky.state.App.is_ena_lightmode,
                                    sticky.const.RGB_LT_BG_PASSIVE_ACCENT,
                                    sticky.const.RGB_DK_BG_PASSIVE_ACCENT)),

                direction = 'right')


# -----------------------------------------------------------------------------
def _mainmenu_trigger(tag_icon, **kwargs) -> reflex.Component:
    """
    Icon to trigger the main menu.

    """

    return reflex.drawer.trigger(
                reflex.icon(
                    tag_icon,
                    **kwargs))


# -----------------------------------------------------------------------------
def _mainmenu_container(
            tag_icon, iter_values, on_click, **kwargs) -> reflex.Component:
    """
    Trigger button for the main menu.

    """
    return reflex.fragment(
                reflex.drawer.overlay(),
                reflex.drawer.portal(
                    reflex.drawer.content(
                        _mainmenu_content(
                            tag_icon    = tag_icon,
                            iter_values = iter_values,
                            on_click    = on_click),
                        **kwargs)))


# -----------------------------------------------------------------------------
def _mainmenu_content(
            tag_icon, iter_values, on_click, **kwargs) -> reflex.Component:
    """
    """
    return reflex.vstack(

                reflex.spacer(),

                reflex.foreach(
                    iter_values,
                    functools.partial(_mainmenu_item, on_click)),

                reflex.drawer.close(
                    reflex.icon(
                        tag_icon,
                        width  = sticky.const.SIZE_MENU_BTN,
                        height = sticky.const.SIZE_MENU_BTN)),

                width = sticky.const.SIZE_FULL,
                align = 'end')

# -----------------------------------------------------------------------------
def _mainmenu_item(on_click, str_name, **kwargs) -> reflex.Component:
    """
    """

    return sticky.component.button.button(
                str_name,
                on_click = functools.partial(
                                    sticky.state.App.on_click_mainmenu_item,
                                    str_name),
                width    = sticky.const.SIZE_FULL,
                **kwargs)



#     return reflex.menu.root(

#                 _menu_content(
#                     iter_values,
#                     on_select = on_select,
#                     width     = '10rem'),

#                 default_value = 'January')




                # sticky.component.menu.menu_main(
                #     iter_values   = sticky.state.App.iter_str_month_nav,
                #     value_default = reflex.icon(
                #                         'menu',
                #                         width    = sticky.const.SIZE_MENU_BTN,
                #                         height   = sticky.const.SIZE_MENU_BTN),
                #     on_select     = sticky.state.App.on_month_select,
                #     flex          = 'none',
                #     width         = sticky.const.SIZE_MENU_BTN,
                #     height        = sticky.const.SIZE_MENU_BTN,
                #     border_radius = sticky.const.RADIUS_BTN),

