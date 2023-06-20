# -*- coding: utf-8 -*-
"""
---

title:
    "Asset preparation functionality package."

description:
    "This python package defines functions
    for preparing assets of various types."

id:
    "aee50d19-fb30-46a5-b53b-88834b9b1193"

type:
    dt002_python_package

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

...
"""


import fl.asset.font
import fl.asset.icon


# -----------------------------------------------------------------------------
def prepare(map_cfg_theme,
            rootpath_font,
            rootpath_icon,
            rootpath_theme):
    """
    Prepare all assets, creating files in the theme directory as needed.

    """

    for (id_font, cfg_font) in map_cfg_theme['font'].items():
        fl.asset.font.prepare(rootpath_font  = rootpath_font,
                              rootpath_theme = rootpath_theme,
                              id_theme       = map_cfg_theme['id_theme'],
                              id_font        = id_font,
                              relpath_font   = cfg_font['relpath'])

    for (id_icon, cfg_icon) in map_cfg_theme['icon'].items():
        fl.asset.icon.prepare(rootpath_icon  = rootpath_icon,
                              rootpath_theme = rootpath_theme,
                              id_theme       = map_cfg_theme['id_theme'],
                              id_icon        = id_icon,
                              id_family      = cfg_icon['id_family'],
                              color_fill     = cfg_icon['color_fill'],
                              width_tgt      = cfg_icon['width_tgt'],
                              height_tgt     = cfg_icon['height_tgt'])
