# -*- coding: utf-8 -*-
"""
---

title:
    "Kazul app."

description:
    "Kazul app."

id:
    "a233eef4-8e7d-4330-921d-855bb10d1b75"

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

import kazul.component
import kazul.component.canvas
import kazul.component.command
import kazul.component.menu
import kazul.const
import kazul.state


# -----------------------------------------------------------------------------
@reflex.page(title   = kazul.const.NAME_APP,
             on_load = kazul.state.App.handle_page_index_on_load)
def index() -> reflex.Component:
    """
    Main page.

    """

    return reflex.fragment(
                # kazul.component.canvas.canvas(),
                kazul.component.command.command(),
                kazul.component.menu.menu())


# -----------------------------------------------------------------------------
style_background = 'linear-gradient(0deg, {rgb_lo}, {rgb_hi})'.format(
                                            rgb_lo = kazul.const.RGB_PASSIVE_BG,
                                            rgb_hi = kazul.const.RGB_PASSIVE_BG)
map_style_app    = dict(color       = kazul.const.RGB_PASSIVE_FG,
                        background  = style_background,
                        font_family = kazul.const.FONT,
                        spacing     = kazul.const.SIZE_ZERO,
                        padding     = kazul.const.SIZE_ZERO,
                        margin      = kazul.const.SIZE_ZERO,
                        resize      = 'none',
                        stylesheets = ['kazul.css'])
app = reflex.App(style = map_style_app)
