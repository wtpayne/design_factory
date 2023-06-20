# -*- coding: utf-8 -*-
"""
---

title:
    "Icon asset module."

description:
    "This python module defines functions
    for preparing icon assets."

id:
    "90c17f60-a831-4528-8826-8d7fde8ccb2f"

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
import tempfile

import cairosvg
import PIL.Image
import xml.etree.ElementTree


# -----------------------------------------------------------------------------
def prepare(rootpath_icon,
            rootpath_theme,
            id_theme,
            id_icon,
            id_family,
            color_fill,
            width_tgt,
            height_tgt):
    """
    Prepare the specified icon, changing the color, size and saving the file.

    """

    dirpath_svg  = os.path.join(rootpath_icon, id_family)
    filename_svg = '{id_icon}.svg'.format(id_icon = id_icon)
    filepath_svg = os.path.join(dirpath_svg, filename_svg)
    tree_xml_svg = xml.etree.ElementTree.parse(filepath_svg)

    _rewrite_tree_xml_svg(tree_xml_svg = tree_xml_svg,
                          color_fill   = color_fill,
                          width_tgt    = width_tgt,
                          height_tgt   = height_tgt)

    dirpath_theme = os.path.join(rootpath_theme, id_theme)
    filename_png  = '{id_icon}.png'.format(id_icon = id_icon)
    filepath_png  = os.path.join(dirpath_theme, filename_png)

    _render_svg_and_save(tree_xml_svg  = tree_xml_svg,
                         filepath_png  = filepath_png)


# -----------------------------------------------------------------------------
def _rewrite_tree_xml_svg(tree_xml_svg,
                          color_fill,
                          width_tgt,
                          height_tgt):
    """
    Modify tree_xml_svg to give it the specified colour and size.

    """

    root_xml      = tree_xml_svg.getroot()
    str_box_svg   = root_xml.get('viewBox')
    tup_box_svg   = tuple(map(float, str_box_svg.split()))
    tup_size_icon = _calculate_icon_size(width_svg  = tup_box_svg[2],
                                         height_svg = tup_box_svg[3],
                                         width_tgt  = width_tgt,
                                         height_tgt = height_tgt)

    (width_icon, height_icon) = tup_size_icon
    root_xml.set('width',  str(width_icon))
    root_xml.set('height', str(height_icon))

    namespace_svg = {'ns0': 'http://www.w3.org/2000/svg'}
    for elem in root_xml.findall('.//ns0:path', namespace_svg):
        elem.set('fill', color_fill)


# -----------------------------------------------------------------------------
def _calculate_icon_size(width_svg,
                         height_svg,
                         width_tgt = None,
                         height_tgt = None):
    """
    Return the icon size.

    Calculate the icon size taking into
    account the target size and aspect
    ratio.

    """

    has_width  = width_tgt  is not None
    has_height = height_tgt is not None
    has_both   = has_width and has_height

    if has_both:
        scale_horiz = width_tgt  / width_svg
        scale_vert  = height_tgt / height_svg
    elif has_width:
        scale_horiz = width_tgt  / width_svg
        scale_vert  = scale_horiz
    elif has_height:
        scale_vert  = height_tgt / height_svg
        scale_horiz = scale_vert
    else:
        raise RuntimeError('Need a width or a height for icon scaling.')

    width_icon  = width_svg  * scale_horiz
    height_icon = height_svg * scale_vert

    return (width_icon, height_icon)


# -----------------------------------------------------------------------------
def _render_svg_and_save(tree_xml_svg, filepath_png):
    """
    Render and save the specified tree xml to the specified binary file.

    """

    with tempfile.NamedTemporaryFile(suffix = ".svg") as tmp_svg:
        with tempfile.NamedTemporaryFile(suffix = ".png") as tmp_png:
            tree_xml_svg.write(tmp_svg.name)
            cairosvg.svg2png(url      = tmp_svg.name,
                             write_to = tmp_png.name)
            img_rect   = PIL.Image.open(tmp_png.name)
            img_square = _add_padding_to_make_square(img_rect)
            img_square.save(filepath_png, 'PNG')


# -----------------------------------------------------------------------------
def _add_padding_to_make_square(rgba_rect):
    """
    Add padding to the icon to make sure it is square.

    TODO: This logic isn't quite right. We need
          to be able to force the icon to be a
          specific size instead.

    """

    rgba_fill       = (255, 255, 255, 0)
    (width, height) = rgba_rect.size
    rgba_mode       = rgba_rect.mode
    if width == height:
        return rgba_rect
    elif width > height:
        icon_size   = (width, width)
        rgba_square = PIL.Image.new(rgba_mode, icon_size, rgba_fill)
        rgba_square.paste(rgba_rect, (0, (width - height) // 2))
        return rgba_square
    else:
        icon_size   = (height, height)
        rgba_square = PIL.Image.new(rgba_mode, icon_size, rgba_fill)
        rgba_square.paste(rgba_rect, ((height - width) // 2, 0))
        return rgba_square
