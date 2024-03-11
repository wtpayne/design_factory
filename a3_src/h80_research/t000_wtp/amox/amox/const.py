# -*- coding: utf-8 -*-
"""
---

title:
    "Amox constants."

description:
    "Constants for the Amox application."

id:
    "86fda7db-e782-4e67-84d9-b53b80c97d50"

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


import os
import os.path

import yaml


# -----------------------------------------------------------------------------
# Load theme/style configuration
#
config = os.environ.get('AMOX_CONFIG', 'default.cfg.yaml')
if os.path.isfile(config):
    filepath_cfg = config
else:
    filename_cfg = config
    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    relpath_cfg  = './cfg'
    dirpath_cfg  = os.path.normpath(os.path.join(dirpath_self, relpath_cfg))
    filepath_cfg = os.path.join(dirpath_cfg, filename_cfg)
with open(filepath_cfg, 'rt') as file_cfg:
    map_cfg = yaml.safe_load(file_cfg)
locals().update(map_cfg)

# Light/dark scheme for passive information display elements.
#
RGB_LT_BG_PASSIVE:         str = LT_BG
RGB_LT_BG_PASSIVE_ACCENT:  str = LT_BG_S1
RGB_LT_FG_PASSIVE:         str = LT_FG

RGB_DK_BG_PASSIVE:         str = DK_BG
RGB_DK_BG_PASSIVE_ACCENT:  str = DK_BG_T1
RGB_DK_FG_PASSIVE:         str = DK_FG

# Light/dark mode color scheme.
#
RGB_LT_BG_ACTIVE_BTN:      str = LT_BG_S2
RGB_LT_FG_ACTIVE_BTN:      str = LT_FG

RGB_DK_BG_ACTIVE_BTN:      str = DK_BG_T2
RGB_DK_FG_ACTIVE_BTN:      str = DK_FG_S1

# Drop shadows and transparent overlay opacities.
#
RGBA_DIMMING:              str = 'rgba(0, 0, 0, 0.60)'


# Layout and sizing (toplevel).
#
SIZE_ZERO:                 str = '0rem'
SIZE_FULL:                 str = '100%'
FONT:                      str = 'sans-serif'
RADIUS_BTN:                str = '0.5rem'
PADDING_TOPLEVEL:          str = '0.5rem'
MARGIN_TOPLEVEL:           str = '0.0rem'

# Layout and sizing (Menu bar).
#
SIZE_MENUBAR:              str = '3.5rem'
SIZE_MENUBAR_BTN:          str = '2.5rem'

# Layout and sizing (Main menu).
#
SIZE_MAINMENU:             str = '12.5rem'
SIZE_MAINMENU_BTN:         str = '3.5rem'
SIZE_MAINMENU_ICON:        str = '2.5rem'
SIZE_MAINMENU_PAD_LEFT:    str = '0.5rem'

# Layout and sizing (Navigation bar).
#
SIZE_NAV_BAR:              str = '2.5rem'
SIZE_NAV_BTN:              str = '2.5rem'
WIDTH_NAV_SELECT:          str = '7rem'
STROKE_BTN_ICON:           int = 2

# Layout and sizing (Monthview).
#
RADIUS_CARD:               str = '0.5rem'
STROKE_CARD_ICON:          int = 3
RGB_CARD_ICON:             str = 'red' # RGB_LT_FG_ACTIVE_BTN  # !!!!!!!!!!

# Layout and sizing (Day overlay).
#
GUTTTER_DAY:               str = '1.0rem'
GUTTTER_DAY_BOTTOM:        str = '1.6rem'
WIDTH_DAY_DONE_BTN:        str = '8rem'
HEIGHT_DAY_DONE_BTN:       str = '3rem'

