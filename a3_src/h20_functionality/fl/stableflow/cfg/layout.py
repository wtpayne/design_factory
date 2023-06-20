# -*- coding: utf-8 -*-
"""
---

title:
    "Configuration file layout module."

description:
    "This component has utilities to layout
    stableflow configuration data."

id:
    "7ea9fc10-4bc2-4704-83fc-9c551685e097"

type:
    dt003_python_module

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


import collections

import fl.util.alg


# -------------------------------------------------------------------------
def horizontal(map_cfg_denorm,
               diagram_border = 10,
               swimlane_title = 30,
               longbus_u      = 60,
               crossbus_v     = 30,
               node_size_x    = 400,
               node_size_y    = 250,
               node_margin_x  = 10,
               node_margin_y  = 10):

    """
    """

    (map_idx_node,
     map_idx_proc,
     count_tranche) = _abstract_grid(map_cfg_denorm = map_cfg_denorm)

    for (id_node, (idx_u, idx_v)) in map_idx_node.items():
        map_cfg_denorm['node'][id_node]['idx_u'] = idx_u
        map_cfg_denorm['node'][id_node]['idx_v'] = idx_v

    for (id_proc, (idx_u, size_u)) in map_idx_proc.items():
        map_cfg_denorm['process'][id_proc]['idx_u']  = idx_u
        map_cfg_denorm['process'][id_proc]['size_u'] = size_u

    map_cfg_denorm['system']['count_tranche'] = count_tranche

    node_stride_x  = (node_size_x + node_margin_x)
    node_stride_y  = (node_size_y + node_margin_y + crossbus_v)

    # Layout nodes in the grid.
    #
    for (id_node, cfg_node) in map_cfg_denorm['node'].items():

        cfg_node['size_x'] = node_size_x
        cfg_node['size_y'] = node_size_y
        cfg_node['pos_x']  = (   diagram_border
                               + swimlane_title
                               + longbus_u
                               + node_margin_x
                               + (node_stride_x * cfg_node['idx_v']))
        cfg_node['pos_y']  = (   diagram_border
                               + (node_stride_y * cfg_node['idx_u']))

        cfg_node['input']  = dict()
        cfg_node['output'] = dict()

    # Layout process swimlanes.
    #
    for (id_proc, cfg_proc) in map_cfg_denorm['process'].items():

        idx_u  = cfg_proc['idx_u']
        size_u = cfg_proc['size_u']
        size_v = map_cfg_denorm['system']['count_tranche']

        cfg_proc['pos_x']  = diagram_border + longbus_u + (idx_u * node_size_x)
        cfg_proc['pos_y']  = diagram_border
        cfg_proc['size_x'] = (   node_margin_x
                               + node_margin_x
                               + (size_u * node_stride_x))
        cfg_proc['size_v'] = (   node_margin_y
                               + node_margin_y
                               + (size_v * node_stride_y))

    # Layout edges.
    #
    for cfg_edge in map_cfg_denorm['edge']:

        id_node_src = cfg_edge['id_node_src']
        id_node_dst = cfg_edge['id_node_dst']
        cfg_src     = map_cfg_denorm['node'][id_node_src]
        cfg_dst     = map_cfg_denorm['node'][id_node_dst]

        cfg_edge['pos_x_start'] = cfg_src['pos_x'] + (cfg_src['size_x'] / 2)
        cfg_edge['pos_y_start'] = cfg_src['pos_y'] + cfg_src['size_y']
        cfg_edge['pos_x_end']   = cfg_dst['pos_x'] + (cfg_dst['size_x'] / 2)
        cfg_edge['pos_y_end']   = cfg_dst['pos_y']

    # Ports.
    #
    for cfg_edge in map_cfg_denorm['edge']:

        id_edge     = cfg_edge['id_edge']
        id_node_src = cfg_edge['id_node_src']
        id_port_src = cfg_edge['relpath_src'][-1]
        id_node_dst = cfg_edge['id_node_dst']
        id_port_dst = cfg_edge['relpath_dst'][-1]
        map_cfg_denorm['node'][id_node_dst]['input'][id_port_dst]  = id_edge
        map_cfg_denorm['node'][id_node_src]['output'][id_port_src] = id_edge

    return map_cfg_denorm


# -------------------------------------------------------------------------
def _abstract_grid(map_cfg_denorm):
    """
    Lay out nodes, swimlanes and buses in an abstract grid.

    Each grid unit corresponds to a single node.

    """
    list_tranche_global  = fl.util.alg.topological_sort(
                                        *_acyclic_data_flow(
                                                map_cfg_denorm['edge']))

    list_id_process      = _sorted_process_list(
                                        map_cfg_denorm,
                                        list_tranche_global)

    map_size_tranche_max = _max_tranche_size(
                                        map_cfg_denorm,
                                        list_tranche_global,
                                        list_id_process)

    map_idx_node         = _2d_node_indices(
                                        map_cfg_denorm,
                                        list_tranche_global,
                                        map_size_tranche_max)

    map_idx_proc         = _2d_process_indices(
                                        list_id_process,
                                        map_size_tranche_max)

    count_tranche        = len(list_tranche_global)

    return (map_idx_node, map_idx_proc, count_tranche)


# -----------------------------------------------------------------------------
def _acyclic_data_flow(iter_cfg_edge, id_process = None):
    """
    Return the data flow graph for the specified process.

    If the process is None, return the data flow graph
    for all edges in the graph.

    The data flow graph is returned as a pair of dicts.
    The first dict maps from upstream nodes to downstream
    nodes, and the second dict maps the reverse, from
    downstream nodes to upstream nodes.

    """
    do_include_all = id_process is None
    map_forward    = collections.defaultdict(set)
    map_backward   = collections.defaultdict(set)

    for cfg_edge in iter_cfg_edge:

        # Decide if we're going to
        # include the current edge.
        #
        is_intra_process = cfg_edge['ipc_type'] == 'intra_process'
        is_local_process = id_process in cfg_edge['list_id_process']
        is_local_edge    = is_intra_process and is_local_process
        do_include_edge  = is_local_edge or do_include_all

        if do_include_edge:

            id_node_src    = cfg_edge['id_node_src']
            id_node_dst    = cfg_edge['id_node_dst']
            is_feedforward = cfg_edge['dirn'] == 'feedforward'

            if is_feedforward:
                map_forward[id_node_src].add(id_node_dst)
                map_backward[id_node_dst].add(id_node_src)
            else:  # is_feedback
                map_backward[id_node_src].add(id_node_dst)
                map_forward[id_node_dst].add(id_node_src)

    return (map_forward, map_backward)


# -----------------------------------------------------------------------------
def _sorted_process_list(map_cfg_denorm, list_tranche_global):
    """
    Return a sorted list of process ids.

    This is intended to be a 'sensible' ordering
    of processes that can be used to arrange
    process-specific swimlanes in a SysML or
    UML activity diagram.

    The returned list of process ids is sorted
    by the index of the first tranche that they
    are involved in processing, then by id_host
    lexicographic order and finally by id_proc
    lexicographic order.

    This means that if the system is overall
    arranged as a pipeline, the swimlanes will
    be sorted in pipeline order, but if it is
    overall arranged as parallel pipelines, then
    the swimlanes will be sorted lexicographically
    by host id and then by process id, giving
    the developer some control over ordering by
    choosing appropirately sortable host and
    process ids.

    """
    # First we get the minimum tranche index
    # for each process (map_idx_tranche_min).
    #
    map_node            = map_cfg_denorm['node']
    map_process         = map_cfg_denorm['process']
    max_idx_tranche     = len(list_tranche_global)
    map_idx_tranche_min = collections.defaultdict(lambda: max_idx_tranche)
    for (idx_tranche, set_id_node) in enumerate(list_tranche_global):
        for id_node in sorted(set_id_node):
            id_process = map_node[id_node]['process']
            map_idx_tranche_min[id_process] = min(
                                idx_tranche, map_idx_tranche_min[id_process])

    # Then we build up a list of tuples containing
    # the keys that we want to sort by, and use
    # it to build a list of process id strings in
    # sorted order. (list_id_process)
    #
    list_tup_key    = list()
    list_id_process = list()
    for (id_process, idx_tranche_min) in map_idx_tranche_min.items():
        id_host = map_process[id_process]['host']
        tup_key = (idx_tranche_min, id_host, id_process)
        list_tup_key.append(tup_key)
    for tup_key in sorted(list_tup_key):
        id_process = tup_key[-1]
        list_id_process.append(id_process)

    return list_id_process


# -----------------------------------------------------------------------------
def _max_tranche_size(map_cfg_denorm, list_tranche_global, list_id_process):
    """
    Return a map from process id to the maximum tranche size for the process.

    This information is needed to size per process
    swimlanes correctly.

    """
    # Work out how many nodes are in each
    # tranche, broken down by process.
    #
    map_node              = map_cfg_denorm['node']
    count_tranche_global  = len(list_tranche_global)
    map_list_size_tranche = dict()
    for id_process in list_id_process:
        map_list_size_tranche[id_process] = [0] * count_tranche_global
    for (idx_tranche, set_id_node) in enumerate(list_tranche_global):
        for id_node in set_id_node:
            id_process = map_node[id_node]['process']
            map_list_size_tranche[id_process][idx_tranche] += 1

    # Work out the maximum tranche size for
    # each process, as this drives how 'wide'
    # the per-process swimlane will need to be.
    #
    map_size_tranche_max = dict()
    for id_process in list_id_process:
        map_size_tranche_max[id_process] = max(map_list_size_tranche[id_process])
    return map_size_tranche_max


# -----------------------------------------------------------------------------
def _2d_node_indices(map_cfg_denorm, list_tranche_global, map_size_tranche_max):
    """
    Return a map of two dimensional indices, one for each node in the graph.

    """
    # Grid positioning transverse to
    # swimlane direction. u is the "x"
    # axis with vertical swimlanes, y
    # axis with horizontal swimlanes.
    #
    idx_u                 = 0
    map_idx_u_min_process = dict()
    for (id_process, size_tranche_max) in map_size_tranche_max.items():
        map_idx_u_min_process[id_process] = idx_u
        idx_u += size_tranche_max

    # x and y grid position for each node.
    #
    map_node     = map_cfg_denorm['node']
    map_idx_node = dict()
    for (idx_tranche, set_id_node) in enumerate(list_tranche_global):
        for (idx_node, id_node) in enumerate(sorted(set_id_node)):
            id_process            = map_node[id_node]['process']
            idx_u_min_process     = map_idx_u_min_process[id_process]
            idx_u_node            = idx_u_min_process + idx_node
            idx_v_node            = idx_tranche
            map_idx_node[id_node] = (idx_u_node, idx_v_node)

    # Sort by tranche and then by
    # position within the tranche.
    #
    map_idx_node = dict(sorted(map_idx_node.items(),
                               key = lambda item: (item[1], item[0])))

    return map_idx_node


# -----------------------------------------------------------------------------
def _2d_process_indices(list_id_process, map_size_tranche_max):
    """
    Return a map of tuples holding the start index and width of each process.

    This fundtion returns a map from id_process
    to a length two tuple describing the size
    of the corresponding process swimlane.

    The first element of the tuple is the start
    index (in abstract grid units).

    The second element of the tuple is the length
    of the swimlane (in abstract grid units).

    """
    map_idx_proc = dict()
    idx_u        = 0
    for id_proc in list_id_process:
        size_u = map_size_tranche_max[id_proc]
        map_idx_proc[id_proc] = (idx_u, size_u)
        idx_u  += size_u

    return map_idx_proc