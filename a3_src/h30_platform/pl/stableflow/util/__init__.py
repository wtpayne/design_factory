# -*- coding: utf-8 -*-
"""
Module of utility functions and classes used across the stableflow system.

"""


import collections
import collections.abc
import functools
import itertools
import string

import dill

import fl.util.alg


# =============================================================================
class PathDict(collections.UserDict):  # pylint: disable=R0901
    """
    Custom dictionary class supporting path-tuple based access.

    """

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Return a PathDict instance.

        """
        self.delim = '.'
        super().__init__(*args, **kwargs)

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Return a reference to the specified item in data.

        """
        reference = self.data
        for name in _ensure_list(key, delim = self.delim):
            reference = reference[name]
        return reference

    # -------------------------------------------------------------------------
    def __setitem__(self, key, value):
        """
        Return a reference to the specified item in data.

        """
        reference = self.data

        # If we want to disable string
        # to list conversion, we can
        # set delim to None.
        #
        if self.delim is not None:
            key = _ensure_list(key, delim = self.delim)

        reference = self.data
        for name in key[:-1]:
            if name not in reference:
                reference[name] = dict()
            reference = reference[name]
        if key:
            reference[key[-1]] = value
        else:
            reference = value


# -----------------------------------------------------------------------------
def clear_outputs(outputs,
                  iter_name_output    = None,
                  iter_field_to_clear = None,
                  has_ena             = True):
    """
`   Clear the specified fields in the specified outputs.

    """
    if iter_name_output is None:
        iter_name_output = tuple(outputs.keys())

    if iter_field_to_clear is None:
        iter_field_to_clear = ('list',)

    map_ctors = {
        'list': list,
        'map':  dict,
        'set':  set,
    }

    for id_out in iter_name_output:
        if id_out not in outputs:
            continue
        if has_ena:
            outputs[id_out]['ena'] = False
        for id_field in iter_field_to_clear:
            if id_field not in outputs[id_out]:
                outputs[id_out][id_field] = map_ctors[id_field]()
            else:
                outputs[id_out][id_field].clear()


# -----------------------------------------------------------------------------
def format_all_strings(map_data):
    """
    Return the specified data structure with formatted string fields.

    The input shall be a python dict, list or tuple,
    which may be nested to an arbitrary depth.
    This data structure can be seen as a tree.
    The internal branches of this tree shall be
    of some dict, list or tuple type, and the
    leaves of the tree shall be values of some
    boolean, numeric, or string type.

    Leaves which are of string type may either be
    PEP3101 format strings, or they may be 'vanilla'
    python strings.

    For all PEP3101 format strings in the data
    structure, the name of the format string
    arguments shall be a dot delimited path which
    references some other string leaf in the input
    data structure.

    In this way, each argument found in a format
    strings leaf shall provide a reference to some
    other string (format string or otherwise) in
    the data structure, forming an implicit
    directed graph of references.

    This implicit directed graph shall be acyclic.

    The purpose of this function is to replace the
    format strings with their 'formatted' output,
    using the topological ordering of the implicit
    graph of references to determine the sequence
    of formatting operations.

    """
    map_dst = collections.defaultdict(set)  # id_field -> {path_to_dst}
    map_src = dict()                        # id_field -> path_to_src
    for (tup_path, leaf) in fl.util.alg.walk(map_data,
                                             gen_leaf    = True,
                                             gen_nonleaf = False,
                                             gen_path    = True,
                                             gen_obj     = True):

        # Any field is a potential source of a parameter value.
        id_field          = '.'.join(str(item) for item in tup_path)
        map_src[id_field] = tup_path

        # Format strings are "destinations" consuming parameter values.
        if is_format_string(leaf):
            for id_field in iter_format_string_fields(leaf):
                map_dst[id_field].add(tup_path)

    # Build the dependency graph between leaves in the content tree.
    map_edge = collections.defaultdict(set)  # path_to_src -> {path_to_dst}
    for (id_field, set_path_dst) in map_dst.items():
        assert id_field in map_src
        path_src = map_src[id_field]
        map_edge[path_src].update(set_path_dst)

    # Format content in topological order.
    for set_rank in fl.util.alg.topological_sort(map_edge):
        for tup_path in sorted(set_rank):
            cursor = map_data
            parent = None
            for key in tup_path:
                parent = cursor
                cursor = cursor[key]
            if is_format_string(cursor):
                parent[tup_path[-1]] = cursor.format(**map_data)

    return map_data


# -----------------------------------------------------------------------------
def is_format_string(maybe_fmt):
    """
    Return true if the supplied string is a format string.

    """
    if not is_string(maybe_fmt):
        return False
    iter_fields   = iter_format_string_fields(maybe_fmt)
    is_fmt_string = any(field is not None for field in iter_fields)
    return is_fmt_string


