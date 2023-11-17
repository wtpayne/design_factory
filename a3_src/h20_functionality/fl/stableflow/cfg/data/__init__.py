# -*- coding: utf-8 -*-
"""
Package of functions that support the configuration of data types.

"""


import collections
import copy
import enum
import itertools

import fl.stableflow.cfg.data.atomic_types
import fl.stableflow.cfg.data.gap_table
import fl.stableflow.cfg.util
import pl.stableflow.util


# -----------------------------------------------------------------------------
def denormalize(cfg):
    """
    Return a denormalised and flattened instance of the data_dictionary.

    This function returns a copy of the specified
    data dictionary with nodes that have been
    expanded/denormalised and flattened.

    """

    cfg_data   = cfg['data']
    parameters = dict()
    subs       = fl.stableflow.cfg.util.SubstitutionTable(parameters)
    typeinfo   = fl.stableflow.cfg.data.atomic_types.as_dict()
    gap_table  = fl.stableflow.cfg.data.gap_table.GapTable()
    stack      = _init_stack(map = cfg_data)
    expanded   = pl.stableflow.util.PathDict()

    for (idx, node) in enumerate(_iter_depth_first(stack)):

        try:

            expanded[node.path][node.name] = _expand_node(
                                                node, subs, typeinfo, idx)

        except TypeError:

            if node.category != FieldCategory.named_type:
                raise

            gap_table.add(incomplete_type = node.path[0],
                          missing_type    = node.spec,
                          gap_parent_path = node.path,
                          gap_field       = node.name)

    # So far, we have only added fundamental types
    # to our expanded data structure.
    #
    # There are still gaps: One each time a user
    # defined data type was referenced. These are
    # now filled using the information recorded in
    # the gap table.
    #
    gap_table.fill_all(expanded)

    std_form = dict()
    for (type_name, type_definition) in expanded.data.items():
        std_form[type_name] = list(_iter_expanded(type_definition))
    cfg['data'] = std_form

    return cfg


# =============================================================================
Frame = collections.namedtuple('Frame',
               ['line', 'col', 'level', 'path', 'item'])


# =============================================================================
Node = collections.namedtuple('Node',
               ['line', 'col', 'level', 'path', 'name', 'spec', 'category'])


# =============================================================================
class FieldCategory(enum.IntEnum):
    """
    Enumeration for data structure field type categories.

    """

    named_type         = 1
    compound_type      = 2
    parameterised_type = 3


# -----------------------------------------------------------------------------
def _init_stack(map):
    """
    Return a sorted deque of Frame named tuples taken from map.items().

    Sort to ensure top level items are processed in a deterministic order.

    """

    stack      = collections.deque()
    tup_items  = ({key: value} for (key, value) in map.items())
    list_items = sorted(
                    tup_items,
                    key = lambda item: pl.stableflow.util.first(item.keys()))
    for item in reversed(list_items):
        try:
            line = item.lc.line
            col  = item.lc.col
        except AttributeError:
            line = None
            col  = None
        stack.append(Frame(line  = line,
                           col   = col,
                           level = 0,
                           path  = [],
                           item  = item))
    return stack


# -----------------------------------------------------------------------------
def _iter_depth_first(stack):
    """
    Yield nodes from a depth-first traversal of the specified stack.

    """

    while True:  # Loop until stack empty. (Throws IndexError).

        try:
            frame = stack.pop()
        except IndexError:
            return

        field_name = pl.stableflow.util.first(frame.item.keys())
        content    = pl.stableflow.util.first(frame.item.values())

        is_compound_type      = isinstance(content, list)
        is_parameterised_type = isinstance(content, dict)
        is_named_type         = isinstance(content, str)

        # Interior node in the tree: push child nodes onto the stack.
        #
        if is_compound_type:
            child_list = content
            for child in reversed(child_list):
                try:
                    line = child.lc.line
                    col  = child.lc.col
                except AttributeError:
                    line = None
                    col  = None
                stack.append(Frame(line  = line,
                                   col   = col,
                                   level = frame.level + 1,
                                   path  = frame.path + [field_name],
                                   item  = child))

            field_category = FieldCategory.compound_type
            field_spec     = None

        elif is_parameterised_type:
            field_category = FieldCategory.parameterised_type
            field_spec     = content

        elif is_named_type:
            field_category = FieldCategory.named_type
            field_spec     = content

        else:
            raise RuntimeError('Did not recognise type.')

        yield Node(line     = frame.line,
                   col      = frame.col,
                   level    = frame.level,
                   path     = frame.path,
                   name     = field_name,
                   spec     = field_spec,
                   category = field_category)


# -----------------------------------------------------------------------------
def _expand_node(node, subs, typeinfo, idx):
    """
    Return an expanded copy of the specified data type definition node.

    This is not recursive. It expands only the
    node provided, not any children.

    """

    spec = node.spec
    node_info = dict()
    node_info['category']   = node.category.name
    node_info['src_line']   = node.line
    node_info['src_col']    = node.col
    node_info['src_level']  = node.level
    node_info['src_path']   = node.path + [node.name]
    node_info['src_seqnum'] = idx

    # The name of an elsewhere-defined type.
    if node.category == FieldCategory.named_type:

        type_info                 = typeinfo[subs[spec]]
        node_info['typeinfo']     = type_info
        node_info['preset']       = type_info['py']()
        node_info['shape']        = None
        node_info['memory_order'] = 'C'

    # Set of key-value pairs defining a type.
    if node.category == FieldCategory.parameterised_type:
        node_info['typeinfo'] = typeinfo[subs[spec['type']]]

        if 'preset' in spec:
            node_info['preset'] = subs[spec['preset']]
        else:
            node_info['preset'] = node_info['typeinfo']['py']()

        if 'shape' in spec:
            node_info['shape'] = subs[spec['shape']]
        else:
            node_info['shape'] = None

        if 'memory_order' in spec:
            node_info['memory_order'] = subs[spec['memory_order']]
        else:
            node_info['memory_order'] = 'C'

    return dict([('_node_info', node_info)])


# -----------------------------------------------------------------------------
def _iter_expanded(expanded_def):
    """
    Yield nodes from a depth-first traversal of expanded_type_definition.

    """

    root_node   = expanded_def
    root_path   = list()
    stack_frame = (root_node, root_path)
    stack       = collections.deque((stack_frame,))

    # Loop until the stack is empty.
    # (i.e. until it throws an IndexError).
    #
    for idx in itertools.count():

        try:
            (node, path) = stack.pop()
        except IndexError:
            return

        node_info               = node['_node_info']
        node_info['dst_seqnum'] = idx
        node_info['dst_path']   = path
        node_info['dst_level']  = len(path)
        yield node_info

        children = tuple(key for key in node.keys() if key != '_node_info')
        if not children:
            continue

        # Close the scope of a compound type with a 'scope-closer' message.
        scope_closer             = copy.deepcopy(node_info)
        scope_closer['category'] = 'compound_type_scope_closer'
        stack.append(({'_node_info':  scope_closer}, path))

        # Add children to the stack in reverse order.
        for key in reversed(children):
            child_node  = node[key]
            child_path  = path + [key]
            stack_frame = (child_node, child_path)
            stack.append(stack_frame)
