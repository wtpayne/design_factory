# -*- coding: utf-8 -*-
"""
---

title:
    "Kazul constants."

description:
    "Constants for the Kazul application."

id:
    "eada606d-0730-4937-ad42-b563921b886e"

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


NAME_APP:                   str = 'Kazul'

RGB_WHITE:                  str = '#FFFFFF'
RGB_BLACK:                  str = '#000000'

# Tahiti Gold palette.
#
RGB_LINEN:                  str = '#FDF1E5'
RGB_TEQUILA:                str = '#FCE3CC'
RGB_LIGHT_APRICOT:          str = '#FAD6B3'
RGB_PEACH_ORANGE:           str = '#F9C89A'
RGB_PEACH:                  str = '#F7BB82'
RGB_APRICOT:                str = '#F6AD6A'
RGB_PASTEL_ORANGE:          str = '#F4A052'
RGB_FADED_ORANGE:           str = '#F3933A'
RGB_CADMIUM_ORANGE:         str = '#F18723'
RGB_TAHITI_GOLD:            str = '#EF780B'
RGB_BAMBOO:                 str = '#D86E0B'
RGB_ORANGE_BROWN:           str = '#C0620A'
RGB_RICH_GOLD:              str = '#A85508'
RGB_MEDIUM_BROWN:           str = '#904907'
RGB_RED_BEECH:              str = '#783D06'
RGB_CARNABY_TAN:            str = '#603105'
RGB_INDIAN_TAN:             str = '#482504'
RGB_DARK_BROWN:             str = '#301802'
RGB_ASPHALT:                str = '#180C01'

# Viridian palette
#
RGB_HARP:                   str = '#E6F4ED'
RGB_SURF_CREST:             str = '#CFE8DC'
RGB_SEA_MIST:               str = '#B8DDCC'
RGB_TURQUOISE_GREEN:        str = '#A3D1BC'
RGB_SHADOW_GREEN:           str = '#8FC6AC'
RGB_GULF_STREAM:            str = '#7DBA9D'
RGB_SILVER_TREE:            str = '#6BAF8F'
RGB_AQUA_FOREST:            str = '#5BA382'
RGB_DUSTY_TEAL:             str = '#4D9875'
RGB_VIRIDIAN:               str = '#3F8B68'
RGB_VIRIDIAN_SHADE:         str = '#397E5E'
RGB_DARK_GREEN_BLUE:        str = '#327053'
RGB_GREEN_PEA:              str = '#2C6249'
RGB_PLANTATION:             str = '#26543F'
RGB_EVERGLADE:              str = '#204634'
RGB_MEDIUM_JUNGLE_GREEN:    str = '#19382A'
RGB_BUSH:                   str = '#132A1F'
RGB_RACING_GREEN:           str = '#0D1C15'
RGB_ALMOST_BLACK:           str = '#060E0A'

# Dusty orange palette
#
RGB_DUSTY_ORANGE:           str = '#F18446'

# Brand color scheme.
#
RGB_BRAND_TINT_09:          str = RGB_HARP
RGB_BRAND_TINT_08:          str = RGB_SURF_CREST
RGB_BRAND_TINT_07:          str = RGB_SEA_MIST
RGB_BRAND_TINT_06:          str = RGB_TURQUOISE_GREEN
RGB_BRAND_TINT_05:          str = RGB_SHADOW_GREEN
RGB_BRAND_TINT_04:          str = RGB_GULF_STREAM
RGB_BRAND_TINT_03:          str = RGB_SILVER_TREE
RGB_BRAND_TINT_02:          str = RGB_AQUA_FOREST
RGB_BRAND_TINT_01:          str = RGB_DUSTY_TEAL
RGB_BRAND:                  str = RGB_VIRIDIAN
RGB_BRAND_SHADE_01:         str = RGB_VIRIDIAN_SHADE
RGB_BRAND_SHADE_02:         str = RGB_DARK_GREEN_BLUE
RGB_BRAND_SHADE_03:         str = RGB_GREEN_PEA
RGB_BRAND_SHADE_04:         str = RGB_PLANTATION
RGB_BRAND_SHADE_05:         str = RGB_EVERGLADE
RGB_BRAND_SHADE_06:         str = RGB_MEDIUM_JUNGLE_GREEN
RGB_BRAND_SHADE_07:         str = RGB_BUSH
RGB_BRAND_SHADE_08:         str = RGB_RACING_GREEN
RGB_BRAND_SHADE_09:         str = RGB_ALMOST_BLACK

# Color scheme for passive information display elements.
#
RGB_PASSIVE_BG:             str  = RGB_BRAND_TINT_09
RGB_PASSIVE_BG_ACCENT:      str  = RGB_BRAND_TINT_03
RGB_PASSIVE_FG:             str  = RGB_BRAND_SHADE_08

# Color scheme for interactive UI control elements.
#
RGB_ACTIVE_BORDER:          str = RGB_BRAND_SHADE_03
RGB_ACTIVE_BG:              str = RGB_BRAND
RGB_ACTIVE_BG_ACCENT:       str = RGB_BRAND_SHADE_01
RGB_ACTIVE_FG:              str = RGB_BRAND_SHADE_08
RGB_ACTIVE_FG_MUTED:        str = RGB_BRAND_SHADE_05
RGB_ACTIVE_BTN_ALT:         str = RGB_BRAND_SHADE_01
RGB_ACTIVE_BTN:             str = RGB_BRAND_SHADE_02
RGB_ACTIVE_BTN_FG:          str = RGB_BRAND_SHADE_09

# Styles and custome CSS for interactive UI control elements.
#
STYLE_ACTIVE_OPACITY:       dict = { 'opacity':          '0.95',
                                     'backdrop-filter':  'blur(6px)' }
STYLE_ACTIVE_PLCHLDR:       dict = { '::placeholder': {
                                             'color':    RGB_ACTIVE_FG_MUTED,
                                             'opacity':  1 } }
CSS_ACTIVE_SHADOW:          str  = 'rgba(0, 0, 0, 0.95) 0px 2px 8px'

# Layout and sizing (toplevel)
#
SIZE_ZERO:                  str = '0rem'
SIZE_FULL:                  str = '100%'
SPACING_TOPLEVEL:           str = '1rem'
PADDING_TOPLEVEL:           str = '1rem'
MARGIN_TOPLEVEL:            str = SIZE_ZERO
FONT:                       str = 'sans-serif'
RADIUS_BDR:                 str = '0.5rem'
RADIUS_BTN:                 str = '0.5rem'

# Layout and sizing (canvas)
#
BORDER_RADIUS_USR:          str = '0.5rem'
PADDING_LEFT_LLM:           str = '1rem'
PADDING_LEFT_USR:           str = '1rem'
PADDING_RIGHT_USR:          str = '1rem'
PADDING_TOP_USR:            str = '0.25rem'
PADDING_BOTTOM_USR:         str = '0.25rem'
MARGIN_TOP_USR:             str = '0.25rem'
MARGIN_BOTTOM_USR:          str = '0.25rem'
MARGIN_LEFT_USR:            str = '0rem'

# Layout and sizing (navigation)
#
SIZE_LEFT_GUTTER:           str = '15rem'
SIZE_LEFT_NAVIGATION:       str = '14rem'
SIZE_LEFT_BTN:              str = '12rem'

# Layout and sizing (chat)
#
SIZE_COMMAND_BAR:           str = '4.0rem'
SIZE_COMMAND_GUTTER:        str = '7.0rem'
PERCENT_WIDTH_CHAT:         str = '80%'
MARGIN_CHAT_INPUT:          str = SIZE_ZERO
BORDER_CHAT_INPUT:          str = 'thin'
SPACING_CHAT_INPUT:         str = '0.4rem'
PADDING_CHAT_INPUT:         str = '0.4rem'
WIDTH_RIGHT_ELEMENT:        str = '3.5rem'
WIDTH_BTN_SUBMIT:           str = '1.7rem'
HEIGHT_BTN_SUBMIT:          str = '1.7rem'
PAD_RIGHT_BTN_SUBMIT:       str = '1.7rem'

