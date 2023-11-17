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


import contextlib
import functools
import io
import pathlib
import tempfile

import nougat
import nougat.utils.checkpoint
import nougat.utils.device
import numpy
import pypdfium2
import torch
import torchvision.transforms

import fl.util.edict
import fl.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Noop component coroutine.

    """

    ocr = _coro_ocr_nougat()

    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if inputs['fileinfo']['ena']:
            length = len(inputs['fileinfo']['list'])
            for fileinfo in inputs['fileinfo']['list']:
                fileinfo['page'] = ocr.send(fileinfo['bytes'])


# -----------------------------------------------------------------------------
@fl.util.coroutine
def _coro_ocr_nougat():
    """
    Coroutine for performing OCR with the FAIR Nougat model.

    """

    checkpoint = nougat.utils.checkpoint.get_checkpoint()
    model      = nougat.utils.device.move_to_device(
                        model = nougat.NougatModel.from_pretrained(checkpoint),
                        bf16  = True,
                        cuda  = True)
    model.eval()

    list_pageinfo = list()
    while True:
        bytes_pdf = yield list_pageinfo
        list_pageinfo.clear()
        list_pageinfo.extend(_gen_page_prediction(model     = model,
                                                  bytes_pdf = bytes_pdf))


# -----------------------------------------------------------------------------
def _gen_page_prediction(model, bytes_pdf, desired_dpi = 96):
    """
    Yield page predictions from the specified PDF file.

    """

    # Calculate scaling factor.
    #
    points_per_inch = 72  # PDF standard unit of length.
    scaling_factor  = desired_dpi / points_per_inch

    # Yield each page from the PDF in turn.
    #
    pdfdoc = pypdfium2.PdfDocument(bytes_pdf)
    for pil_page in pdfdoc.render(converter   = pypdfium2.PdfBitmap.to_pil,
                                  n_processes = 1,
                                  scale       = scaling_factor):

        # Carry out model-specific data prep
        # on pil_page (a PIL image in RGB order),
        # giving us a 3D pytorch tensor with
        # dimensions color (RBG), height then
        # width.
        #
        tensor3_page = model.encoder.prepare_input(pil_page,
                                                   random_padding = False)

        # The model expects a four dimensional
        # tensor, with the initial dimension
        # containing the batch size. Here we
        # have a batch size of 1, but we still
        # need the page tensor to be in the right
        # shape for the model to work.
        #
        tensor4_page = torch.utils.data.dataloader.default_collate(
                                                            [tensor3_page,])

        # Run inference using the model.
        # This returns a dict with the following
        # fields:
        #
        # {
        #   'predictions': list(),
        #   'sequences':   list(),
        #   'repeats':     list(),
        #   'repetitions': list()
        # }
        #
        map_results = model.inference(image_tensors  = tensor4_page,
                                      early_stopping = False)

        yield map_results
