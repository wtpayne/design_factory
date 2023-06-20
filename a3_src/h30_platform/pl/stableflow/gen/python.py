# -*- coding: utf-8 -*-
"""
Module of functions supporting the use of data dictionaries from python.

This module defines various functions that create allocators, initializers
and validators for the Python language from data types defined in a data
dictionary.

The data dictionary is stored in cfg['data'] or cfg_data.

"""

import copy

import numpy

import pl.stableflow.util


# -----------------------------------------------------------------------------
def map_allocator(cfg_data):
    """
    Return a map of allocator functions for the specified data dictionary.

    Allocator functions allocate the memory
    that is required to store each data type
    in the cfg_data data dictionary.

    """
    map_alloc = _map_function(cfg_data, _allocator)
    map_alloc[None] = dict
    return map_alloc


# -----------------------------------------------------------------------------
def map_initializer(cfg_data):
    """
    Return a map of initializer functions for the specified data dictionary.

    Initializer functions set or reset each data
    type in the cfg_data data dictionary to a
    clean initial state.

    """
    return _map_function(cfg_data, _initializer)


# -----------------------------------------------------------------------------
def map_validator(cfg_data):
    """
    Return a map of validator functions for the specified data dictionary.

    Validator functions check each data type in
    the cfg_data data dictionary for validity.

    In production this is used to detect radiation
    damage. During early development, this is used
    to detect some simple bugs.

    """
    return _map_function(cfg_data, _validator)


# -----------------------------------------------------------------------------
def _map_function(cfg_data, _get_function):
    """
    Return dict mapping each type in the data dictionary to a function.

    The return value is a table that provides a
    mapping from id_type to a function (allocator,
    initializer, validator etc...).

    The function is retrieved by calling the
    specified higher-order-function _get_function
    with the id_type (key) and list_node (value)
    from the cfg_data.

    """
    map_function = dict()
    for (id_type, list_node) in cfg_data.items():
        map_function[id_type] = _get_function(id_type, list_node)
    return map_function


# -----------------------------------------------------------------------------
def _allocator(id_type, list_node):
    """
    Return an allocator function for the specified type.

    """
    prototype = _make_prototype_instance(id_type, list_node)
    return lambda: copy.copy(getattr(prototype, 'data', prototype))


# -----------------------------------------------------------------------------
def _make_prototype_instance(id_type, list_node):  # pylint: disable=W0613
    """
    Return a prototype data instance for the specified type.

    """
    blacklist = set(('compound_type',
                     'compound_type_scope_closer'))

    prototype = pl.stableflow.util.PathDict()
    for node in list_node:

        if node['category'] in blacklist:
            continue

        typeinfo = node['typeinfo']

        # Numpy types
        if typeinfo['np'] is not None:
            if node['shape'] is not None:
                value = numpy.zeros(shape = node['shape'],
                                    dtype = node['typeinfo']['np'],
                                    order = node['memory_order'])
            else:
                dtype = numpy.dtype(node['typeinfo']['np'])
                value = dtype.type()

        # Pure python types
        elif typeinfo['py'] is not None:
            value = node['typeinfo']['py']()

        else:
            raise RuntimeError('Neither numpy nor python typeinfo found.')

        dst_path = node['dst_path']
        if dst_path:
            prototype[dst_path] = value
        else:
            prototype = value

    return prototype


# -----------------------------------------------------------------------------
def _initializer(id_type, list_node):  # pylint: disable=W0613
    """
    Return an initializer function for the specified type.

    """
    default_initializer_list = _get_initializers_for_all_nodes(list_node)

    # -------------------------------------------------------------------------
    def _initialize_all_fields(data_structure,
                               initializer_list = None):
        """
        Initialize all known entries in the specified data structure.

        """
        if initializer_list is None:
            initializer_list = default_initializer_list
        path_dict = pl.stableflow.util.PathDict(data_structure)
        for initializer_function in initializer_list:
            initializer_function(path_dict)

    return _initialize_all_fields


# -----------------------------------------------------------------------------
def _get_initializers_for_all_nodes(list_node):
    """
    Return a list of initializer functions, one for each node in the list.

    """
    blacklist = set(('compound_type',
                     'compound_type_scope_closer'))

    initializer_list = list(_get_initializer_for_one_node(node)
                                    for node in list_node
                                        if node['category'] not in blacklist)

    return initializer_list


# -----------------------------------------------------------------------------
def _get_initializer_for_one_node(node):
    """
    Return an initializer function for the specified node.

    """
    path  = node['dst_path']
    dtype = numpy.dtype(node['typeinfo']['id'])
    value = dtype.type(node['preset'])

    if node['shape'] is None:

        # -----------------------------------------------------------------
        def _initialize_one_field(path_dict, path = path, value = value):
            """
            Initialize an entry in path_dict with the specifed value.

            """
            path_dict[path] = value

    else:

        # -----------------------------------------------------------------
        def _initialize_one_field(path_dict, path = path, value = value):
            """
            Initialize an entry in path_dict with the specifed value.

            """
            path_dict[path].fill(value)

    return _initialize_one_field


# -----------------------------------------------------------------------------
def _validator(id_type, list_node):  # pylint: disable=W0613
    """
    Return a validator function for the specified type.

    """
    # blacklist = set(('compound_type',
    #                  'compound_type_scope_closer'))

    # path_dict = pl.stableflow.util.PathDict()
    # for node in list_node:
    #     if node['category'] in blacklist:
    #         continue

    #     path    = node['dst_path']
    #     id_type = node['typeinfo']['id']
    #     dtype   = numpy.dtype(id_type)
    #     shape   = node['shape']

    #     if shape is None:
    #         path_dict[path] = good.Schema(dtype.type)
    #     else:
    #         dtype = numpy.dtype(id_type)
    #         path_dict[path] = good.All(
    #             good.Type(numpy.ndarray),
    #             good.Check(
    #                    lambda ndarray, dtype = dtype: ndarray.dtype == dtype,
    #                    message  = 'Numpy ndarray of wrong type.',
    #                    expected = 'numpy.dtype({type})'.format(
    #                                                   type = dtype.name)))
    # return good.Schema(path_dict._data)
    return None
