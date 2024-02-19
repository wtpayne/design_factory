# -*- coding: utf-8 -*-
"""
---

title:
    "Kazul canvas UI components."

description:
    "This module defines the canvas UI component."

id:
    "083de365-7db0-4e39-b6a8-5831de139260"

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

import kazul.const
import kazul.state


# -----------------------------------------------------------------------------
def canvas() -> reflex.Component:
    """
    UI canvas component.

    Consists of a vertically stacked sequence of
    card components.

    """

    return reflex.vstack(
                reflex.box(
                    reflex.foreach(
                        kazul.state.App.list_work_item,
                        _work_item),
                    color        = kazul.const.RGB_PASSIVE_FG,
                    bg           = kazul.const.RGB_PASSIVE_BG,
                    padding      = kazul.const.PADDING_TOPLEVEL,
                    spacing      = kazul.const.SPACING_TOPLEVEL,
                    padding_left = kazul.const.SIZE_LEFT_GUTTER,
                    padding_top  = kazul.const.SIZE_COMMAND_GUTTER,
                    height       = kazul.const.SIZE_FULL,
                    width        = kazul.const.SIZE_FULL),
                width = kazul.const.SIZE_FULL)


# -----------------------------------------------------------------------------
def _work_item(work_item: kazul.state.WorkItem) -> reflex.Component:
    """
    Return an accordion component for a single work item.

    """

    return reflex.accordion(
                reflex.accordion_item(
                    _work_item_summary(work_item),
                    _work_item_content(work_item)),
                allow_toggle       = True,
                color              = kazul.const.RGB_PASSIVE_FG,
                bg                 = kazul.const.RGB_PASSIVE_BG_ACCENT,
                padding            = kazul.const.SIZE_ZERO,
                spacing            = kazul.const.SIZE_ZERO,
                margin             = '1rem',
                border_radius      = kazul.const.RADIUS_BDR,
                border_color       = kazul.const.RGB_PASSIVE_BG_ACCENT,
                focus_border_color = kazul.const.RGB_PASSIVE_BG_ACCENT,
                error_border_color = kazul.const.RGB_PASSIVE_BG_ACCENT,
                box_shadow         = kazul.const.CSS_ACTIVE_SHADOW)


# -----------------------------------------------------------------------------
def _work_item_summary(work_item: kazul.state.WorkItem) -> reflex.Component:
    """
    Return summary display components for a single work item.

    """

    return reflex.accordion_button(
                reflex.accordion_icon(),
                reflex.heading(work_item.title, size = 'sm'))


# -----------------------------------------------------------------------------
def _work_item_content(work_item: kazul.state.WorkItem) -> reflex.Component:
    """
    Return detailed content display components for a single work item.

    """

    return reflex.accordion_panel(
                reflex.foreach(
                    work_item.list_field,
                    _work_item_field))


# -----------------------------------------------------------------------------
def _work_item_field(field: kazul.state.WorkItemField) -> reflex.Component:
    """
    Work item field component.

    Consists of a styled box with some text in it.

    """

    return reflex.vstack(
                reflex.text(
                    field.name),
                reflex.text_area(
                    value               = field.content,
                    color               = kazul.const.RGB_ACTIVE_FG,
                    bg                  = kazul.const.RGB_ACTIVE_BG,
                    border_radius       = kazul.const.RADIUS_BDR,
                    border_color        = kazul.const.RGB_ACTIVE_BG_ACCENT,
                    focus_border_color  = kazul.const.RGB_ACTIVE_BG_ACCENT,
                    error_border_color  = kazul.const.RGB_ACTIVE_BG_ACCENT,
                    resize              = 'none',
                    on_change           = kazul.state.App.set_str_cmd_input,
                    on_blur             = kazul.state.App.set_str_cmd_input,
                    height              = kazul.const.SIZE_FULL,
                    style               = kazul.const.STYLE_ACTIVE_PLCHLDR),
                reflex.text_area(
                    value               = 'review',
                    color               = kazul.const.RGB_ACTIVE_FG,
                    bg                  = kazul.const.RGB_ACTIVE_BG,
                    border_radius       = kazul.const.RADIUS_BDR,
                    border_color        = kazul.const.RGB_ACTIVE_BG_ACCENT,
                    focus_border_color  = kazul.const.RGB_ACTIVE_BG_ACCENT,
                    error_border_color  = kazul.const.RGB_ACTIVE_BG_ACCENT,
                    resize              = 'none',
                    on_change           = kazul.state.App.set_str_cmd_input,
                    on_blur             = kazul.state.App.set_str_cmd_input,
                    height              = kazul.const.SIZE_FULL,
                    style               = kazul.const.STYLE_ACTIVE_PLCHLDR),
                align_items = 'left',
                margin  = '1rem')
