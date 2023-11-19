# -*- coding: utf-8 -*-
"""
---

title:
    "Epistematic OCR data cache stableflow-edict component."

description:
    "Epistematic OCR data cache component."

id:
    "5199ed68-0c42-4ab2-a656-e2ed391fb18f"

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


import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Epistematic OCR data cache component coroutine.

    """

    tup_key_in      = tuple(inputs.keys())
    tup_key_out     = tuple(outputs.keys())
    tup_key_msg_in  = tuple((k for k in tup_key_in  if k not in ('ctrl',)))
    tup_key_msg_out = tuple((k for k in tup_key_out))
    timestamp       = dict()

    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Search for cached OCR results for each
        # file identified by the filesystem
        # scanner.
        #
        list_fileinfo_raw.clear()
        list_fileinfo_ocr.clear()
        if inputs['raw']['ena']:
            for fileinfo_raw in inputs['raw']['list']:
                hexdigest    = fileinfo_raw['metadata']['hexdigest']
                fileinfo_ocr = _lookup(key = hexdigest)
                if fileinfo_ocr is None:  # Not in cache
                    list_fileinfo_raw.append(fileinfo_raw)
                else:
                    list_fileinfo_ocr.append(fileinfo_ocr)

        # Store OCR results in the cache so
        # we don't need to recompute them in
        # future. (Trim off things like page
        # images and OCR model weights).
        #
        if inputs['ocr']['ena']:
            for fileinfo_ocr_fat in inputs['ocr']['list']:
                fileinfo_ocr = _trim(fileinfo_ocr_fat)
                _store(fileinfo_ocr)
                list_fileinfo_ocr.append(fileinfo_ocr)

        # Send for OCR prcessing.
        #
        if list_fileinfo_raw:
            outputs['raw']['ena'] = True
            outputs['raw']['ts'].update(timestamp)
            outputs['raw']['list'][:] = list_fileinfo_raw

        # Send to the engine.
        #
        if list_fileinfo_ocr:
            outputs['ocr']['ena'] = True
            outputs['ocr']['ts'].update(timestamp)
            outputs['ocr']['list'][:] = list_fileinfo_raw



# -----------------------------------------------------------------------------
def _trim():
    """
    Get rid of surplus fields like bytes or page images.

    """
    pass

# -----------------------------------------------------------------------------
def _lookup(key):
    """
    """
    return None