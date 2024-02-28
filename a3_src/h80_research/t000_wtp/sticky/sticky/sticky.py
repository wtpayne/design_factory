# -*- coding: utf-8 -*-
"""
---

title:
    "Sticky app."

description:
    "Sticky app."

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

import sticky.component
import sticky.component.menubar
import sticky.component.monthview
import sticky.component.navigation
import sticky.const
import sticky.state


# -----------------------------------------------------------------------------
@reflex.page(title   = sticky.const.NAME_APP,
             on_load = sticky.state.App.handle_page_index_on_load)
def index() -> reflex.Component:
    """
    Main page.

    """

    return reflex.fragment(
                reflex.vstack(

                    sticky.component.navigation.navigation(
                        flex       = 'none',
                        zindex     = '0',
                        width      = sticky.const.SIZE_FULL,
                        height     = sticky.const.SIZE_NAV_BAR,
                        padding    = sticky.const.PADDING_TOPLEVEL),

                    sticky.component.monthview.monthview(
                        flex       = 'auto',
                        width      = sticky.const.SIZE_FULL,
                        height     = sticky.const.SIZE_FULL,
                        padding    = sticky.const.PADDING_TOPLEVEL,
                        style      = { 'max-width':  sticky.const.SIZE_FULL,
                                       'max-height': sticky.const.SIZE_FULL }),

                    sticky.component.menubar.menubar(
                        flex       = 'none',
                        width      = sticky.const.SIZE_FULL,
                        height     = sticky.const.SIZE_MENU_BAR,
                        padding    = sticky.const.PADDING_TOPLEVEL),

                    width      = '100%',
                    height     = '100vh',
                    background = reflex.cond(sticky.state.App.is_lightmode,
                                             sticky.const.RGB_LT_BG_PASSIVE,
                                             sticky.const.RGB_DK_BG_PASSIVE)))


# -----------------------------------------------------------------------------
style_background = 'linear-gradient(0deg, {rgb_lo}, {rgb_hi})'.format(
                                        rgb_lo = sticky.const.RGB_PASSIVE_BG,
                                        rgb_hi = sticky.const.RGB_PASSIVE_BG)
map_style_app    = dict(color       = sticky.const.RGB_PASSIVE_FG,
                        background  = style_background,
                        font_family = sticky.const.FONT,
                        spacing     = sticky.const.SIZE_ZERO,
                        padding     = sticky.const.SIZE_ZERO,
                        margin      = sticky.const.SIZE_ZERO,
                        resize      = 'none',
                        stylesheets = ['sticky.css'])
app = reflex.App(style = map_style_app)
