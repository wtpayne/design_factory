# -*- coding: utf-8 -*-
"""
---

title:
    "File watching and loading component."

description:
    "File watching and loading functionality."

id:
    "f7e8577f-6e66-4068-95ce-6502b23f0581"

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
import fl.load.file


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Prototype functionality coroutine.

    """

    fl.util.edict.validate(inputs = inputs,  must_contain = ('ctrl',))

    gen_list_fileinfo = fl.load.file.gen_list_fileinfo(
                iter_dirpath_root      = cfg['dirpath_root'],
                iter_pathincl          = cfg.get('pathincl',            None),
                iter_pathexcl          = cfg.get('pathexcl',            None),
                iter_direxcl           = cfg.get('direxcl',             None),
                iter_read_as_txt       = cfg.get('read_as_txt',         None),
                iter_read_as_bin       = cfg.get('read_as_bin',         None),
                size_batch             = cfg.get('batch_size',          50),
                do_output_all          = cfg.get('output_all',          False),
                do_repeat_all          = cfg.get('repeat_all',          False),
                do_output_modified     = cfg.get('output_modified',     False),
                do_terminate_when_done = cfg.get('terminate_when_done', False))

    signal = fl.util.edict.init(outputs)
    while True:

        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if not inputs['ctrl']['ena']:
            continue

        timestamp     = inputs['ctrl']['ts']
        list_fileinfo = next(gen_list_fileinfo)

        if list_fileinfo:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(timestamp)
                outputs[id_out]['list'][:] = list_fileinfo
