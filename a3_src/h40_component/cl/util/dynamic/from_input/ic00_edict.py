# -*- coding: utf-8 -*-
"""
---

title:
    "Dynamic node from input component."

description:
    "This component allows python source code
    to be received via input ports and loaded
    dynamically, allowing for programmatically
    generated code to be executed in a controlled
    environment."

id:
    "8e29f377-b5a6-4e7b-8729-ffcb7dfe7731"

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


import enum
import types

import pl.stableflow.log


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

    cfg_dyn      = cfg()
    state_dyn    = dict()
    signal       = None
    design_cache = None

    while True:

        inputs = yield (outputs, signal)

        # If we have a new module design, reload 
        # the dynamic module following the new
        # design.
        #
        if 'design' in inputs and inputs['design']['ena']:
            design_new  = inputs['design']
            has_changed = design_new != design_cache
            if has_changed:
                design_cache = design_new
                cfg_dyn      = design_new['cfg']
                args_init    = (runtime, cfg_dyn, inputs, state_dyn, outputs)
                signal       = _load_design(
                                    design_new, state, state_dyn, args_init)

        # Step the currently loaded module design.
        #
        args_step = (inputs, state_dyn, outputs)
        args_init = (runtime, cfg_dyn, inputs, state_dyn, outputs)
        signal = _step(state, state_dyn, inputs, args_step, args_init)


# -----------------------------------------------------------------------------
def _load_design(design_new, state, state_dyn, args_init):
    """
    Reload the module from the provided design.

    """

    signal = None
    name   = design_new['name']
    source = design_new['source']
    module = types.ModuleType('dynamic_module')
    try:
        exec(source, module.__dict__)
    except Exception as err:
        pl.stableflow.log.logger.exception(
                'Live module reload error for "{module}" with error "{err}"',
                module = name,
                err    = err)
        return signal
    else:
        state['module']      = module
        state['name_module'] = name
        state['type_module'] = _get_module_type(module)
        return _reset(state, state_dyn, args_init)



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
        signal = _step_coro(state_dyn, inputs)
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
