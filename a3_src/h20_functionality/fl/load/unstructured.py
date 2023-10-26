# -*- coding: utf-8 -*-
"""
---

title:
    "Unstructured data ETL module."

description:
    "Unstructured data ETL functionality."

id:
    "38e2c07a-809b-4816-bb26-9bb36e257d10"

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


import io
import multiprocessing
import queue

import magic
import perscache
import unstructured.partition.auto
import unstructured.partition.pdf

import fl.util


cache = perscache.Cache()


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro():  # pylint: disable=W0613
    """
    Prototype functionality coroutine.

    """

    cfg_worker        = {}
    str_name_process  = 'loader-worker'
    fcn_worker        = _loader_worker
    queue_to_worker   = multiprocessing.Queue()  # system --> worker
    queue_from_worker = multiprocessing.Queue()  # worker --> system
    tup_args          = (cfg_worker, queue_to_worker, queue_from_worker)
    proc_worker       = multiprocessing.Process(
                                        target = fcn_worker,
                                        args   = tup_args,
                                        name   = str_name_process,
                                        daemon = True)  # So we get terminated
    proc_worker.start()

    list_to_worker   = list()
    list_from_worker = list()

    while True:

        list_to_worker.clear()
        (list_to_worker) = yield (list_from_worker)
        list_from_worker.clear()

        for item in list_to_worker:
            try:
                queue_to_worker.put(item, block = False)
            except queue.Full as err:
                list_from_worker.append(
                        dict(type    = 'log_event',
                             content = 'Item dropped: queue_to_bot is full.'))
                break

        while True:
            try:
                list_from_worker.append(queue_from_worker.get(block = False))
            except queue.Empty:
                break


# -----------------------------------------------------------------------------
def _loader_worker(cfg_worker, queue_to_worker, queue_from_worker):
    """
    Load and partition data from enqueued bytes.

    """

    obj_magic = magic.Magic(mime = True)

    while True:

        try:
            fileinfo = queue_to_worker.get(block = False)
        except queue.Empty:
            continue

        filepath   = fileinfo['filepath']
        bytes_file = fileinfo['bytes']
        io_file    = io.BytesIO(bytes_file)
        type_file  = obj_magic.from_buffer(bytes_file[:2048])

        if type_file == 'application/pdf':
            list_chunk = _partition_pdf(file                  = io_file,
                                        strategy              = 'auto',
                                        infer_table_structure = True)
        else:
            list_chunk = _partition_auto(file     = io_file,
                                         strategy = 'auto')

        for chunk in list_chunk:
            chunk.metadata.filename = filepath
            try:
                queue_from_worker.put(chunk, block = False)
            except queue.Full as err:
                continue


# -----------------------------------------------------------------------------
@cache
def _partition_pdf(file, strategy, infer_table_structure):
    """
    Partition the specified PDF file.

    """

    return unstructured.partition.pdf.partition_pdf(
                                file                  = file,
                                strategy              = strategy,
                                infer_table_structure = infer_table_structure)


# -----------------------------------------------------------------------------
@cache
def _partition_auto(file, strategy):
    """
    Partition the specified file (auto-detect type).

    """

    return unstructured.partition.auto.partition(file     = file,
                                                 strategy = strategy)
