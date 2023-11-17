# -*- coding: utf-8 -*-
"""
Module of utilities to support the operation of process hosts.

"""


import os
import pl.stableflow.signal

import loguru
import psutil


# -----------------------------------------------------------------------------
def stop(id_system):
    """
    Stop the specified system.

    """

    # Does not seem to be killing processes
    # reliably. Do we need to repeat this
    # several times?
    #
    return _signal_process_by_prefix(
                        prefix      = id_system,
                        iter_signal = (pl.stableflow.signal.exit_ok_controlled,
                                       pl.stableflow.signal.exit_ex_immediate))


# -----------------------------------------------------------------------------
def pause(id_system):
    """
    Pause or unpause the specified system.

    """

    return _signal_process_by_prefix(
                        prefix      = id_system,
                        iter_signal = (pl.stableflow.signal.control_pause,))


 # -----------------------------------------------------------------------------
def step(id_system):
    """
    Single step the specified system.

    """

    return _signal_process_by_prefix(
                        prefix      = id_system,
                        iter_signal = (pl.stableflow.signal.control_step,))


# -----------------------------------------------------------------------------
def print_process_summary(id_system, id_host):
    """
    Print the process summary for the specified system.

    """

    list_proc_name = list()
    for proc in psutil.process_iter(['name', 'pid']):
        proc_name = proc.info['name']
        if proc_name.startswith(id_system):
            list_proc_name.append(proc_name)

    # Don't print anything if there are no
    # matching processes running.
    #
    if not list_proc_name:
        return 0

    # Print the process tree on the current host:
    #
    print('\n')
    print('{id_system}.{id_host}:'.format(
                                id_system = id_system,
                                id_host   = id_host))
    for proc_name in sorted(list_proc_name):
        print('   {proc_name}'.format(
                                proc_name = proc_name))
    print('\n')

    return 0


# -----------------------------------------------------------------------------
def _signal_process_by_prefix(prefix, iter_signal):
    """
    Send the specified signal to the process with the specified name prefix.

    """

    for signal in iter_signal:

        set_pid   = _pid_from_prefix(prefix)
        count_pid = len(set_pid)

        if count_pid == 0:
            break

        loguru.logger.info('Send {signal} to {count} pids.'.format(
                                                        signal = str(signal),
                                                        count  = count_pid))

        _signal_process_tree(
                        iter_pid = set_pid,
                        signal   = signal)

    return 0


# -----------------------------------------------------------------------------
def _pid_from_prefix(prefix):
    """
    Return a list of process ids that correspond to the specified names.

    """

    set_pids  = set()
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'].startswith(prefix):
            set_pids.add(proc.info['pid'])
    return set_pids


# -----------------------------------------------------------------------------
def _signal_process_tree(iter_pid, signal):
    """
    Send the specified signal to all specified process trees.

    iter_pid should be an iterable over a set of
    process ids. The signal will be sent to all
    processes specified by iter_pid as well as
    all of their subprocesses (recursively).

    """

    for pid in iter_pid:

        assert pid != os.getpid(), \
               'A process should not attempt to kill itself'
        try:
            parent = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue

        children = parent.children(recursive = True)
        children.append(parent)
        for proc in children:
            proc.send_signal(signal)

        psutil.wait_procs(children)
