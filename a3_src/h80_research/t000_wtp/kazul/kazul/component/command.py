# -*- coding: utf-8 -*-
"""
---

title:
    "Kazul command UI components."

description:
    "This package defines the command bar UI
    component."

id:
    "f4fd7348-7961-46fd-9417-1017ee9ed276"

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
def command() -> reflex.Component:
    """
    Command bar component.

    This is the bar that runs across the very
    top of each page that allows you to send
    commands to the application.

    It consists of a visible part for the
    input itself, and an invisible component
    that enables it to be positioned correctly.

    """

    return reflex.hstack(

                # Padding the width of the menu.
                #
                reflex.box(
                    height    = kazul.const.SIZE_FULL,
                    min_width = kazul.const.SIZE_LEFT_NAVIGATION),

                # The visible-to-the-user bit in
                # the middle with the input and
                # the buttons.
                #
                reflex.center(
                    _visible_input_bar(),
                    height = kazul.const.SIZE_FULL,
                    width  = kazul.const.SIZE_FULL),

                bg            = 'transparent',
                width         = kazul.const.SIZE_FULL,
                height        = kazul.const.SIZE_COMMAND_BAR,
                position      = 'fixed',
                top           = kazul.const.PADDING_TOPLEVEL)


# -----------------------------------------------------------------------------
def _visible_input_bar() -> reflex.Component:
    """
    Command input component.

    This is the visible part of the bar that
    runs across the very bottom of each page.

    It consists of an input component and
    a submit button.

    """

    icon_submit = reflex.icon(tag = 'chevron_right')

    input_usr = reflex.input(
                    placeholder         = f'Type to search...',
                    name                = 'input',
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
                    style               = kazul.const.STYLE_ACTIVE_PLCHLDR)

    btn_submit = reflex.button(
                    icon_submit,
                    type_               = 'submit',
                    color_scheme        = 'whiteAlpha',
                    color               = kazul.const.RGB_ACTIVE_BTN_FG,
                    border_radius       = kazul.const.RADIUS_BTN,
                    bg                  = kazul.const.RGB_ACTIVE_BTN,
                    width               = kazul.const.WIDTH_BTN_SUBMIT,
                    height              = kazul.const.HEIGHT_BTN_SUBMIT)

    elem_right = reflex.InputRightElement(
                    children            = [btn_submit],
                    padding             = kazul.const.PADDING_CHAT_INPUT,
                    spacing             = kazul.const.SPACING_CHAT_INPUT,
                    width               = kazul.const.WIDTH_RIGHT_ELEMENT,
                    height              = kazul.const.SIZE_FULL,
                    padding_right       = kazul.const.PAD_RIGHT_BTN_SUBMIT)

    inputgroup_usr = reflex.InputGroup(
                    children            = [input_usr, elem_right],
                    height              = kazul.const.SIZE_FULL,
                    width               = kazul.const.SIZE_FULL,
                    padding             = kazul.const.PADDING_CHAT_INPUT,
                    spacing             = kazul.const.SPACING_CHAT_INPUT,
                    border_radius       = kazul.const.RADIUS_BDR,
                    border_width        = kazul.const.BORDER_CHAT_INPUT,
                    border_color        = kazul.const.RGB_ACTIVE_BORDER,
                    bg                  = kazul.const.RGB_ACTIVE_BG,
                    style               = kazul.const.STYLE_ACTIVE_OPACITY,
                    box_shadow          = kazul.const.CSS_ACTIVE_SHADOW)

    return reflex.form(
                    inputgroup_usr,
                    on_submit           = kazul.state.App.handle_btn_cmd_submit,
                    reset_on_submit     = True,
                    height              = kazul.const.SIZE_FULL,
                    width               = kazul.const.PERCENT_WIDTH_CHAT)
