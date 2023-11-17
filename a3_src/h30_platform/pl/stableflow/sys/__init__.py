# -*- coding: utf-8 -*-
"""
Package of functions that support the operation of the system as a whole.

This package contains functions to start, stop,
pause/unpause and single-step an stableflow system.

"""


import copy
import os
import subprocess
import sys  # pylint: disable=W0406
import time
import uuid

import zmq

import fl.stableflow.cfg
import pl.stableflow.host
import pl.stableflow.util.serialization


# -----------------------------------------------------------------------------
def prep_and_start(map_cfg, is_local):
    """
    Prepare configuration and start the system.

    """

    return start(fl.stableflow.cfg.prepare(map_cfg  = map_cfg,
                                           is_local = is_local))


# -----------------------------------------------------------------------------
def start(cfg):
    """
    Start the system.

    """

    cfg['runtime']['id']['id_run'] = uuid.uuid4().hex[0:8]
    cfg['runtime']['id']['ts_run'] = time.strftime('%Y%m%d%H%M%S',
                                                   time.gmtime())

    if cfg['runtime']['opt']['is_local']:
        return _run_locally(cfg)

    if cfg['runtime']['opt']['do_make_ready']:
        pass
        # pl.stableflow.sys.orchestration.ensure_ready_to_run(cfg)

    for id_host in _list_id_host(cfg):
        _command(cfg, id_host, 'start-host')

    return 0


# -----------------------------------------------------------------------------
def stop(cfg):
    """
    Stop the system.

    """

    for id_host in _list_id_host(cfg):
        _command(cfg, id_host, 'stop-host')

    return 0


# -----------------------------------------------------------------------------
def pause(cfg):
    """
    Pause the system.

    """

    if cfg['runtime']['opt']['is_local']:
        raise RuntimeError('Not implemented.')

    for id_host in _list_id_host(cfg):
        _command(cfg, id_host, 'pause-host')

    return 0


# -----------------------------------------------------------------------------
def step(cfg):
    """
    Single step the system.

    """

    if cfg['runtime']['opt']['is_local']:
        raise RuntimeError('Not implemented.')

    for id_host in _list_id_host(cfg):
        _command(cfg, id_host, 'step-host')

    return 0


# -----------------------------------------------------------------------------
def print_process_status(cfg):
    """
    Print the process status for the specified system.

    """

    if cfg['runtime']['opt']['is_local']:
        raise RuntimeError('Not implemented.')

    for id_host in _list_id_host(cfg):
        _command(cfg, id_host, 'ps-host')

    return 0


# -----------------------------------------------------------------------------
def _list_id_host(cfg):
    """
    Return a sorted list of unique id_host.

    """

    iter_cfg_proc = cfg['process'].values()
    set_id_host   = set(cfg_proc['host'] for cfg_proc in iter_cfg_proc)
    list_id_host  = sorted(set_id_host)
    return list_id_host


# -----------------------------------------------------------------------------
def _command(cfg, id_host, command):
    """
    Give the specified host a command.

    """

    cfg_copy        = copy.deepcopy(cfg)
    cfg_copy['runtime']['id']['id_host'] = id_host

    cfg_encoded   = pl.stableflow.util.serialization.serialize(cfg_copy)
    cfg_host      = cfg_copy['host'][id_host]
    launch_cmd    = cfg_host['launch_cmd']
    command_group = 'host'

    if id_host == 'localhost':

        list_args = launch_cmd.split(' ')
        list_args.extend([command_group, command, cfg_encoded])
        subprocess.Popen(list_args)

        # subprocess.Popen(
        #         args   = list_args,
        #         stdin  = subprocess.DEVNULL,
        #         stdout = subprocess.DEVNULL,
        #         stderr = subprocess.DEVNULL)

    else:

        remote_command = '{launch} {grp} {cmd} {cfg}'.format(
                                                launch = launch_cmd,
                                                grp    = command_group,
                                                cmd    = command,
                                                cfg    = cfg_encoded)
        local_command = 'ssh {act}@{host} "{cmd}"'.format(
                                                act  = cfg_host['acct_run'],
                                                host = cfg_host['hostname'],
                                                cmd  = remote_command)

        subprocess.run(local_command, shell = True, check = True)


# -----------------------------------------------------------------------------
def _run_locally(cfg):
    """
    Start all compute nodes in the current process only.

    This function modifies the specified config
    dict to force all data flow graph nodes
    to execute in a single sequential process.

    This is intended to assist with debugging
    and diagnosing errors.

    """

    import pl.stableflow.proc  # pylint: disable=C0415,W0621

    id_host_local    = 'localhost'
    id_process_local = 'mainprocess'

    for cfg_proc in cfg['process'].values():
        cfg_proc['host'] = id_host_local

    cfg['process'][id_process_local] = {'host': id_host_local}

    for cfg_node in cfg['node'].values():
        cfg_node['process'] = id_process_local

    cfg = fl.stableflow.cfg.denormalize(cfg)

    for cfg_edge in cfg['edge']:
        cfg_edge['ipc_type']        = 'intra_process'
        cfg_edge['list_id_process'] = [id_process_local]

    cfg['runtime']['id']['id_host']    = id_host_local
    cfg['runtime']['id']['id_process'] = id_process_local

    map_queues = pl.stableflow.host.connect_queues(cfg, id_host_local)
    return pl.stableflow.proc.start(
                            cfg, id_process_local, id_host_local, map_queues)
