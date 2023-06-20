# -*- coding: utf-8 -*-
"""
Package of functions that mutate configuration data.

---
type:
    python_extension

name_extension:
    fl.stableflow.cfg.builder
...

"""


# -----------------------------------------------------------------------------
def get_skeleton_config():
    """
    Return a skeleton configuration structure.

    """
    return {
        'system':       {},
        'host':         {},
        'process':      {},
        'node':         {},
        'edge':         [],
        'req_host_cfg': {},
        'data':         {}
    }


# -----------------------------------------------------------------------------
def set_system_id(cfg, id_system):
    """
    Mutate the config structure with a modified system_id.

    """
    cfg['system']['id_system'] = id_system


# -----------------------------------------------------------------------------
def add_host(cfg, id_host, **kwargs):
    """
    Mutate the config structure to add a new process host.

    """
    cfg['host'][id_host] = dict(kwargs.items())


# -----------------------------------------------------------------------------
def remove_host(cfg, id_host):
    """
    Mutate the config structure to remove the specified process host.

    All processes in the process host are also
    removed, as are all all nodes contained in
    any of these processes, and all edges starting
    or ending at any of these nodes.

    """
    list_id_process_to_delete = list()
    for (id_process, cfg_process) in cfg['process'].items():
        if cfg_process['host'] == id_host:
            list_id_process_to_delete.append(id_process)

    for id_process in list_id_process_to_delete:
        remove_process(cfg, id_process)

    del cfg['host'][id_host]


# -----------------------------------------------------------------------------
def add_process(cfg, id_process, id_host = None, **kwargs):
    """
    Mutate the config structure to add a new process.

    """
    tup_hosts = tuple(cfg['host'].keys())
    if id_host is None:
        id_host = tup_hosts[0]

    assert id_host in tup_hosts

    cfg['process'][id_process] = dict(kwargs.items())
    cfg['process'][id_process]['host'] = id_host


# -----------------------------------------------------------------------------
def remove_process(cfg, id_process):
    """
    Mutate the config structure to remove the specified process.

    All nodes in the process are also removed, as
    are all edges starting or ending at any of
    these nodes.

    """
    list_id_node_to_delete = list()
    for (id_node, cfg_node) in cfg['node'].items():
        if cfg_node['process'] == id_process:
            list_id_node_to_delete.append(id_node)

    for id_node in list_id_node_to_delete:
        remove_node(cfg, id_node)

    del cfg['process'][id_process]


# -----------------------------------------------------------------------------
def add_node(cfg,  # pylint: disable=R0913
             id_node,
             id_process    = None,
             req_host_cfg  = None,
             functionality = None,
             py_module     = None,
             state_type    = None,
             config        = None):
    """
    Mutate the config structure to add a new node.

    """
    cfg_node = dict()

    if id_process is not None:
        cfg_node['process'] = id_process
    else:
        cfg_node['process'] = tuple(cfg['process'].keys())[0]

    if req_host_cfg is not None:
        cfg_node['req_host_cfg'] = req_host_cfg

    if functionality is not None:
        cfg_node['functionality'] = functionality
    else:
        cfg_node['functionality'] = dict()

    if py_module is not None:
        cfg_node['functionality']['py_module'] = py_module

    if state_type is not None:
        cfg_node['state_type'] = state_type

    if config is not None:
        cfg_node['config'] = config

    cfg['node'][id_node] = cfg_node


# -----------------------------------------------------------------------------
def remove_node(cfg, id_node):
    """
    Mutate the config structure to remove the specified node.

    All edges starting or ending at the node are also removed.

    """
    path_prefix             = '{id_node}.'.format(id_node = id_node)
    list_cfg_edge_to_remove = list()

    for cfg_edge in cfg['edge']:
        if cfg_edge['src'].startswith(path_prefix):
            list_cfg_edge_to_remove.append(cfg_edge)
        if cfg_edge['dst'].startswith(path_prefix):
            list_cfg_edge_to_remove.append(cfg_edge)

    for cfg_edge in list_cfg_edge_to_remove:
        cfg['edge'].remove(cfg_edge)

    del cfg['node'][id_node]


# -----------------------------------------------------------------------------
def add_edge(cfg,  # pylint: disable=R0913
             id_src,
             src_ref,
             id_dst,
             dst_ref,
             data):
    """
    Mutate the config structure to add a new edge.

    """
    cfg['edge'].append({
        'owner': id_src,
        'data':  data,
        'src':   id_src + '.' + src_ref,
        'dst':   id_dst + '.' + dst_ref
    })


# -----------------------------------------------------------------------------
def remove_edge(cfg, src, dst):
    """
    Mutate the config structure to remove the specified edge.

    """
    list_cfg_edge_to_remove = list()

    for cfg_edge in cfg['edge']:
        if (cfg_edge['src'] == src) or (cfg_edge['dst'] == dst):
            list_cfg_edge_to_remove.append(cfg_edge)

    for cfg_edge in list_cfg_edge_to_remove:
        cfg['edge'].remove(cfg_edge)


# -----------------------------------------------------------------------------
def add_data(cfg, id_data, spec_data):
    """
    Mutate the config structure to add a new data type.

    """
    cfg['data'][id_data] = spec_data


# -----------------------------------------------------------------------------
def remove_data(cfg, id_data):
    """
    Mutate the config structure to remove the specified data type.

    """
    del cfg['data'][id_data]


# -----------------------------------------------------------------------------
def add_pipeline(cfg,  # pylint: disable=R0913
                 iter_id_node,
                 spec_id_process,
                 spec_req_host_cfg,
                 spec_py_module,
                 spec_state_type,
                 spec_config,
                 iter_edge_info):
    """
    Mutate the config structure to add a pipeline of new nodes.

    """
    list_id_node   = list(iter_id_node)
    num_nodes      = len(list_id_node)
    list_edge_info = list(iter_edge_info)
    num_edges      = len(list_edge_info)

    assert num_edges == ( num_nodes - 1 )

    list_id_process   = _make_list(spec_id_process,   str,  num_nodes)
    list_req_host_cfg = _make_list(spec_req_host_cfg, str,  num_nodes)
    list_py_module    = _make_list(spec_py_module,    str,  num_nodes)
    list_state_type   = _make_list(spec_state_type,   str,  num_nodes)
    list_config       = _make_list(spec_config,       dict, num_nodes)

    for (id_node,
         id_process,
         req_host_cfg,
         py_module,
         state_type,
         config) in zip(list_id_node,
                        list_id_process,
                        list_req_host_cfg,
                        list_py_module,
                        list_state_type,
                        list_config):

        add_node(cfg,
                 id_node      = id_node,
                 id_process   = id_process,
                 req_host_cfg = req_host_cfg,
                 py_module    = py_module,
                 state_type   = state_type,
                 config       = config)

    for (id_node_src,
         id_node_dst,
         edge_info) in zip(list_id_node[:-1],
                           list_id_node[1:],
                           list_edge_info):

        for each_edge in edge_info:
            (port_src, port_dst, edge_data_type) = each_edge
            add_edge(cfg,
                     id_src  = id_node_src,
                     src_ref = 'outputs.{port}'.format(port = port_src),
                     id_dst  = id_node_dst,
                     dst_ref = 'inputs.{port}'.format(port = port_dst),
                     data    = edge_data_type)


# -----------------------------------------------------------------------------
def _make_list(data, type, count):
    """
    If data is type, return count copies in a list, else return as-is.

    """
    if isinstance(data, type):
        return [data] * count
    return data
