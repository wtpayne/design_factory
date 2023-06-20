# -*- coding: utf-8 -*-
"""
---

title:
    "Data persistence component."

description:
    "Stableflow component to persistent data
    over restarts by saving it on a local disk,
    reloading it when the system restarts."

id:
    "282e3ab1-df99-48ec-9753-8cff6794e964"

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

import appdirs
import dill

import fl.util
import pl.stableflow.signal


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Persistent data store component coroutine.

    """

    list_str_log = list()
    signal       = None

    # We expect persisted datasets to have
    # a corresponding input and output with
    # the same name. We reserve the names
    # 'ctrl' and 'log' for control signals
    # and logging respectively. We consider
    # violations of these precodntions to be
    # critical (nonrecoverable) errors, so
    # we signal the system to shut down by
    # raising an exception.
    #
    set_id_out  = set(outputs.keys())
    set_id_in   = set(inputs.keys())
    set_id_save = set_id_in & set_id_out
    if 'ctrl' in set_id_save:
        raise RuntimeError(
            'The persistence component must only have one "ctrl" input.')
    if 'log' in set_id_save:
        raise RuntimeError(
            'The persistence component must only have one "log" output.')

    # Load configuration. If the dirpath is not
    # provided, then we use the appdirs library
    # to generate a system specific default path.
    # On Unix systems, this will be:
    #
    #   ~/.local/share/{id_system}/
    #
    dirpath = cfg.get('dirpath', None)
    if dirpath is None:
        dirpath = appdirs.user_data_dir(appname = runtime['id']['id_system'])

    # Create the directory where the data is
    # going to be saved. If we cannot create
    # the directory then we consider that to
    # be a critical (nonrecoverable) error, so
    # we signal the system to shut down by
    # raising an exception.
    #
    try:
        os.makedirs(dirpath, exist_ok = True)
    except OSerror as err:
        raise RuntimeError(
            'Critical error creating directory "{dirpath}": {err}'.format(
                                                            dirpath = dirpath,
                                                            err     = err))

    # Work out the filepath for each
    # dataset that we want to persist.
    #
    map_filepath = dict()
    for id_save in set_id_save:
        map_filepath[id_save] = os.path.join(
                                        dirpath,
                                        '{name}.bin'.format(name = id_save))

    # Load saved state if the file exists.
    #
    map_state = dict()
    for (id_save, filepath) in map_filepath.items():
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'rb') as file:
                    map_state[id_save] = dill.load(file)
            except (OSError, IOError) as err:
                list_str_log.append(
                    'Error reading file "{file}": {err}'.format(
                                                            file = filepath,
                                                            err  = err))
            except (dill.UnpicklingError, EOFError) as err:
                list_str_log.append(
                    'Error unpickling data from file "{file}": {err}'.format(
                                                            file = filepath,
                                                            err  = err))

    # Initialize outputs.
    #
    for id_out in set_id_out:
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in set_id_out:
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Allow ourselves to be disabled
        # with a control signal.
        #
        if not inputs['ctrl']['ena']:
            continue

        # Send saved state (but only once)
        #
        for id_save in set_id_save:

            if id_save not in map_state:
                continue

            outputs[id_save]['ena']     = True
            outputs[id_save]['ts']      = inputs['ctrl']['ts']
            outputs[id_save]['list'][:] = map_state[id_save]
            del map_state[id_save]

        # Save any new incoming state.
        #
        for id_save in set_id_save:

            if not inputs[id_save]['ena']:
                continue

            filepath = map_filepath[id_save]
            try:
                with open(filepath, 'wb') as file:
                    dill.dump(inputs[id_save]['list'], file)
            except (OSError, IOError) as err:
                list_str_log.append(
                    'Error writing to file "{file}": {err}'.format(
                                                            file = filepath,
                                                            err  = err))
            except TypeError as err:
                list_str_log.append(
                    'Error pickling data to file "{file}": {err}'.format(
                                                            file = filepath,
                                                            err  = err))

        # Output log messages.
        #
        if list_str_log:
            if 'log' in outputs:
                outputs['log']['ena']     = True
                outputs['log']['ts']      = inputs['ctrl']['ts']
                outputs['log']['list'][:] = list_str_log
            else:
                for str_log in list_str_log:
                    print(str_log)
            list_str_log.clear()
