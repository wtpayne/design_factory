# -*- coding: utf-8 -*-
"""
---

title:
    "Epestematic engine stableflow-edict component."

description:
    "Epestematic engine component."

id:
    "f1116747-c179-4b70-9963-6f873160268b"

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

import io


import pdf2image.exceptions
import pdf2image

import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Noop component coroutine.

    """

    print('')

    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if inputs['fileinfo']['ena']:
            length = len(inputs['fileinfo']['list'])
            for item in inputs['fileinfo']['list']:
                filepath    = item['filepath']
                buffer      = item['bytes']

                try:
                    list_images = pdf2image.convert_from_path(filepath)
                    # list_images = pdf2image.convert_from_bytes(buffer)
                except pdf2image.exceptions.PDFInfoNotInstalledError as err:
                    print('PDFInfoNotInstalledError')
                    continue
                except pdf2image.exceptions.PDFPageCountError as err:
                    print('PDFPageCountError')
                    continue
                except pdf2image.exceptions.PDFSyntaxError as err:
                    print('PDFSyntaxError')
                    continue
                else:
                    print(len(list_images))
                    for (idx, image) in enumerate(list_images):
                        image_path = f"/media/wtp/Data1/tmp//page_{idx}.jpg"
                        image.save(image_path, 'JPEG')


                # try:
                #     elements = unstructured.partition.pdf.partition_pdf(
                #                             file                  = buffer,
                #                             include_page_breaks   = True,
                #                             strategy              = 'ocr_only',
                #                             infer_table_structure = False,
                #                             ocr_language          = 'eng',
                #                             max_partition         = None,
                #                             include_metadata      = True,
                #                             metadata_filename     = filepath)
                # except pdfminer.psparser.PSEOF:
                #     continue

                # print(filepath)
                # for item in elements:
                #     print('-' * 80)
                #     print('')
                #     print(item)
                #     print('')

