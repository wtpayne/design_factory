# -*- coding: utf-8 -*-
"""
System level controller component.

"""


import datetime
import time


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the controller.

    """

    # Execution rate control.
    #
    state['period_us']     = None
    state['time_start_us'] = None
    state['time_prev_us']  = None
    if 'frequency_hz' in cfg:
        period_secs            = 1.0 / float(cfg['frequency_hz'])
        state['period_us']     = _int_microseconds(period_secs)
        state['time_start_us'] = _time_us()
        state['time_prev_us']  = state['time_start_us']

    # Degraded mode control.
    #
    state['degraded_enter_maxq'] = cfg.get('dmode_enter_maxq', 20)
    state['degraded_exit_maxq']  = cfg.get('dmode_exit_maxq',  3)
    state['do_degraded']         = False

    # Termination criteria based on elapsed run time.
    #
    state['time_elapsed_max_us'] = None
    if 'time_elapsed_max_secs' in cfg:
        state['time_elapsed_max_us'] = _int_microseconds(
                                                cfg['time_elapsed_max_secs'])

    # Termination criteria based on number of simulation steps.
    #
    state['idx_max'] = None
    if 'idx_max' in cfg:
        state['idx_max'] = cfg['idx_max']
    state['idx'] = 0


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Send a control message with timestamps and mode flags.

    """

    (time_us, load_rel) = _execution_rate_control(inputs, state)
    (do_halt, retval)   = _halt_signal_control(inputs, state, time_us)
    (id_year, id_day, id_hour, id_min, id_sec) = _temporal_aggregation_codes()

    for key in outputs.keys():
        outputs[key]['ena']         = True
        outputs[key]['idx']         = state['idx']
        outputs[key]['ts_rel_us']   = time_us  # Monotonic us. Arbitrary zero.
        outputs[key]['id_year']     = id_year
        outputs[key]['id_day']      = id_day
        outputs[key]['id_hour']     = id_hour
        outputs[key]['id_min']      = id_min
        outputs[key]['id_sec']      = id_sec
        outputs[key]['load_rel']    = load_rel
        outputs[key]['do_degraded'] = state['do_degraded']
        outputs[key]['do_halt']     = do_halt
        outputs[key]['retval']      = retval

    state['idx'] = state['idx'] + 1


# -----------------------------------------------------------------------------
def _execution_rate_control(inputs, state):
    """
    Return the step time and the relative load.

    Wait for the next step time if we are rate
    limited and running early.

    """

    load_rel = 1.0
    is_rate_limited = state['period_us'] is not None
    if is_rate_limited:

        target_us = _time_target_us(state, is_fixed_rate = True)
        delta_us  = target_us - _time_us()  # +ve iff before target time.
        delta_rel = float(delta_us) / float(state['period_us'])
        load_rel  = 1.0 - delta_rel
        is_late   = delta_us < 0

        if is_late:

            # lateness_us = -delta_us
            pass

        else:  # is_early

            delta_secs = _float_seconds(delta_us)
            time.sleep(delta_secs)

    # MUST be measured AFTER the call to time.sleep()
    time_us = _time_us()
    state['time_prev_us'] = time_us

    # Load based degraded-mode initiation
    # and hysteresis based on high/low
    # water marks.
    #
    map_load = dict()
    for feedback in inputs.values():
        if feedback['ena'] and feedback['map_load']:
            map_load.update(feedback['map_load'])
    max_load = 0
    for load_value in map_load.values():
        if load_value > max_load:
            max_load = load_value
    if max_load > state['degraded_enter_maxq']:
        state['do_degraded'] = True
    elif max_load < state['degraded_exit_maxq']:
        state['do_degraded'] = False

    return (time_us, load_rel)


# -----------------------------------------------------------------------------
def _halt_signal_control(inputs, state, time_us):
    """
    Return halt signal and return code.

    Halt if maximum elapsed time is exceeded or
    if maximum number of simulation steps is
    reached.

    """

    # Termination based on elapsed time.
    #
    is_max_time_exceeded = (     (state['time_elapsed_max_us'] is not None)
                             and (state['time_elapsed_max_us'] <= time_us))
    is_max_idx_exceeded  = (     (state['idx_max'] is not None)
                             and (state['idx_max'] <= state['idx']))

    if is_max_time_exceeded or is_max_idx_exceeded:
        do_halt = True
        retval  = 0
    else:
        do_halt = False
        retval  = 0

    # Termination based on reported
    # errors and exceptions.
    #
    for item in inputs.values():
        if item['ena']:
            has_exception = len(item['list_ex']) > 0
            # More sophisticated reset/retry logic can go here.
            if has_exception:
                print('[' + str(state['idx']) + '] - SYSTEM CONTROLLER DETECTS THROWN EXCEPTION.')
                do_halt = True;

    return (do_halt, retval)


# -----------------------------------------------------------------------------
def _temporal_aggregation_codes():
    """
    Return temporal aggregation codes.

    """

    gmt     = time.gmtime()
    id_year = gmt.tm_year
    id_day  = (id_year * 1000) + gmt.tm_yday
    id_hour = (id_day  *  100) + gmt.tm_hour
    id_min  = (id_hour *  100) + gmt.tm_min
    id_sec  = (id_min  *  100) + gmt.tm_sec

    return (id_year, id_day, id_hour, id_min, id_sec)


# -----------------------------------------------------------------------------
def _time_target_us(state, is_fixed_rate):
    """
    Return the target execution time in us.

    """

    if is_fixed_rate:
        return state['time_start_us'] + (state['idx'] * state['period_us'])
    else:
        return state['time_prev_us'] + state['period_us']


# -----------------------------------------------------------------------------
def _time_us():
    """
    Return the current time in milliseconds.

    """

    time_secs = time.monotonic()
    time_us   = _int_microseconds(time_secs)

    return (time_us)


# -----------------------------------------------------------------------------
def _float_seconds(num_us):
    """
    Convert integer microseconds to floating point seconds.

    """

    us_per_second = 1000000
    num_secs      = float(num_us) / float(us_per_second)

    return num_secs


# -----------------------------------------------------------------------------
def _int_microseconds(num_secs):
    """
    Convert floating point seconds to integer microseconds.

    """

    us_per_second = 1000000
    num_us        = int(num_secs * us_per_second)

    return num_us
