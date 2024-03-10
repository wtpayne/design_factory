# -*- coding: utf-8 -*-
"""
---

title:
    "Menu UI components."

description:
    "This package defines a generic menu UI
    component for the Sticky app."

id:
    "6a19b70a-04fb-49d7-a4fc-d36ba6bc89e5"

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
def panel(**kwargs) -> reflex.Component:
    """
    Menu component with dark/light mode.

    """

    return reflex.box(
                reflex.card(

                    reflex.heading('Records'),

                    reflex.spacer(
                        height = sticky.const.PADDING_TOPLEVEL),

                    reflex.center(
                        reflex.vstack(
                            reflex.foreach(
                                sticky.state.App.list_str_item,
                                _daily_item))),

                    sticky.component.button.button(
                        'Done',
                        on_click      = sticky.state.App.on_toggle_overlay_day,
                        width         = sticky.const.WIDTH_DAY_DONE_BTN,
                        height        = sticky.const.HEIGHT_DAY_DONE_BTN,
                        border_radius = sticky.const.RADIUS_BTN,
                        position      = 'absolute',
                        right         = sticky.const.PADDING_TOPLEVEL,
                        bottom        = sticky.const.PADDING_TOPLEVEL),

                    background   = reflex.cond(
                                            sticky.state.App.is_ena_lightmode,
                                            sticky.const.RGB_LT_BG_PASSIVE,
                                            sticky.const.RGB_DK_BG_PASSIVE),
                    position     = 'absolute',
                    left         = sticky.const.GUTTTER_DAY,
                    right        = sticky.const.GUTTTER_DAY,
                    top          = sticky.const.GUTTTER_DAY,
                    bottom       = sticky.const.GUTTTER_DAY_BOTTOM,
                    border_color = 'black',
                    border       = 'thin'),
                **kwargs)


# -----------------------------------------------------------------------------
def _daily_item(str_item) -> reflex.Component:
    """
    Checkbox item component.

    """

    return reflex.card(
                reflex.flex(

                    sticky.component.button.button(
                        str_item,
                        on_click      = functools.partial(
                                            sticky.state.App.on_click_daily_item,
                                            str_item),
                        width         = sticky.const.WIDTH_DAY_DONE_BTN,
                        height        = sticky.const.HEIGHT_DAY_DONE_BTN,
                        border_radius = sticky.const.RADIUS_BTN),

                        reflex.center(
                            reflex.icon(
                                'check',
                                stroke_width = sticky.const.STROKE_BTN_ICON,
                                height       = '3rem',
                                width        = '3rem'),

                            width  = '100%',
                            height = '100%'),

                    direction = 'row',
                    width     = '100%',
                    height    = '100%'),

                width      = '16rem',
                background = reflex.cond(sticky.state.App.is_ena_lightmode,
                                         sticky.const.RGB_LT_BG_PASSIVE,
                                         sticky.const.RGB_DK_BG_PASSIVE))



                # reflex.inset(
                #     reflex.icon(
                #         'check',
                #         stroke_width = sticky.const.STROKE_BTN_ICON),
                #     side = 'right'),

