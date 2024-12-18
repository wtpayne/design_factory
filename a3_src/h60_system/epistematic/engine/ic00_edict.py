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


import os
import os.path

import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Epestematic engine component coroutine.

    """

    tup_key_in      = tuple(inputs.keys())
    tup_key_out     = tuple(outputs.keys())
    tup_key_msg_in  = tuple((k for k in tup_key_in  if k not in ('ctrl',)))
    tup_key_msg_out = tuple((k for k in tup_key_out))
    list_processed  = list()
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

        for str_key in tup_key_msg_in:

            if not inputs[str_key]['ena']:
                continue

            for fileinfo in inputs[str_key]['list']:

                dirpath_tmp  = '/home/wtp/tmp/'
                filename_tmp = '{digest}.txt'.format(
                                digest = fileinfo['metadata']['hexdigest'])
                filepath_tmp = os.path.join(dirpath_tmp, filename_tmp)
                if not os.path.isfile(filepath_tmp):
                    with open(filepath_tmp, 'wt') as file_tmp:
                        file_tmp.write(fileinfo['mmd'])
