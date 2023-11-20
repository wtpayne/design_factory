# -*- coding: utf-8 -*-
"""
---

title:
    "OCR data cache stableflow-edict component."

description:
    "This module documents the design of a
    stableflow-edict component which is intended
    to function as a data cache for document OCR
    results, allowing OCR results to be cached
    persistently, reducing the need to repeat
    time consuming and computationally expensive
    optical character recognition.

    This component recieves file information
    from some a filesystem scanner-reader, and
    then checks to see if OCR results for that
    file are stored in the cache. If results
    are present in the cache, they are used
    as-is. Otherwise, the file information is
    handed off to an OCR pipeline for processing.

    Any file information that is returned from
    the OCR pipeline is stored in the cache
    for future use.

    OCR results, whether retrieved from the
    cache or computer on-demand, are then
    handed off to the next stage in the process."

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


import sqlitedict

import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Epistematic OCR data cache component coroutine.

    """

    tup_key_in = (
        'ctrl',          # Control signal from system controller.
        'fileinfo_raw',  # Raw file information from reader.
        'fileinfo_ocr')  # OCR processed file information from OCR pipeline.
    tup_key_out = (
        'fileinfo_raw',  # Raw file information to OCR pipeline.
        'fileinfo_ocr')  # OCR processed file information to engine.

    assert tup_key_in  == tuple(inputs.keys())
    assert tup_key_out == tuple(outputs.keys())

    filepath_cache = cfg.get('filepath_cache_db')
    cache          = sqlitedict.SqliteDict(filepath_cache, autocommit = False)

    timestamp         = dict()
    list_fileinfo_raw = list()
    list_fileinfo_ocr = list()

    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Get timestamp from control input.
        #
        if not inputs['ctrl']['ena']:
            continue
        timestamp.update(inputs['ctrl']['ts'])

        # Build a list of OCR results that have
        # been pulled from the cache as well as
        # a list of files that were not found in
        # the cache and need to be OCRd.
        #
        list_fileinfo_ocr.clear()  # Retrieved from the cache.
        list_fileinfo_raw.clear()  # Not found in cache.
        if inputs['fileinfo_raw']['ena']:
            for fileinfo_raw in inputs['fileinfo_raw']['list']:

                print('')
                print(fileinfo_raw['filepath'])


                key = fileinfo_raw['metadata']['hexdigest']
                try:
                    list_fileinfo_ocr.append(cache[key])
                    print('CACHE HIT')
                except KeyError:
                    list_fileinfo_raw.append(fileinfo_raw)
                    print('CACHE MISS')

        # Cache OCR results, trimming things like
        # page images and OCR model weights.
        #
        if inputs['fileinfo_ocr']['ena']:
            for fileinfo_ocr_fat in inputs['fileinfo_ocr']['list']:
                fileinfo_ocr = _trim(fileinfo_ocr_fat)
                key          = fileinfo_ocr['metadata']['hexdigest']
                cache[key]   = fileinfo_ocr
                list_fileinfo_ocr.append(fileinfo_ocr)
            cache.commit()

        # Send for OCR prcessing.
        #
        if list_fileinfo_raw:
            outputs['fileinfo_raw']['ena'] = True
            outputs['fileinfo_raw']['ts'].update(timestamp)
            outputs['fileinfo_raw']['list'][:] = list_fileinfo_raw

        # Send to the engine.
        #
        if list_fileinfo_ocr:
            outputs['fileinfo_ocr']['ena'] = True
            outputs['fileinfo_ocr']['ts'].update(timestamp)
            outputs['fileinfo_ocr']['list'][:] = list_fileinfo_ocr


# -----------------------------------------------------------------------------
def _trim(fileinfo):
    """
    Get rid of large intermediate data such as page images and raw content.

    """
    try:
        del fileinfo['list_pageinfo']
    except KeyError:
        pass

    try:
        del fileinfo['bytes']
    except KeyError:
        pass

    return fileinfo
