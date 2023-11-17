# -*- coding: utf-8 -*-
"""
---

title:
    "Theme asset preparation for FlowForge."

description:
    "This python module defines the theme
    asset preparation process for the FlowForge
    system."

id:
    "d943794a-aab0-409d-ac52-098936f4f801"

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


import os
import glob

import fl.asset
import fl.util.io
import fl.util.debug


# -----------------------------------------------------------------------------
def all_assets(rootpath_theme, rootpath_font, rootpath_icon):
    """
    Prepare all assets.

    """

    with fl.util.debug.rich_exception_printing_context():

        for (id_theme, cfg_theme) in _map_cfg_theme(rootpath_theme).items():

            fl.asset.prepare(cfg_theme,
                             rootpath_font,
                             rootpath_icon,
                             rootpath_theme)


# -----------------------------------------------------------------------------
def _map_cfg_theme(rootpath_theme):
    """
    Return a map of all theme configuration.

    """

    map_cfg = dict()
    for dirpath_theme in _subdirs(path = rootpath_theme):

        tup_filepath_theme = tuple(glob.glob(dirpath_theme + '/*.yaml'))

        assert len(tup_filepath_theme) == 1

        filepath_cfg        = tup_filepath_theme[0]
        (_, id_theme)       = os.path.split(dirpath_theme)
        (map_cfg[id_theme],
         map_error)         = fl.util.io.load_from_filepath(filepath_cfg)

        if map_error:
            raise map_error['exception']

        assert map_cfg[id_theme]['id_theme'] == id_theme

    return map_cfg


# -----------------------------------------------------------------------------
def _subdirs(path):
    """
    Return all the subdirectories of the specified path as a tuple.

    Ignore subdirectories that start with one or
    more underscores or periods.

    """

    return tuple((os.path.join(path, name) for name in os.listdir(path)
                                if     os.path.isdir(os.path.join(path, name))
                                   and not name.startswith('_')
                                   and not name.startswith('.')))
