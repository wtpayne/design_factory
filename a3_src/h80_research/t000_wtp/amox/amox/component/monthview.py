# -*- coding: utf-8 -*-
"""
---

title:
    "Amox monthview UI components."

description:
    "This package defines the monthview UI
    component for the Amox app."

id:
    "da9cd82e-6069-420f-8ba3-ccb4fa6469eb"

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

import amox.const
import amox.state


# -----------------------------------------------------------------------------
def monthview(**kwargs) -> reflex.Component:
    """
    Monthview component.

    """

    TUP_WEEKDAY:   tuple[str] = ( 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su' )
    COUNT_WEEKDAY: str        = str(len(TUP_WEEKDAY))
    MAX_WEEKS:     str        = '6'

    return reflex.vstack(

                _heading_row(
                    tup_heading = TUP_WEEKDAY),

                reflex.grid(
                    reflex.foreach(
                        amox.state.App.list_idx_day,
                        _month_card),

                    flex    = 'auto',
                    width   = amox.const.SIZE_FULL,
                    height  = amox.const.SIZE_FULL,
                    padding = amox.const.SIZE_ZERO,
                    spacing = '2',
                    rows    = MAX_WEEKS,
                    columns = COUNT_WEEKDAY,
                    flow    = 'row'),

                **kwargs)


# -----------------------------------------------------------------------------
def _heading_row(tup_heading) -> reflex.Component:
    """
    Heading row for the month view.

    """

    return reflex.hstack(
                reflex.foreach(
                    tup_heading,
                    reflex.text),
                width    = amox.const.SIZE_FULL,
                style    = { 'justify-content': 'space-around' },
                padding  = '0rem')


# -----------------------------------------------------------------------------
def _month_card(idx: int) -> reflex.Component:
    """
    Month card component.

    """

    return reflex.cond(
                amox.state.App.list_do_render[idx],
                _month_card_in_month(idx),
                _month_card_out_of_month())


# -----------------------------------------------------------------------------
def _month_card_in_month(idx: int) -> reflex.Component:
    """
    Month card (in month) component.

    """

    return reflex.card(
                reflex.text(
                    amox.state.App.list_day_of_month[idx],
                    color = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                    size  = '1',
                    style = { 'position': 'absolute',
                              'top':      '0.5rem',
                              'right':    '0.5rem' }),
                    reflex.cond(
                        amox.state.App.list_has_icon[idx],
                        reflex.center(
                            reflex.icon(
                                'smile',
                                size         = 50,
                                flex         = '0 1 auto',
                                stroke_width = amox.const.STROKE_CARD_ICON,
                                color        = amox.const.RGB_CARD_ICON),
                            width  = '100%',
                            height = '100%'),
                        reflex.spacer()),
                on_click      = lambda: amox.state.App.on_click_month(idx),
                background    = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_BG_PASSIVE_ACCENT,
                                    amox.const.RGB_DK_BG_PASSIVE_ACCENT),
                border_color  = 'black',
                border        = 'thin',
                width         = amox.const.SIZE_FULL)


# -----------------------------------------------------------------------------
def _month_card_out_of_month() -> reflex.Component:
    """
    Month card (in month) component.

    """

    return reflex.card(
                background    = reflex.cond(amox.state.App.is_ena_lightmode,
                                            amox.const.RGB_LT_BG_PASSIVE,
                                            amox.const.RGB_DK_BG_PASSIVE),
                border_color  = 'black',
                border        = 'thin',
                width         = amox.const.SIZE_FULL)
