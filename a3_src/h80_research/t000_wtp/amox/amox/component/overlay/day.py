# -*- coding: utf-8 -*-
"""
---

title:
    "Day overlay UI components."

description:
    "This package defines UI components for
    the daily overview overlay."

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

import amox.component.button
import amox.const
import amox.state


# -----------------------------------------------------------------------------
def panel(**kwargs) -> reflex.Component:
    """
    Menu component with dark/light mode.

    """

    return reflex.center(
                reflex.card(

                    _panel_content(),

                    background   = reflex.cond(
                                            amox.state.App.is_ena_lightmode,
                                            amox.const.RGB_LT_BG_PASSIVE,
                                            amox.const.RGB_DK_BG_PASSIVE),

                    # position   = 'absolute',
                    # left       = amox.const.GUTTTER_DAY,
                    # right      = amox.const.GUTTTER_DAY,
                    # top        = amox.const.GUTTTER_DAY,
                    # bottom     = amox.const.GUTTTER_DAY_BOTTOM,

                    width        = '22rem',
                    height       = '90%',
                    border_color = 'black',
                    border       = 'thin'),
                **kwargs)


# -----------------------------------------------------------------------------
def _panel_content() -> reflex.Component:
    """
    """
    return reflex.fragment(
                reflex.heading('Achievements'),
                reflex.spacer(
                    height = amox.const.PADDING_TOPLEVEL),
                reflex.center(
                    reflex.vstack(
                        reflex.foreach(
                            amox.state.App.list_str_item,
                            _daily_item))),
                amox.component.button.button(
                    'Done',
                    on_click      = amox.state.App.on_toggle_overlay_day,
                    width         = amox.const.WIDTH_DAY_DONE_BTN,
                    height        = amox.const.HEIGHT_DAY_DONE_BTN,
                    border_radius = amox.const.RADIUS_BTN,
                    position      = 'absolute',
                    right         = amox.const.PADDING_TOPLEVEL,
                    bottom        = amox.const.PADDING_TOPLEVEL))


# -----------------------------------------------------------------------------
def _daily_item(str_item) -> reflex.Component:
    """
    Checkbox item component.

    """

    return reflex.card(
                reflex.flex(

                    amox.component.button.button(
                        str_item,
                        on_click      = functools.partial(
                                            amox.state.App.on_click_daily_item,
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

