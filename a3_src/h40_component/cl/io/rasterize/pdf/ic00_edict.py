# -*- coding: utf-8 -*-
"""
---

title:
    "PDF rasterization stableflow-edict component."

description:
    "PDF rasterization component. Augments each
    provided fileinfo dict with a list_pil_page
    field which contains a list of PIL images,
    one per page."

id:
    "31b1a3f8-0f07-4347-ad6f-540bd5022f72"

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


import fl.io.rasterize.pdf
import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    PDF rasterization stableflow-edict component coroutine.

    """

    rasterizer      = fl.io.rasterize.pdf.coro()
    tup_key_in      = tuple(inputs.keys())
    tup_key_out     = tuple(outputs.keys())
    tup_key_msg_in  = tuple((k for k in tup_key_in  if k not in ('ctrl',)))
    tup_key_msg_out = tuple((k for k in tup_key_out))
    list_rasterized = list()
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

        # If any other inputs have any documents,
        # then rasterize each one of them in turn.
        #
        list_rasterized.clear()
        for str_key in tup_key_msg_in:

            if not inputs[str_key]['ena']:
                continue

            for fileinfo in inputs[str_key]['list']:

                if 'list_pageinfo' not in fileinfo:
                    fileinfo['list_pageinfo'] = list()
                list_pageinfo = fileinfo['list_pageinfo']

                list_pil_page = rasterizer.send(fileinfo['bytes'])

                for (idx, pil_page) in enumerate(list_pil_page):

                    if idx >= len(list_pageinfo):
                        list_pageinfo.append(dict())

                    list_pageinfo[idx]['pil_image'] = pil_page
                    fileinfo['list_pageinfo'] = list_pageinfo

                list_rasterized.append(fileinfo)

        # If we have rasterized any documents,
        # then send them to all outputs.
        #
        if list_rasterized:
            for str_key in tup_key_msg_out:
                outputs[str_key]['ena'] = True
                outputs[str_key]['ts'].update(timestamp)
                outputs[str_key]['list'][:] = list_rasterized
