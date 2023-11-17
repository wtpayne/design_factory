# -*- coding: utf-8 -*-
"""
Module of functions that support the configuration of data flow graph edges.

---
type:
    python_extension

name_extension:
    fl.stableflow.cfg.edge
...

"""


import collections


# -----------------------------------------------------------------------------
def denormalize(cfg):
    """
    Add redundant information to each edge to make it more convenient to use.

    """

    _denormalize_nodes(cfg)
    set_id_host_remote_owner = _denormalize_edges(cfg)
    _denormalize_hosts(cfg, set_id_host_remote_owner)
    return cfg


# -----------------------------------------------------------------------------
def _denormalize_nodes(cfg):
    """
    Add derived information to each node.

    """

    for (id_node, cfg_node) in cfg['node'].items():
        id_process = cfg_node['process']
        id_host    = cfg['process'][id_process]['host']
        cfg['node'][id_node]['host'] = id_host

        # Add a placeholder class (tag) list
        # to the node config.
        #
        if 'class' not in cfg_node:
            cfg['node'][id_node]['class'] = list()


# -----------------------------------------------------------------------------
def _denormalize_edges(cfg):
    """
    Add derived information to each edge.

    """

    set_id_host_remote_owner = set()
    map_idx_edge = collections.defaultdict(int)

    for cfg_edge in cfg['edge']:

        (path_src, id_process_src, id_host_src) = _add_src_info(cfg, cfg_edge)
        (path_dst, id_process_dst, id_host_dst) = _add_dst_info(cfg, cfg_edge)

        if 'dirn' not in cfg_edge:
            cfg_edge['dirn'] = 'feedforward'

        cfg_edge['id_edge']         = id_edge(cfg_edge)
        cfg_edge['list_id_process'] = [id_process_src, id_process_dst]
        cfg_edge['list_id_host']    = [id_host_src, id_host_dst]

        id_host_owner = _add_host_owner(cfg, cfg_edge)
        is_inter_host = _add_ipc_type(cfg_edge,
                                      id_process_src, id_process_dst,
                                      id_host_src,    id_host_dst)
        if is_inter_host:
            set_id_host_remote_owner.add(id_host_owner)
            idx_edge = map_idx_edge[id_host_owner]
            map_idx_edge[id_host_owner] += 1
        else:
            idx_edge = None

        cfg_edge['idx_edge'] = idx_edge

    return set_id_host_remote_owner


# -----------------------------------------------------------------------------
def id_edge(cfg_edge):
    """
    Return the edge id for the specified edge configuration.

    """

    return ':'.join((cfg_edge['src'], cfg_edge['dst']))


# -----------------------------------------------------------------------------
def _add_src_info(cfg, cfg_edge):
    """
    Add information about the source of each edge.

    """

    path_src       = cfg_edge['src']
    path_parts_src = path_src.split('.')
    id_node_src    = path_parts_src[0]
    id_process_src = cfg['node'][id_node_src]['process']
    id_host_src    = cfg['node'][id_node_src]['host']

    cfg_edge['relpath_src'] = path_parts_src[1:]
    cfg_edge['id_node_src'] = id_node_src
    cfg_edge['id_host_src'] = id_host_src

    return (path_src, id_process_src, id_host_src)


# -----------------------------------------------------------------------------
def _add_dst_info(cfg, cfg_edge):
    """
    Add information about the destination of each edge.

    """

    path_dst       = cfg_edge['dst']
    path_parts_dst = path_dst.split('.')
    id_node_dst    = path_parts_dst[0]
    id_process_dst = cfg['node'][id_node_dst]['process']
    id_host_dst    = cfg['node'][id_node_dst]['host']

    cfg_edge['relpath_dst'] = path_parts_dst[1:]
    cfg_edge['id_node_dst'] = id_node_dst
    cfg_edge['id_host_dst'] = id_host_dst

    return (path_dst, id_process_dst, id_host_dst)


# -----------------------------------------------------------------------------
def _add_host_owner(cfg, cfg_edge):
    """
    Add information about the process host on which the edge owner resides.

    """

    id_node_owner = cfg_edge['owner']
    id_host_owner = cfg['node'][id_node_owner]['host']
    cfg_edge['id_host_owner'] = id_host_owner

    return id_host_owner


# -----------------------------------------------------------------------------
def _add_ipc_type(cfg_edge,
                  id_process_src, id_process_dst,
                  id_host_src,    id_host_dst):
    """
    Add IPC type information to the edge configuration.

    """

    is_same_process  = (id_process_src == id_process_dst)
    is_same_host     = (id_host_src == id_host_dst)
    is_intra_process = is_same_host and is_same_process
    is_inter_process = is_same_host and (not is_same_process)
    is_inter_host    = (not is_same_host) and (not is_same_process)
    ipc_type         = _ipc_type(is_intra_process,
                                 is_inter_process,
                                 is_inter_host)
    cfg_edge['ipc_type'] = ipc_type

    return is_inter_host


# -----------------------------------------------------------------------------
def _denormalize_hosts(cfg, set_id_host_remote_owner):
    """
    Add derived information to each host.

    """

    for (id_host, cfg_host) in cfg['host'].items():
        cfg_host['is_inter_host_edge_owner'] = (
                                        id_host in set_id_host_remote_owner)


# -----------------------------------------------------------------------------
def _ipc_type(is_intra_process, is_inter_process, is_inter_host):
    """
    Return ipc_type as a string.

    """

    if is_intra_process:
        ipc_type = 'intra_process'
    elif is_inter_process:
        ipc_type = 'inter_process'
    elif is_inter_host:
        ipc_type = 'inter_host'
    else:
        raise RuntimeError(
                    'Cannot use one process_id on two different hosts')
    return ipc_type
