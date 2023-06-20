# -*- coding: utf-8 -*-
"""
Package of functions that support the operation of process hosts.

"""


import multiprocessing
import os
import platform
import sys

import fl.stableflow.cfg
import pl.stableflow.host.util
import pl.stableflow.log
import pl.stableflow.proc


FIFO_HOST_CONTROL = "stableflow_host_control"


pl.stableflow.log.setup()


# -----------------------------------------------------------------------------
@pl.stableflow.log.logger.catch
def start(cfg):
    """
    Start all compute nodes for the local host.

    """
    _setup_host(cfg)
    pl.stableflow.log.logger.info('Host start')
    return _start_all_hosted_processes(cfg)


# -----------------------------------------------------------------------------
@pl.stableflow.log.logger.catch
def stop(cfg):
    """
    Stop all compute nodes for the local host.

    """
    _setup_host(cfg)
    pl.stableflow.log.logger.info('Host stop')
    return pl.stableflow.host.util.stop(id_system = cfg['system']['id_system'])


# -----------------------------------------------------------------------------
@pl.stableflow.log.logger.catch
def pause(cfg):
    """
    Pause/unpause all compute nodes for the local host.

    """
    _setup_host(cfg)
    pl.stableflow.log.logger.info('Host pause')
    return pl.stableflow.host.util.pause(id_system = cfg['system']['id_system'])


# -----------------------------------------------------------------------------
@pl.stableflow.log.logger.catch
def step(cfg):
    """
    Single step all compute nodes for the local host.

    """
    _setup_host(cfg)
    pl.stableflow.log.logger.info('Host step')
    return pl.stableflow.host.util.step(id_system = cfg['system']['id_system'])


# -----------------------------------------------------------------------------
@pl.stableflow.log.logger.catch
def get_process_summary(cfg):
    """
    Return the process summary for the local host.

    """
    id_host = _setup_host(cfg)
    pl.stableflow.log.logger.info('Host ps')
    return pl.stableflow.host.util.print_process_summary(
                                        id_system = cfg['system']['id_system'],
                                        id_host   = id_host)


# -----------------------------------------------------------------------------
def _setup_host(cfg):
    """
    Perform common setup actions and return id_host.

    """
    cfg     = fl.stableflow.cfg.denormalize(cfg)
    id_host = cfg['runtime']['id']['id_host']
    return id_host


# -----------------------------------------------------------------------------
def _start_all_hosted_processes(cfg):
    """
    Start all processes on the local host.

    """
    # TODO: POSIX event handling.

    # Forking is unsafe on OSX and isn't supported
    # on windows.
    if platform.system() == 'Linux':
        multiprocessing.set_start_method('fork')
    else:
        multiprocessing.set_start_method('spawn')

    id_host_local = cfg['runtime']['id']['id_host']
    map_queues    = connect_queues(cfg, id_host_local)
    map_processes = dict()

    # Redirect stdin and stdout
    #
    # sys.stdin.close()
    # sys.stdout.close()
    # sys.stderr.close()
    # file_devnull = open(os.devnull, 'w')
    # sys.stdin    = file_devnull
    # sys.stdout   = file_devnull
    # sys.stderr   = file_devnull

    for (id_process, cfg_process) in sorted(cfg['process'].items()):
        if cfg_process['host'] == id_host_local:
            map_processes[id_process] = _start_one_child_process(
                                                cfg        = cfg,
                                                id_process = id_process,
                                                map_queues = map_queues)
    sys.exit(0)


# -----------------------------------------------------------------------------
def connect_queues(cfg, id_host_local):
    """
    Return a map of (id_node, path) to queues.

    Start servers and connect clients as required.

    """
    map_cfg_edge    = _index_edge_config(cfg)
    map_id_by_class = _group_edges_by_class(cfg, id_host_local)
    map_queues      = _construct_queues(cfg,
                                        map_cfg_edge,
                                        map_id_by_class,
                                        id_host_local)
    return map_queues


# -----------------------------------------------------------------------------
def _index_edge_config(cfg):
    """
    Retun a map from edge id to the config for that edge.

    """
    map_cfg_edge = dict()
    for cfg_edge in cfg['edge']:
        map_cfg_edge[cfg_edge['id_edge']] = cfg_edge
    return map_cfg_edge


# -----------------------------------------------------------------------------
def _group_edges_by_class(cfg, id_host_local):
    """
    Return a map of edge ids grouped into ipc, server, or client edge classes.

    """
    map_id_by_class = {
        'intra_process':     set(),
        'inter_process':     set(),
        'inter_host_server': set(),
        'inter_host_client': set()
    }

    for cfg_edge in cfg['edge']:
        id_edge = cfg_edge['id_edge']

        # Ignore edges that don't impact the current host.
        #
        is_on_host_local = id_host_local in cfg_edge['list_id_host']
        if not is_on_host_local:
            continue

        # Inter-host (i.e. remote) queues have a server end and a client end.
        #
        if cfg_edge['ipc_type'] == 'inter_host':
            if id_host_local == cfg_edge['id_host_owner']:
                queue_type = 'inter_host_server'
            else:
                queue_type = 'inter_host_client'

        # Inter-process and intra-process queues are the same class both ends.
        #
        else:
            queue_type = cfg_edge['ipc_type']  # inter_process or intra_process

        map_id_by_class[queue_type].add(id_edge)

    return map_id_by_class


# -----------------------------------------------------------------------------
def _construct_queues(cfg, map_cfg_edge, map_id_by_class, id_host_local):
    """
    Return a map from edge id to queue instance.

    """
    # Ensure queue implementations are loaded.
    #
    map_queue_impl = dict()
    for (id_edge_class, spec_module) in cfg['queue'].items():
        module = pl.stableflow.proc.ensure_imported(spec_module)
        if 'Queue' not in module.__dict__:
            raise pl.stableflow.exception.NonRecoverableError(
                                cause = 'No Queue class in specified module.')
        map_queue_impl[id_edge_class] = module.Queue

    # Select the correct queue implementation for each edge.
    #
    map_queues = dict()
    for (id_edge_class, queue_impl) in map_queue_impl.items():
        for id_edge in map_id_by_class[id_edge_class]:
            map_queues[id_edge] = queue_impl(
                                    cfg, map_cfg_edge[id_edge], id_host_local)

    return map_queues


# -----------------------------------------------------------------------------
def _start_one_child_process(cfg, id_process, map_queues):
    """
    Start a single specified child process.

    """
    # name_proc is also used to
    # set process title inside
    # pl.stableflow.proc.start
    #
    name_proc   = pl.stableflow.proc.fully_qualified_name(cfg, id_process)
    id_host     = cfg['runtime']['id']['id_host']
    proc        = multiprocessing.Process(
                        target = pl.stableflow.proc.start,
                        args   = (cfg, id_process, id_host, map_queues),
                        name   = name_proc)
    proc.daemon = False
    try:
        proc.start()
    except BrokenPipeError:
        pl.stableflow.log.logger.warning(
                                    'Broken pipe when running: ' + id_process)
    return proc
