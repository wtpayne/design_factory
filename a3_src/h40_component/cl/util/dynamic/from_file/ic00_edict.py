# -*- coding: utf-8 -*-
"""
---

title:
    "Dynamic node from file component."

description:
    "This component allows python source
    files to be monitored on disk and reloaded
    dynamically when they are updated, providing
    a sort of lightweight live coding
    experience.

    Features:

    * File monitoring using modification time (mtime)
    * Error handling with retry mechanisms.
    * State preservation between reloads.
    * Handles both coroutine and step-function APIs.
    * Automatic recovery from syntax errors.
    * Configurable through py_module configuration parameter.

    Usage:
    The component expects a configuration dict with:
    
    - py_module: str  # The Python module path to monitor
    
    Example:
    {
        'py_module': 'my.package.module'
    }

    Note: The monitored module must implement either:
    1. A coroutine interface with 'coro' function, or
    2. A step function interface with 'step' and 'reset' functions."

id:
    "d97cc431-2f50-47a8-9466-c4e2dac4f80c"

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


import copy
import enum
import importlib
import os.path
import time
import types

import pl.stableflow.log


SECS_DELAY_RETRY_RELOAD = 5
SECS_DELAY_RETRY_STEP   = 2


# =============================================================================
class NodeApi(enum.Enum):
    """
    API type for python modules providing a stableflow node implementation.

    Python modules providing implementations for
    stableflow nodes can do so with either using
    a generator function (synchronous coroutine)
    or a pair of functions (step and reset).

    """

    UNKNOWN   = 'unknown'
    COROUTINE = 'coroutine'
    STEP_FCN  = 'step_function'


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine to manage live reload of dynamically changing modules.

    """

    cfg_dyn = copy.deepcopy(cfg)
    cfg_dyn.pop('py_module', None)
    state_dyn = dict()

    name_module          = cfg['py_module']
    module               = importlib.import_module(name_module)
    type_module          = _get_module_type(module)
    state['module']      = module
    state['name_module'] = name_module
    state['type_module'] = type_module

    args_init  = (runtime, cfg_dyn, inputs, state_dyn, outputs)
    args_step  = (inputs, state_dyn, outputs)
    signal     = _reset(state, state_dyn, args_init)
    filepath   = module.__file__
    mtime_last = os.path.getmtime(filepath)

    while True:

        inputs = yield (outputs, signal)

        mtime = os.path.getmtime(filepath)
        if mtime > mtime_last:
            mtime_last = mtime
            _ensure_reload(state, state_dyn, args_init)

        signal = _ensure_step(state, state_dyn, inputs, args_step, args_init)


# -----------------------------------------------------------------------------
def _get_module_type(module: types.ModuleType) -> NodeApi:
    """
    Return the NodeApi for the specified module.

    """

    if 'coro' in module.__dict__:
        return NodeApi.COROUTINE
    elif 'step' in module.__dict__ and 'reset' in module.__dict__:
        return NodeApi.STEP_FCN
    else:
        return NodeApi.UNKNOWN


# -----------------------------------------------------------------------------
def _ensure_reload(state, state_dyn, args_init):
    """
    Ensure the dynamic module is reloaded.

    This function blocks until the dynamic module
    is successfully reloaded.

    """

    err_reload_cache = None
    while True:
        try:
            importlib.reload(state['module'])
        except Exception as err:
            err_reload = str(err)
            if err_reload_cache != err_reload:
                err_reload_cache = err_reload
                pl.stableflow.log.logger.exception(
                                    'Live module reload error for "{module}"',
                                    module = state['name_module'])
            time.sleep(SECS_DELAY_RETRY_RELOAD)
        else:  # Reset on successful reload
            return _reset(state, state_dyn, args_init)

# -----------------------------------------------------------------------------
def _ensure_step(state, state_dyn, inputs, args_step, args_init):
    """
    Ensure the module is stepped.
    
    This function blocks until the dynamic module
    is successfully stepped.

    """

    err_step_cache = None
    while True:

        try:
            signal = _step(state, state_dyn, inputs, args_step)
        except (Exception) as err:
            err_step = str(err)
            if err_step_cache != err_step:
                err_step_cache = err_step
                pl.stableflow.log.logger.exception(
                                'Live module step error for "{module}"',
                                module = state['name_module'])
            time.sleep(SECS_DELAY_RETRY_STEP)
            _ = _ensure_reload(state, state_dyn, args_init)
            continue

        else:
            return signal


# -----------------------------------------------------------------------------
def _reset(state, state_dyn, args_init):
    """
    Reset using either reset function or coroutine.

    """

    signal = None
    if state['type_module'] == NodeApi.STEP_FCN:
        signal =_reset_stepfcn(state, args_init)
    elif state['type_module'] == NodeApi.COROUTINE: 
        signal = _reset_coro(state, state_dyn, args_init)
    else:  # type_module == NodeApi.UNKNOWN
        raise RuntimeError('Logic error: unknown node API type')
    return signal


# -----------------------------------------------------------------------------
def _step(state, state_dyn, inputs, args_step):
    """
    Step using either reset function or coroutine.

    """

    signal = None
    if state['type_module'] == NodeApi.STEP_FCN:
        signal = _step_stepfcn(state, args_step)
    elif state['type_module'] == NodeApi.COROUTINE: 
        signal =_step_coro(state_dyn, inputs)
    else:
        raise RuntimeError('Logic error: unknown node API type')
    return signal


# -----------------------------------------------------------------------------
def _reset_stepfcn(state, args_init):
    """
    Reset a module that uses the step function API standard.

    """

    (_, signal) = state['module'].reset(*args_init)
    return signal


# -----------------------------------------------------------------------------
def _reset_coro(state, state_dyn, args_init):
    """
    Reset a module that uses the coroutine API standard.

    """

    if '__stableflow_coro__' in state_dyn:
        state_dyn['__stableflow_coro__'].close()
    state_dyn['__stableflow_coro__'] = state['module'].coro(*args_init)
    (_, signal) = state_dyn['__stableflow_coro__'].send(None)
    return signal


# -----------------------------------------------------------------------------
def _step_stepfcn(state, args_step):
    """
    Step a module that uses the step function API standard.

    """

    return state['module'].step(*args_step)


# -----------------------------------------------------------------------------
def _step_coro(state_dyn, inputs):
    """
    Step a module that uses the coroutine API standard.

    """

    try:
        (_, signal) = state_dyn['__stableflow_coro__'].send(inputs)
    except StopIteration:
        signal = (pl.stableflow.signal.exit_ok_controlled,)
    return signal
