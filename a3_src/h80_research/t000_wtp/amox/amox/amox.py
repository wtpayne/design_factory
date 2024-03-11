# -*- coding: utf-8 -*-
"""
---

title:
    "AMOX configurable web application."

description:
    "AMOX configurable web application."

id:
    "739415a8-0f51-4355-9f86-46d9d661caef"

type:
    dt001_python_script

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

import amox.component
import amox.component.overlay.day
import amox.component.overlay.settings
import amox.component.menubar
import amox.component.monthview
import amox.component.navigation
import amox.const
import amox.state


# -----------------------------------------------------------------------------
@reflex.page(title   = amox.const.NAME_APP,
             on_load = amox.state.App.handle_page_index_on_load)
def index() -> reflex.Component:
    """
    Main page.

    """

    return reflex.fragment(

                reflex.match(
                    amox.state.App.str_type_overlay,
                    ('NONE',        reflex.box(display = 'none')),
                    ('DAY',         amox.component.overlay.day.panel(
                                        background = amox.const.RGBA_DIMMING,
                                        position   = 'absolute',
                                        z_index    = '5',
                                        left       = amox.const.SIZE_ZERO,
                                        right      = amox.const.SIZE_ZERO,
                                        top        = amox.const.SIZE_ZERO,
                                        bottom     = amox.const.SIZE_MENUBAR)),
                    ('SETTINGS',    amox.component.overlay.settings.panel(
                                        background = amox.const.RGBA_DIMMING,
                                        position   = 'absolute',
                                        z_index    = '5',
                                        left       = amox.const.SIZE_ZERO,
                                        right      = amox.const.SIZE_ZERO,
                                        top        = amox.const.SIZE_ZERO,
                                        bottom     = amox.const.SIZE_MENUBAR)),
                    reflex.text('BAD TYPE FOR OVERLAY')),

                reflex.vstack(

                    amox.component.navigation.navigation(
                        flex       = 'none',
                        zindex     = '0',
                        width      = amox.const.SIZE_FULL,
                        height     = amox.const.SIZE_NAV_BAR,
                        padding    = amox.const.PADDING_TOPLEVEL),

                    amox.component.monthview.monthview(
                        flex       = 'auto',
                        zindex     = '0',
                        width      = amox.const.SIZE_FULL,
                        height     = amox.const.SIZE_FULL,
                        padding    = amox.const.PADDING_TOPLEVEL,
                        margin     = amox.const.SIZE_ZERO,
                        style      = { 'max-width':  amox.const.SIZE_FULL,
                                       'max-height': amox.const.SIZE_FULL }),

                    amox.component.menubar.menubar(
                        flex       = 'none',
                        zindex     = '10',
                        width      = amox.const.SIZE_FULL,
                        height     = amox.const.SIZE_MENUBAR,
                        padding    = amox.const.PADDING_TOPLEVEL),

                    width      = '100%',
                    height     = '100vh',
                    background = reflex.cond(amox.state.App.is_ena_lightmode,
                                             amox.const.RGB_LT_BG_PASSIVE,
                                             amox.const.RGB_DK_BG_PASSIVE)))


# -----------------------------------------------------------------------------
style_background = 'linear-gradient(0deg, {rgb_lo}, {rgb_hi})'.format(
                                rgb_lo = amox.const.RGB_LT_BG_PASSIVE,
                                rgb_hi = amox.const.RGB_LT_BG_PASSIVE_ACCENT)
map_style_app    = dict(color       = reflex.cond(
                                            amox.state.App.is_ena_lightmode,
                                            amox.const.RGB_LT_FG_PASSIVE,
                                            amox.const.RGB_DK_FG_PASSIVE),
                        background  = style_background,
                        font_family = amox.const.FONT,
                        spacing     = amox.const.SIZE_ZERO,
                        padding     = amox.const.SIZE_ZERO,
                        margin      = amox.const.SIZE_ZERO,
                        resize      = 'none',
                        stylesheets = ['amox.css'])
app = reflex.App(style = map_style_app)
