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
                    _heading_text),
                width    = amox.const.SIZE_FULL,
                style    = { 'justify-content': 'space-around' },
                padding  = '0rem')


# -----------------------------------------------------------------------------
def _heading_text(str_item) -> reflex.Component:
    """
    """
    return reflex.text(
                str_item,
                color = reflex.cond(amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE))


# -----------------------------------------------------------------------------
def _month_card(idx: int) -> reflex.Component:
    """
    Month card component.

    """

    return reflex.match(
                amox.state.App.list_day_type[idx],
                ('inactive', _mv_card_day_inactive()),
                ('past',     _mv_card_day_past(idx)),
                ('today',    _mv_card_day_today(idx)),
                ('future',   _mv_card_day_future(idx)))


# -----------------------------------------------------------------------------
def _mv_card_day_inactive() -> reflex.Component:
    """
    Month card (in month) component.

    """

    return reflex.card(
                background    = reflex.cond(amox.state.App.is_ena_lightmode,
                                            amox.const.RGB_LT_BG_PASSIVE,
                                            amox.const.RGB_DK_BG_PASSIVE),
                border_color  = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                border        = 'thin',
                width         = amox.const.SIZE_FULL)


# -----------------------------------------------------------------------------
def _mv_card_day_past(idx: int) -> reflex.Component:
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

                    _month_card_icon(
                        tag_icon = amox.state.App.list_str_icon[idx]),

                on_click      = lambda: amox.state.App.on_click_mv_day_past(idx),
                background    = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_BG_PASSIVE_ACCENT_1,
                                    amox.const.RGB_DK_BG_PASSIVE_ACCENT_1),
                border_color  = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                border        = 'thin',
                width         = amox.const.SIZE_FULL)


# -----------------------------------------------------------------------------
def _mv_card_day_today(idx: int) -> reflex.Component:
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

                    _month_card_icon(
                        tag_icon = amox.state.App.list_str_icon[idx]),

                on_click      = lambda: amox.state.App.on_click_mv_today(idx),
                background    = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_BG_PASSIVE_ACCENT_2,
                                    amox.const.RGB_DK_BG_PASSIVE_ACCENT_2),
                border_color  = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                border        = 'thin',
                width         = amox.const.SIZE_FULL)


# -----------------------------------------------------------------------------
def _mv_card_day_future(idx: int) -> reflex.Component:
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

                    _month_card_icon(
                        tag_icon = amox.state.App.list_str_icon[idx]),

                on_click      = lambda: amox.state.App.on_click_mv_day_future(idx),
                background    = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_BG_PASSIVE_ACCENT_1,
                                    amox.const.RGB_DK_BG_PASSIVE_ACCENT_1),
                border_color  = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                border        = 'thin',
                width         = amox.const.SIZE_FULL)

# -----------------------------------------------------------------------------
def _month_card_icon(tag_icon: str) -> reflex.Component:
    """
    """
    return reflex.match(
                tag_icon,
                ('smile', _specific_month_card_icon('smile')),
                reflex.spacer())

# -----------------------------------------------------------------------------
def _specific_month_card_icon(tag_icon: str) -> reflex.Component:
    """
    """
    return reflex.center(
                reflex.icon(
                    tag_icon,
                    size         = 50,
                    flex         = '0 1 auto',
                    stroke_width = amox.const.STROKE_CARD_ICON,
                    color        = amox.const.RGB_CARD_ICON),
                width  = '100%',
                height = '100%')