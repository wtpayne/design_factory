# -*- coding: utf-8 -*-
"""
Package of stableflow control signals.

These signals are understood by the runtime.

---
type:
    python_extension

name_extension:
    pl.stableflow.signal
...

"""


import cython
import signal


# Continue, everything is OK.
#
continue_ok: cython.int = 100

# Immediate exceptional shutdown (e.g. fatal nonrecoverable error).
#
exit_ex_immediate: cython.int = int(signal.SIGKILL)

# Controlled exceptional shutdown.
#
exit_ex_controlled: cython.int = 101

# Controlled nominal shutdown.
#
exit_ok_controlled: cython.int = int(signal.SIGTERM)

# Reset and retry
#
control_reset: cython.int = 102

# Pause
#
control_pause: cython.int = int(signal.SIGUSR1)

# Single-step when paused.
#
control_step: cython.int = int(signal.SIGUSR2)

exit = (
    exit_ex_immediate,
    exit_ex_controlled,
    exit_ok_controlled)

reset = (
    control_reset,)

immediate = (
    exit_ex_immediate,)

controlled = (
    exit_ex_controlled,
    exit_ok_controlled,
    control_reset,
    control_pause,
    control_step)
