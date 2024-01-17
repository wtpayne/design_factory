# -*- coding: utf-8 -*-
"""
---

title:
    "pypdf PDF text extraction."

description:
    "This module contains functionality for
    extracting text from PDF and DOC documents
    using the textract library by Dean Malmgren."

id:
    "fe87daba-3a54-4500-b905-9bc20d86b7ad"

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

import pypdf

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

            pdf      = pypdf.PdfReader(file_tmp.name)
            metadata = pdf.metadata

            print(metadata.keys)

            # output                         = dict()
            # output['metadata']             = dict()
            # output['metadata']['author']   = metadata.author
            # output['metadata']['creator']  = metadata.creator
            # output['metadata']['producer'] = metadata.producer
            # output['metadata']['subject']  = metadata.subject
            # output['metadata']['title']    = metadata.title
            # output['list_pageinfo']        = list()

            # for page in pdf.pages:
            #     text = page.extract_text()


            # for page in :
            #     text =
            #     print(text)

