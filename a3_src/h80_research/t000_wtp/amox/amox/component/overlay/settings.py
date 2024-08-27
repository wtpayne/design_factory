# -*- coding: utf-8 -*-
"""
---

title:
    "Settings overlay UI components."

description:
    "This package defines UI components for
    the settings overlay."

id:
    "7a0bc997-78a7-4405-8ea7-31004e826731"

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
def panel(**kwargs) -> reflex.Component:
    """
    Menu component with dark/light mode.

    """

    return reflex.center(
                reflex.box(
                    reflex.vstack(
                        reflex.heading('Settings'),
                        reflex.foreach(
                            amox.state.App.list_str_setting,
                            _setting_item)),

                    amox.component.button.button(
                        'Done',
                        on_click      = amox.state.App.on_settings_close(),
                        width         = amox.const.WIDTH_DAY_DONE_BTN,
                        height        = amox.const.HEIGHT_DAY_DONE_BTN,
                        border_radius = amox.const.RADIUS_BTN,
                        position      = 'absolute',
                        right         = amox.const.PADDING_TOPLEVEL,
                        bottom        = amox.const.PADDING_TOPLEVEL),

                    background   = reflex.cond(
                                            amox.state.App.is_ena_lightmode,
                                            amox.const.RGB_LT_BG_PASSIVE,
                                            amox.const.RGB_DK_BG_PASSIVE),
                    width        = amox.const.WIDTH_RESPONSIVE_SETTINGS,
                    height       = amox.const.HEIGHT_SETTINGS,
                    border_color = reflex.cond(
                                            amox.state.App.is_ena_lightmode,
                                            amox.const.RGB_LT_FG_PASSIVE,
                                            amox.const.RGB_DK_FG_PASSIVE),
                    border       = 'thin'),
                style = { 'margin': '0 auto' },
                **kwargs)


# -----------------------------------------------------------------------------
def _setting_item(str_item) -> reflex.Component:
    """
    Checkbox item component.

    """

    return reflex.box(
                reflex.flex(

                    amox.component.button.button(
                        str_item,
                        on_click      = functools.partial(
                                            amox.state.App.on_click_settings_item,
                                            str_item),
                        width         = amox.const.WIDTH_DAY_DONE_BTN,
                        height        = amox.const.HEIGHT_DAY_DONE_BTN,
                        border_radius = amox.const.RADIUS_BTN),

                        reflex.center(
                            reflex.icon(
                                'check',
                                stroke_width = amox.const.STROKE_BTN_ICON,
                                height       = '3rem',
                                width        = '3rem'),

                            width  = '100%',
                            height = '100%'),

                    direction = 'row',
                    width     = '100%',
                    height    = '100%'),

                width      = '16rem',
                background = reflex.cond(amox.state.App.is_ena_lightmode,
                                         amox.const.RGB_LT_BG_PASSIVE,
                                         amox.const.RGB_DK_BG_PASSIVE))



                # reflex.inset(
                #     reflex.icon(
                #         'check',
                #         stroke_width = amox.const.STROKE_BTN_ICON),
                #     side = 'right'),

