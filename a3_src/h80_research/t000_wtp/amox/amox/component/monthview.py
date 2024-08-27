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
                        _daybox),

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
    Text for the month view heading row.

    This is normally day-of-week column headers.

    """

    return reflex.text(
                str_item,
                color = reflex.cond(amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE))


# -----------------------------------------------------------------------------
def _daybox(idx: int) -> reflex.Component:
    """
    Monthview day-box component.

    """

    return reflex.match(
                amox.state.App.list_day_type[idx],
                ('inactive', _daybox_inactive()),
                ('past',     _daybox_past(idx)),
                ('today',    _daybox_today(idx)),
                ('future',   _daybox_future(idx)))


# -----------------------------------------------------------------------------
def _daybox_inactive() -> reflex.Component:
    """
    Inactive, hidden day-box component.

    """

    return reflex.box(
                background    = reflex.cond(amox.state.App.is_ena_lightmode,
                                            amox.const.RGB_LT_BG_PASSIVE,
                                            amox.const.RGB_DK_BG_PASSIVE),
                border_color  = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                border        = 'thin',
                border_radius = amox.const.RADIUS_DAYBOX,
                width         = amox.const.SIZE_FULL)


# -----------------------------------------------------------------------------
def _daybox_past(idx: int) -> reflex.Component:
    """
    A day-box for past dates.

    """

    return _daybox_active_impl(
                idx,
                on_click = lambda: amox.state.App.on_click_mv_day_past(idx))


# -----------------------------------------------------------------------------
def _daybox_today(idx: int) -> reflex.Component:
    """
    The day-box for today's date.

    """

    return _daybox_active_impl(
                idx,
                on_click   = lambda: amox.state.App.on_click_mv_today(idx),
                background = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_BG_PASSIVE_ACCENT_2,
                                    amox.const.RGB_DK_BG_PASSIVE_ACCENT_2))


# -----------------------------------------------------------------------------
def _daybox_future(idx: int) -> reflex.Component:
    """
    A day-box for future dates.

    """

    return _daybox_active_impl(
                idx,
                on_click = lambda: amox.state.App.on_click_mv_day_future(idx))


# -----------------------------------------------------------------------------
def _daybox_active_impl(idx: int, *args, **kwargs) -> reflex.Component:
    """
    The implementation for all active day-box compoennts.

    """

    map_properties = dict(
                direction     = 'column',
                justify       = 'start',
                align         = 'center',
                flex_grow     = 1,
                flex_shrink   = 1,
                background    = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_BG_PASSIVE_ACCENT_1,
                                    amox.const.RGB_DK_BG_PASSIVE_ACCENT_1),
                border_color  = reflex.cond(
                                    amox.state.App.is_ena_lightmode,
                                    amox.const.RGB_LT_FG_PASSIVE,
                                    amox.const.RGB_DK_FG_PASSIVE),
                position      = 'static',
                border        = 'thin',
                border_radius = amox.const.RADIUS_DAYBOX,
                padding       = amox.const.PADDING_DAYBOX,
                width         = amox.const.SIZE_FULL)

    map_properties.update(kwargs)

    return reflex.flex(
                _daybox_date(idx),
                _daybox_content(idx),
                **map_properties)


# -----------------------------------------------------------------------------
def _daybox_date(idx: int) -> reflex.Component:
    """
    Date text on a day box.

    """

    return reflex.text(
                amox.state.App.list_day_of_month[idx],
                color      = reflex.cond(
                                amox.state.App.is_ena_lightmode,
                                amox.const.RGB_LT_FG_PASSIVE,
                                amox.const.RGB_DK_FG_PASSIVE),
                text_align = 'right',
                size       = amox.const.SIZE_TEXT_DAYBOX,
                width      = amox.const.SIZE_FULL),


# -----------------------------------------------------------------------------
def _daybox_content(idx: int) -> reflex.Component:
    """
    Content of a day box.

    https://lucide.dev/icons/categories#files

    """

    return reflex.match(
                amox.state.App.list_day_icon[idx],
                ('folder_plus',     _daybox_icon('folder_plus')),
                ('folder_sync',     _daybox_icon('folder_sync')),
                ('folder_pen',      _daybox_icon('folder_pen')),
                ('folder_open',     _daybox_icon('folder_open')),
                ('folder_open_dot', _daybox_icon('folder_open_dot')),
                ('folder_closed',   _daybox_icon('folder_closed')),
                ('folder_key',      _daybox_icon('folder_key')),
                ('folder_lock',     _daybox_icon('folder_lock')),
                ('folder_x',        _daybox_icon('folder_x')),
                ('triangle_alert',  _daybox_icon('triangle_alert')),
                ('folders',         _daybox_icon('folders')),
                ('file_stack',      _daybox_icon('file_stack')),
                ('videotape',       _daybox_icon('videotape')),
                ('none',            reflex.spacer()),
                _daybox_icon('circle_help'))



# -----------------------------------------------------------------------------
def _daybox_icon(str_tag: str, **kwargs) -> reflex.Component:
    """
    Icon on a month card.

    """

    return reflex.icon(
                    str_tag,
                    size         = amox.const.SIZE_ICON_DAYBOX,
                    stroke_width = amox.const.STROKE_ICON_DAYBOX,
                    color        = reflex.cond(
                                        amox.state.App.is_ena_lightmode,
                                        amox.const.RGB_LT_FG_PASSIVE,
                                        amox.const.RGB_DK_FG_PASSIVE),
                    flex_grow = 1)

