# -*- coding: utf-8 -*-
"""
---

title:
    "PDF rasterization stableflow-edict component."

description:
    "PDF rasterization component."

id:
    "80d484fe-27ed-4ddc-a030-f287cddb0bbc"

type:
    dt004_python_stableflow_edict_component

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


import pypdfium2

import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro(desired_dpi = 96):
    """
    Yield a list of rasterized pages for each supplied PDF data buffer.

    """

    list_pil_page = list()

    while True:

        bytes_pdf = yield list_pil_page

        list_pil_page.clear()
        list_pil_page.extend(_rasterize_all_pages(bytes_pdf   = bytes_pdf,
                                                  desired_dpi = desired_dpi))


# -----------------------------------------------------------------------------
def _rasterize_all_pages(bytes_pdf, desired_dpi = 96):
    """
    Return a list of rasterized pages from the specified PDF data buffer.

    To avoid the device-dependent effects of
    specifying objects in device space, the
    ISO 23000-2:2020 PDF 2.0 standard defines
    a device independent coordinate system that
    always bears the same relationship to the
    current page, regardless of the output
    device on which printing or displaying
    occurs.

    This device-independent coordinate system
    is called user space. The length of a unit
    along both the x and y axes of user space
    is set by the UserUnit entry in the page
    dictionary.

    If that entry is not present or supported,
    the default value of 1 ⁄ 72 inch is used.

    This coordinate system is called default
    user space.

    For the purposes of this function, we
    assume that default user space is being
    used.

    In future, we may wish to interrogate
    the PDF to find out if a custom user
    space has been specified.

    """

    # The scale argument in the pypdfium2 render
    # method indicates the desired number of
    # pixels per PDF canvas unit. Assuming that
    # the PDF is using default user space, we
    # need to divide the desired DPI by the
    # standard PDF canvas unit size.
    #
    user_space_units_per_inch = 72  # According to ISO 23000-2:2020 8.3.2.3
    pixels_per_canvas_unit    = desired_dpi / user_space_units_per_inch

    # Each page gets rendered to a PIL image,
    # which is stored as a 3-channel color image
    # with channel, height, width raster order,
    # with color channels sorted in RGB order.
    #
    pdfdoc        = pypdfium2.PdfDocument(bytes_pdf)
    list_pil_page = list(pil_page for pil_page in pdfdoc.render(
                                    converter   = pypdfium2.PdfBitmap.to_pil,
                                    n_processes = 1,
                                    scale       = pixels_per_canvas_unit))

    return list_pil_page
