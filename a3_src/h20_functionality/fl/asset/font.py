# -*- coding: utf-8 -*-
"""
---

title:
    "Font asset module."

description:
    "This python module defines functions
    for preparing font assets."

id:
    "beffb9cd-642a-42b8-a6e6-7d67cd2737aa"

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

...
"""


import os.path
import shutil


# -----------------------------------------------------------------------------
def prepare(rootpath_font,
            relpath_font,
            rootpath_theme,
            id_theme,
            id_font):
    """
    Copy and rename the specified font to the theme asset directory.

    """

    filepath_src = os.path.join(rootpath_font, relpath_font)
    dirpath_dst  = os.path.join(rootpath_theme, id_theme)
    filename_dst = '{id_font}.ttf'.format(id_font = id_font)
    filepath_dst = os.path.join(dirpath_dst, filename_dst)

    shutil.copy(filepath_src, filepath_dst)
