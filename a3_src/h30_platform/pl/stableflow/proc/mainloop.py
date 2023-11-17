# -*- coding: utf-8 -*-
"""
Python extension module for process mainloop support.

"""


import signal

import pl.stableflow.signal


#cdef int STEP     = 0
#cdef int RESET    = 1
#cdef int FINALIZE = 2

STEP     = 0
RESET    = 1
FINALIZE = 2


# -----------------------------------------------------------------------------
def run_with_retry(tup_node, list_signal):
    """
    Repeatedly step the specified nodes in order, resetting if needed.

    On each 'schedule round', we may be stepping
    any number of dataflow graph nodes, and each
    node step function may return any number of
    signals, so one of the main purposes of this
    function is to look at the returned signals
    and act on them in priority order. I.e.
    exit takes priority over reset, and reset
    takes priority over continue.

    When the system halts, the highest priority
    signal value from the last 'schedule round'
    is returned.

    """

    # cdef object iter_sig_reset
    # cdef object iter_sig_step
    # cdef object iter_sig_pause
    while True:

        # Reset all nodes to make sure they are
        # in a runnable state before we enter the
        # main loop. Act on any signals returned
        # from the application layer.
        #
        iter_sig_reset = _call(function = RESET,
                               tup_node = tup_node)

        if _has_exit_signal(iter_sig = iter_sig_reset):
            _call(function = FINALIZE,
                  tup_node = tup_node)
            return _get_exit_signal(iter_sig_reset)

        # If a RESET function returns a
        # pl.stableflow.signal.control_reset
        # signal, then we do not honor it, as
        # we could easily end up in an endless
        # loop of reset after reset. Instead we
        # return:
        #
        #   pl.stableflow.signal.exit_ex_immediate.
        #
        if _has_reset_signal(iter_sig_reset):
            _call(function = FINALIZE,
                  tup_node = tup_node)
            return pl.stableflow.signal.exit_ex_immediate

        while True:

            # Check to see if we've received
            # a pl.stableflow.signal.control_pause
            # signal from the interrupt handler
            # (it places it into list_signal)
            # and if so enter the pause and
            # single-step state loop until
            # un-paused. Act on any signals
            # received while single-stepping
            # the system.
            #
            if _has_pause_signal(list_signal):

                list_signal.clear()

                iter_sig_pause = _pause_loop(tup_node    = tup_node,
                                             list_signal = list_signal)

                if _has_exit_signal(iter_sig_pause):
                    _call(function = FINALIZE,
                          tup_node = tup_node)
                    return _get_exit_signal(iter_sig_pause)

                if _has_reset_signal(iter_sig_pause):
                    break  # Reset and retry

            list_signal.clear()

            # Now that we know that all nodes have
            # been configured and reset to an
            # operational state and that we are
            # not in a pause-state, we can finally
            # loop through all nodes, single
            # stepping each one and collecting
            # all the returned signals. We then
            # act on these to return or retry as
            # needed.
            #
            iter_sig_step = _call(function = STEP,
                                  tup_node = tup_node)

            if _has_exit_signal(iter_sig_step):
                _call(function = FINALIZE,
                      tup_node = tup_node)
                return _get_exit_signal(iter_sig_step)

            if _has_reset_signal(iter_sig_step):
                break  # Reset and retry


# -----------------------------------------------------------------------------
# cdef object _pause_loop(tup_node, list_signal):
def _pause_loop(tup_node, list_signal):
    """
    Handle pause and single step states.

    """

    # We will be paused when we enter this function
    # so loop until we are unpaused, handling any
    # single-stepping until then.
    #
    while True:

        sig = signal.sigwait([pl.stableflow.signal.control_pause,
                              pl.stableflow.signal.control_step])

        is_unpaused = (sig == pl.stableflow.signal.control_pause)
        if is_unpaused:
            return (pl.stableflow.signal.continue_ok,)

        is_stepped = (sig == pl.stableflow.signal.control_step)
        if is_stepped:

            iter_sig_step = _call(function = STEP,
                                  tup_node = tup_node)

            if _has_exit_signal(iter_sig_step):
                return iter_sig_step

            # If we are unlucky enough to get a
            # reset signal while single-stepping,
            # then we need to remain in the pause
            # state somehow, so we cheekily add
            # a pause signal back on the list_signal
            # and return the reset signal.
            #
            # This complexity is an indication that
            # the mainloop really should be
            # implemented explictly as a state
            # machine.
            #
            if _has_reset_signal(iter_sig_step):
                list_signal.append(pl.stableflow.signal.control_pause)
                return iter_sig_step

            continue


# -----------------------------------------------------------------------------
def _has_pause_signal(list_signal):
    """
    Return true iff iter_sig contains a pause signal.

    """

    is_paused = pl.stableflow.signal.control_pause in list_signal
    return is_paused


# -----------------------------------------------------------------------------
def _has_reset_signal(iter_sig):
    """
    Return true if iter_sig contains a reset signal.

    """

    is_reset = pl.stableflow.signal.control_reset in iter_sig
    return is_reset


# -----------------------------------------------------------------------------
def _has_exit_signal(iter_sig):
    """
    Return true if iter_sig contains an exit signal.

    """

    for sig_exit in pl.stableflow.signal.exit:
        if sig_exit in iter_sig:
            return True
    return False


# -----------------------------------------------------------------------------
def _get_exit_signal(iter_sig):
    """
    Return the first exit signal from iter_sig.

    """

    for sig_exit in pl.stableflow.signal.exit:
        if sig_exit in iter_sig:
            return sig_exit
    return pl.stableflow.signal.exit_ex_controlled


# -----------------------------------------------------------------------------
# cdef object _call(object function, object tup_node):
def _call(function, tup_node):
    """
    Call the specified function once on each node.

    """

    # cdef object accumulator = list()
    # cdef object iter_signal
    accumulator = list()

    for node in tup_node:

        if function == STEP:
            iter_signal = node.step()
        elif function == RESET:
            iter_signal = node.reset()
        elif function == FINALIZE:
            iter_signal = node.finalize()
        else:
            iter_signal = (pl.stableflow.signal.exit_ex_immediate,)

        for signal in pl.stableflow.signal.immediate:
            if signal in iter_signal:
                return (signal,)

        for signal in iter_signal:
            if signal in pl.stableflow.signal.controlled:
                accumulator.append(signal)

    if accumulator:
        return tuple(accumulator)
    else:
        return tuple()
