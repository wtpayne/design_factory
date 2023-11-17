# -*- coding: utf-8 -*-
"""
Package of functions that support the operation of individual compute nodes.

"""


import functools
import importlib
import sys

import pl.stableflow.log
import pl.stableflow.signal
import pl.stableflow.util
import pl.stableflow.proc


# =============================================================================
class Node():  # pylint: disable=R0902
    """
    Class representing a node in the data flow graph.

    """

    # -------------------------------------------------------------------------
    def __init__(self, id_node, cfg_node, runtime):
        """
        Return an instance of a Node object.

        """

        # Create our own copy of the runtime.
        self.runtime = {'id': {}, 'proc': {}}
        self.runtime['id'].update(runtime['id'])
        self.runtime['proc'].update(runtime['proc'])
        self.runtime['id']['id_node'] = id_node

        self.id_node       = id_node
        self.config        = dict()
        self.inputs        = pl.stableflow.util.RestrictedWriteDict()
        self.state         = dict()
        self.outputs       = pl.stableflow.util.RestrictedWriteDict()
        self.input_queues  = dict()
        self.output_queues = dict()

        try:
            self.config = cfg_node['config']
        except KeyError:
            pass

        (self.fcn_reset,
         self.fcn_step,
         self.fcn_finalize) = _load_functionality(cfg_node['functionality'])

    # -------------------------------------------------------------------------
    def reset(self):
        """
        Reset or zeroize node data structures.

        """

        iter_signal = _call_reset(
                id_node   = self.id_node,
                fcn_reset = self.fcn_reset,
                runtime   = self.runtime,
                config    = self.config,
                inputs    = self.inputs,
                state     = self.state,
                outputs   = self.outputs)

        _prime_feedback(
                id_node       = self.id_node,
                inputs        = self.inputs,
                input_queues  = self.input_queues,
                outputs       = self.outputs,
                output_queues = self.output_queues)

        return iter_signal

    # -------------------------------------------------------------------------
    def step(self):
        """
        Step node logic.

        """

        _dequeue_inputs(
                    input_queues = self.input_queues,
                    input_memory = self.inputs)

        iter_signal = _call_step(
                    id_node  = self.id_node,
                    fcn_step = self.fcn_step,
                    inputs   = self.inputs,
                    state    = self.state,
                    outputs  = self.outputs)

        _enqueue_outputs(
                    output_queues = self.output_queues,
                    output_memory = self.outputs)

        return iter_signal


    # -------------------------------------------------------------------------
    def finalize(self):
        """
        Finalize node logic.

        """

        iter_signal = _call_finalize(
                id_node      = self.id_node,
                fcn_finalize = self.fcn_finalize,
                runtime      = self.runtime,
                config       = self.config,
                inputs       = self.inputs,
                state        = self.state,
                outputs      = self.outputs)

        return iter_signal


# -------------------------------------------------------------------------
def _load_functionality(cfg_func):
    """
    Return a tuple containing the reset and step functions.

    """

    fcn_reset    = None
    fcn_step     = None
    fcn_finalize = None

    if 'py_module' in cfg_func:
        (fcn_reset,
         fcn_step,
         fcn_finalize) = _load_from_module(
                                spec_module = cfg_func['py_module'])

    elif 'py_dill' in cfg_func:
        (fcn_reset,
         fcn_step,
         fcn_finalize) = _load_serialized(
                            spec     = cfg_func['py_dill'],
                            unpacker = pl.stableflow.util.function_from_dill)

    elif 'py_src' in cfg_func:
        (fcn_reset,
         fcn_step,
         fcn_finalize) = _load_serialized(
                            spec     = cfg_func['py_src'],
                            unpacker = pl.stableflow.util.function_from_source)

    return (fcn_reset, fcn_step, fcn_finalize)


# -----------------------------------------------------------------------------
def _load_from_module(spec_module):
    """
    Try to import the specified module.

    """

    module = pl.stableflow.proc.ensure_imported(spec_module)  # throws

    if _is_step(map_func = module.__dict__):
        fcn_reset    = module.reset
        fcn_step     = module.step
    else:  # is_coro
        fcn_reset    = functools.partial(_coro_reset, module.coro)
        fcn_step     = _coro_step


    # Finalize is optional.
    #
    if _has_finalize(map_func = module.__dict__):
        fcn_finalize = module.finalize
    else:
        fcn_finalize = None

    return (fcn_reset, fcn_step, fcn_finalize)


# -----------------------------------------------------------------------------
def _load_serialized(spec, unpacker):
    """
    Load functionality from serialized objects.

    """

    if _is_step(map_func = spec):
        fcn_reset    = unpacker(spec['reset'])
        fcn_step     = unpacker(spec['step'])
    else:  # is_coro
        fcn_reset    = functools.partial(_coro_reset, unpacker(spec['coro']))
        fcn_step     = _coro_step


    # Finalize is optional.
    #
    if _has_finalize(map_func = spec):
        fcn_finalize = unpacker(spec['finalize'])
    else:
        fcn_finalize = None

    return (fcn_reset, fcn_step, fcn_finalize)


# -----------------------------------------------------------------------------
def _is_step(map_func):
    """
    Return true iff map_func has a reset and step function defined.

    """

    is_coro = 'coro'  in map_func
    is_step = 'reset' in map_func and 'step' in map_func
    assert is_coro or is_step
    return is_step


