# -*- coding: utf-8 -*-
"""
---

title:
    "Textract document text extraction."

description:
    "This module contains functionality for
    extracting text from PDF and DOC documents
    using the textract library by Dean Malmgren."

id:
    "6e89cc10-dc6a-420e-a456-6f8227f8e983"

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


import tempfile

import textract

import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro():
    """
    Yield text for each document provided.

    """

    while True:
        bytes_doc = yield text

        with tempfile.NamedTemporaryFile() as file_tmp:
            file_tmp.write(bytes_doc)
            file_tmp.seek(0)
            filepath_tmp = file_tmp.name
            text = textract.process(filepath_tmp, extension = '.pdf')