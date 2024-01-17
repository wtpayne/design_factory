# -*- coding: utf-8 -*-
"""
---

title:
    "Unstructured document text extraction."

description:
    "This module contains functionality for
    extracting text from PDF documents
    using the unstructured library."

id:
    "fc382122-bc46-44f6-9cab-4a430415409d"

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


import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro():
    """
    Yield text for each document provided.

    """

    while True:
        bytes_doc = yield text