# -----------------------------------------------------------------------------
def is_string(obj):
    """
    Return true if obj is a string. Works in Python 2 and Python 3.

    """
    return isinstance(obj, string_types())


# -----------------------------------------------------------------------------
def string_types():
    """
    Return the string types for the current Python version.

    """
    is_python_2 = str is bytes
    if is_python_2:  # pylint: disable=R1705
        return (str, unicode)  # pylint: disable=E0602
    else:
        return (str, bytes)


# -----------------------------------------------------------------------------
def iter_format_string_fields(fmt_string):
    """
    Return an iterable over the field names in the specified format string.

    """
    return (tup[1] for tup in string.Formatter().parse(fmt_string)
                                                        if tup[1] is not None)


# -----------------------------------------------------------------------------
def _ensure_list(key, delim):
    """
    Ensure that key is represented as a list of names.

    """
    if isinstance(key, str):
        list_str  = key.split(delim)
        list_name = []
        for str_name in list_str:
            try:
                name = int(str_name)
            except ValueError:
                name = str_name
            list_name.append(name)
        key = list_name
    return key


# -----------------------------------------------------------------------------
def first(iterable):
    """
    Return the first item in the specified iterable.

    """
    return next(iter(iterable))


# -----------------------------------------------------------------------------
def gen_path_value_pairs_depth_first(map):
    """
    Yield (path, value) pairs taken from map in depth first order.

    """
    stack = collections.deque(_reversed_key_value_pairs(map))

    while True:

        try:
            (path_parent, value_parent) = stack.pop()
        except IndexError:
            return

        if not isinstance(path_parent, list):
            path_parent = [path_parent]

        if is_container(value_parent):
            for (key_child, value_child) in _reversed_key_value_pairs(
                                                                value_parent):

                stack.append((path_parent + [key_child], value_child))

        yield (tuple(path_parent), value_parent)


# -----------------------------------------------------------------------------
def _reversed_key_value_pairs(value):
    """
    Return a reversed list of the items taken from the specified dict or list.

    Input value must be a dict or a list.

    """
    if isinstance(value, dict):
        iter_key_value_pairs = value.items()

    if isinstance(value, list):
        iter_key_value_pairs = enumerate(value)

    return sorted(iter_key_value_pairs, reverse = True)


# -----------------------------------------------------------------------------
def is_container(value):
    """
    Return True iff the specified value is of a type that contains children.

    The biggest difficulty here is in distinguishing
    strings, byte arrays etc... from other sequence
    containers -- All we can really do is check
    explicitly whether they are instances of list()
    or tuple(). We can be more generic with Mappings
    and Sets since we have a suitable abstract base
    type for these.

    """
    is_map   = isinstance(value, collections.abc.Mapping)
    is_set   = isinstance(value, collections.abc.Set)
    is_list  = isinstance(value, list)
    is_tuple = isinstance(value, tuple)
    return is_map or is_set or is_list or is_tuple


# -------------------------------------------------------------------------
def function_from_source(string_source):
    """
    Return the first function found in the specified source listing.

    This calls exec on the supplied string.

    """
    list_functions = list()
    fcn_locals     = dict()
    exec(string_source, dict(), fcn_locals)  # pylint: disable=W0122
    for value in fcn_locals.values():
        if callable(value):
            list_functions.append(value)
    assert len(list_functions) == 1
    return list_functions[0]


# -------------------------------------------------------------------------
def function_from_dill(pickled_function):
    """
    Return the function found in the specified pickle.

    """
    return dill.loads(pickled_function)


# =============================================================================
class RestrictedWriteDict(collections.UserDict):  # pylint: disable=R0901
    """
    Custom dictionary class supporting restrictions on write operations.

    A common mistake is to assign to output data
    structures directly, accidentally replacing
    them with a new container. This breaks shared
    reference in-memory communication, and can be
    a difficult bug to fix, as it causes
    in-process communication between python nodes
    to fail silently.

        outputs['X'] = {...}         # NO!
        outputs['X'].update({...})   # YES!

    This class is a quality-of-life fix for this
    problem. It raises a runtime error immediately
    if a component unwittingly attempts to replace
    a field value.

    """

    # -------------------------------------------------------------------------
    def _stableflow_framework_internal_setitem(self, key, value):
        """
        Set a dict item, bypassing restrictions.

        This should only be called by the stableflow
        framework internally.

        Due to the way container sharing is used
        for intra-process communication, errors
        may be introduced if it is called
        directly by the step function.

        """
        super().__setitem__(key, value)

    # -------------------------------------------------------------------------
    def __setitem__(self, key, value):
        """
        Raise RuntimeError to prevent inadvertent overwrite of edge containers.

        """
        raise RuntimeError('Ensure you are updating output (or input) '
                           'container content rather than changing the '
                           'identity of the containers themselves.')
