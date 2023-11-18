# -*- coding: utf-8 -*-
"""
---

title:
    "Nougat academic paper OCR module."

description:
    "This module contains functionality for
    performing OCR using the Nougat library
    from Meta (Facebook), which utilises a
    deep learning model tuned for performing
    OCR on academic papers."

id:
    "0edbaa78-fac2-4199-9e8a-61931f4c401d"

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


import nougat
import nougat.utils.checkpoint
import nougat.utils.device
import pypdfium2
import torch
import torchvision.transforms

import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro():
    """
    Yield a pageinfo dict for each PIL image provided.

    """

    checkpoint = nougat.utils.checkpoint.get_checkpoint()
    model      = nougat.utils.device.move_to_device(
                        model = nougat.NougatModel.from_pretrained(checkpoint),
                        bf16  = True,
                        cuda  = True)
    model.eval()

    pageinfo = dict()
    while True:
        pil_image = yield pageinfo
        pageinfo  = _predict_pageinfo(model     = model,
                                      pil_image = pil_image)


# -----------------------------------------------------------------------------
def _predict_pageinfo(model, pil_image):
    """
    Return pageinfo prediction from the specified PIL image.

    """

    # Carry out model-specific data prep
    # on pil_image (a PIL image in RGB order),
    # giving us a 3D pytorch tensor with
    # dimensions color (RBG), height then
    # width.
    #
    tensor3_page = model.encoder.prepare_input(pil_image,
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
    pageinfo = model.inference(image_tensors  = tensor4_page,
                                  early_stopping = False)

    return pageinfo
