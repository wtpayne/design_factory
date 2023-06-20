# -*- coding: utf-8 -*-
"""
---

title:
    "Enabled dictionary components utility functions module."

description:
    "This module contains various utility
    functions to help with programming stableflow
    components that conform to the edict (enabled
    dictionary) convention."

id:
    "7e43d715-d0e2-41d8-879b-e5aeaa9b7dc8"

type:
    dt003_python_module

validation_level:
    v00_minimums

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


# -----------------------------------------------------------------------------
def validate(inputs         = None,
             outputs        = None,
             cannot_contain = None,
             must_contain   = None,
             must_equal     = None):
    """
    Validate inputs or outputs.

    """
    if (inputs is not None) and (outputs is None):
        str_io = 'inputs'
        set_id = set(inputs.keys())
    elif (inputs is None) and (outputs is not None):
        str_io = 'outputs'
        set_id = set(outputs.keys())
    else:
        raise RuntimeError('Must provide either inputs only or outputs only.')


    if cannot_contain is not None:
        if set(cannot_contain).issubset(set_id):
            raise RuntimeError(
                    'Invalid {io}. Contains invalid id.'.format(io = str_io))

    if must_contain is not None:
        if not set(must_contain).issubset(set_id):
            raise RuntimeError(
                    'Invalid {io}. Required id not found.'.format(io = str_io))

    if must_equal is not None:
        set_required = set(must_equal)
        if set_id != set_required:

            str_missing = ''
            set_missing = set_required - set_id
            if set_missing:
                str_missing = 'Missing: {tup}. '.format(
                                                    tup = tuple(set_missing))

            str_extra = ''
            set_extra = set_id - set_required
            if set_extra:
                str_extra = 'Extra: {tup}. '.format(tup = tuple(set_extra))

            raise RuntimeError(
                    'Invalid {str_io}. {missing}{extra}'.format(
                                                        str_io  = str_io,
                                                        missing = str_missing,
                                                        extra   = str_extra))


# -----------------------------------------------------------------------------
def init(outputs, collection = 'list'):
    """
    Initialize all outputs.

    In a C/C++ implementation, this is where memory
    for the output would be allocated.

    """

    for id_out in outputs.keys():

        packet        = outputs[id_out]
        packet['ena'] = False
        packet['ts']  = dict()

        if collection == 'list':
            packet['list'] = list()

        elif collection == 'map':
            packet['map']  = dict()

        else:
            raise RuntimeError('Unrecognized collection type.')




# -----------------------------------------------------------------------------
def reset(outputs):
    """
    Reset all outputs.

    """

    for id_out in outputs.keys():

        packet        = outputs[id_out]
        packet['ena'] = False
        packet['ts'].clear()

        if 'list' in packet:
            packet['list'].clear()

        if 'map' in packet:
            packet['map'].clear()