# -----------------------------------------------------------------------------
def _has_finalize(map_func):
    """
    Return true iff map_func has a finalize function defined.

    """

    has_finalize = 'finalize' in map_func
    return has_finalize


# -----------------------------------------------------------------------------
def _coro_reset(coro, runtime, config, inputs, state, outputs):
    """
    Create the coroutine and run it to the first yield point.

    """

    state['__stableflow_coro__'] = coro(runtime, config, inputs, state, outputs)
    (outputs, signal) = state['__stableflow_coro__'].send(None)
    return signal


# -----------------------------------------------------------------------------
def _coro_step(inputs, state, outputs):
    """
    Single step the coroutine, running it to the next yield point.

    """

    try:
        (outputs, signal) = state['__stableflow_coro__'].send(inputs)
        return signal
    except StopIteration:
        return (pl.stableflow.signal.exit_ok_controlled,)


# -----------------------------------------------------------------------------
def _call_reset(id_node, fcn_reset, runtime, config, inputs, state, outputs):
    """
    Call the reset function and return any signal.

    This function acts as an adapter for the
    various different ways that a reset function
    can return/throw a control signal.

    """

    if fcn_reset is None:
        return (pl.stableflow.signal.continue_ok,)

    try:

        iter_signal = fcn_reset(runtime, config, inputs, state, outputs)
        if not iter_signal:
            iter_signal = (pl.stableflow.signal.continue_ok,)
        return iter_signal

    except Exception as error:
        pl.stableflow.log.logger.exception(
                'Reset function failed for id_node = "{id}"', id = id_node)
        return (pl.stableflow.signal.exit_ex_immediate,)


# -------------------------------------------------------------------------
def _prime_feedback(id_node, inputs, input_queues, outputs, output_queues):
    """
    Prime all owned feedback input and output queues with one message.

    """

    for (path, queue) in output_queues.items():
        if queue.owner == id_node and queue.direction == 'feedback':
            item = _get_ref(outputs, path)
            queue.non_blocking_write(item)

    for (path, queue) in input_queues.items():
        if queue.owner == id_node and queue.direction == 'feedback':
            item = _get_ref(inputs, path)
            queue.non_blocking_write(item)


# -----------------------------------------------------------------------------
def _call_step(id_node, fcn_step, inputs, state, outputs):
    """
    Call the step function and return any signal.

    This function acts as an adapter for the
    various different ways that a step function
    can return/throw a control signal.

    """

    if fcn_step is None:
        return (pl.stableflow.signal.continue_ok,)

    try:

        iter_signal = fcn_step(inputs, state, outputs)
        if not iter_signal:
            iter_signal = (pl.stableflow.signal.continue_ok,)
        return iter_signal

    except Exception as error:
        pl.stableflow.log.logger.exception(
                    'Step function failed for id_node = "{id}"', id = id_node)
        return (pl.stableflow.signal.exit_ex_immediate,)


# -----------------------------------------------------------------------------
def _call_finalize(
            id_node, fcn_finalize, runtime, config, inputs, state, outputs):
    """
    Call the finalize function and return any signal.

    This function acts as an adapter for the
    various different ways that a finalize function
    can return/throw a control signal.

    """

    if fcn_finalize is None:
        return (pl.stableflow.signal.continue_ok,)

    try:

        iter_signal = fcn_finalize(runtime, config, inputs, state, outputs)
        if not iter_signal:
            iter_signal = (pl.stableflow.signal.continue_ok,)
        return iter_signal

    except Exception as error:
        pl.stableflow.log.logger.exception(
                'Finalize function failed for id_node = "{id}"', id = id_node)
        return (pl.stableflow.signal.exit_ex_immediate,)


# -----------------------------------------------------------------------------
def _dequeue_inputs(input_queues, input_memory):
    """
    Dequeue items from the input queues and store in input memory.

    Note: Shared memory edges are not touched by
    this process, as they are transmitted
    implicitly, by making parts of an input_memory
    and output_memory structure alias each
    other.

    """

    for (path, queue) in input_queues.items():
        item = queue.blocking_read()
        _put_ref(input_memory, path, item)


# -----------------------------------------------------------------------------
def _enqueue_outputs(output_queues, output_memory):
    """
    Enqueue items from output memory into output queues.

    Note: Shared memory edges are not touched by
    this process, as they are transmitted
    implicitly, by making parts of an input_memory
    and output_memory structure alias each
    other.

    """

    for (path, queue) in output_queues.items():
        item = _get_ref(output_memory, path)
        queue.non_blocking_write(item)


# -----------------------------------------------------------------------------
def _put_ref(ref, path, item):
    """
    Make the specified node and path point to the specified memory.

    """

    for name in path[:-1]:
        ref = ref[name]

    if isinstance(ref, pl.stableflow.util.RestrictedWriteDict):
        ref._stableflow_framework_internal_setitem(path[-1], item)
    else:
        ref[path[-1]] = item


# -----------------------------------------------------------------------------
def _get_ref(ref, path):
    """
    Get a reference to the value that path refers to.

    """

    for name in path:
        ref = ref[name]
    return ref
