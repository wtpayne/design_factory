# -*- coding: utf-8 -*-
"""
---

title:
    "Utility algorithms module."

description:
    "This module contains various utility
    algorithms."

id:
    "bce62560-5aac-4b5a-9052-408ba32e070f"

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
import collections.abc
import inspect
import typing


# -----------------------------------------------------------------------------
def walk(obj:            typing.Any,          # pylint: disable=R0912,R0913
         gen_leaf:       bool                 = False,
         gen_nonleaf:    bool                 = False,
         gen_path:       bool                 = False,
         gen_obj:        bool                 = False,
         use_fat_leaves: bool                 = False,
         path:           typing.Tuple         = (),
         memo:           typing.Optional[set] = None) -> typing.Iterator[
                                                            typing.Union[
                                                                typing.Tuple,
                                                                typing.Any]]:
    """
    Generate depth-first traversal over tree of mappings and other iterables.

    This function performs a depth-first,
    left-to-right recursive traversal over
    the provided data structure, which is
    assumed to consist of a finite, treelike
    arrangement of nested collections.Mapping
    and collections.Iterable types.

    The function can be configured to yield
    information about nodes in the tree:
    leaf nodes, non-leaf (internal) nodes,
    or both. Additionally, the information
    yielded can be configured to include
    the path to the node and/or the object
    at the node itself.

    Adapted from:

        {http://code.activestate.com/recipes/577982-recursively-walk-python-objects/}

    Parameters:

        obj (object):                       The object to be traversed.

        gen_leaf (bool, optional):          If True, leaf nodes will be
                                            generated. Default is False.

        gen_nonleaf (bool, optional):       If True, non-leaf nodes will be
                                            generated. Default is False.

        gen_path (bool, optional):          If True, the path to the node will
                                            be generated. Default is False.

        gen_obj (bool, optional):           If True, the object at the node
                                            will be generated. Default is
                                            False.

        use_fat_leaves (bool, optional):    If True, simple data structures
                                            like lists or tuples of integers
                                            will be considered as leaf rather
                                            than nonleaf nodes.

        path (tuple, optional):             A tuple representing the path to
                                            the current node. Default is an
                                            empty tuple.

        memo (set, optional):               A set used to track visited objects
                                            to avoid infinite recursion.

    Yields:

        tuple or object:                    The configured information for each
                                            node in the traversal.

    Examples:

        >>> data = {'a': 1, 'b': {'c': 2, 'd': [3, 4]}}
        >>> list(walk(data, gen_leaf=True, gen_path=True))
        [(('a',), 1), (('b', 'c'), 2), (('b', 'd', 0), 3), (('b', 'd', 1), 4)]

    ---
    type:   generator
    ...

    """
    # If the object is elemental, it cannot be
    # decomposed, so we must bottom out the
    # recursion and yield the object and its'
    # path before returning control back up
    # the stack.
    #
    if is_leaf(obj, use_fat_leaves = use_fat_leaves):
        if gen_leaf:
            if gen_path and gen_obj:
                yield (path, obj)
            elif gen_path:
                yield path
            elif gen_obj:
                yield obj
        return

    # Since this is a recursive function, we need
    # to be on our guard against any references
    # to objects back up the call stack (closer
    # to the root of the tree). Any such
    # references would be circular, leading to
    # an infinite tree, and causing us to blow
    # our stack in a fit of unbounded recursion.
    #
    # If we detect that we've already visited
    # this object (using identity not equality),
    # then the safe thing to do is to halt the
    # recursive descent and return control back
    # up the stack.
    #
    _id = id(obj)
    if memo is None:
        memo = set()
    if _id in memo:
        return
    memo.add(_id)

    # If the object is not elemental (i.e. it is
    # an Iterable), then it may be decomposed, so
    # we should recurse down into each component,
    # yielding the results as we go. Of course,
    # we need different iteration functions for
    # mappings vs. other iterables.
    #
    def mapiter(mapping):
        """
        Return an iterator over the specified mapping or other iterable.

        This function selects the appropriate
        iteration function to use.

        """
        return getattr(mapping, 'items', mapping.items)()
    itfcn = mapiter if isinstance(obj, collections.abc.Mapping) else enumerate

    for pathpart, component in itfcn(obj):

        childpath = path + (pathpart,)
        if gen_nonleaf:
            if gen_path and gen_obj:
                yield (childpath, component)
            elif gen_path:
                yield childpath
            elif gen_obj:
                yield component

        for result in walk(obj            = component,
                           gen_leaf       = gen_leaf,
                           gen_nonleaf    = gen_nonleaf,
                           gen_path       = gen_path,
                           gen_obj        = gen_obj,
                           use_fat_leaves = use_fat_leaves,
                           path           = childpath,
                           memo           = memo):
            yield result

    # We only need to guard against infinite
    # recursion within a branch of the call-tree.
    # There is no danger in visiting the same item
    # instance in sibling branches, so we can
    # forget about objects once we are done
    # with them and about to pop the stack.
    #
    memo.remove(_id)

    return


# -----------------------------------------------------------------------------
def is_leaf(obj, use_fat_leaves = False):
    """
    Return True if obj is a leaf data type, False otherwise.

    The function identifies a 'leaf' as a data
    type which doesn't contain any nested types.

    Certain types are always considered 'leaves',
    such as strings, int, float, bool, generators,
    and coroutines.

    Certain types are never considered 'leaves',
    such as collections.abc.Mapping types.

    If 'use_fat_leaves' is set to True, simple
    lists and tuples containing only fundamental
    numeric types or strings are also considered
    to be 'leaves'.

    Parameters:

        obj (object):                    The object to be evaluated.

        use_fat_leaves (bool, optional): Indicates if simple lists and tuples
                                         containing only fundamental numeric
                                         types or strings should also be
                                         considered as 'leaves'. Defaults to
                                         False.

    Returns:

        bool: True if the object is a leaf data type, False otherwise.

    Raises:

        None

    Examples:

        >>> is_leaf(5)
        True

        >>> is_leaf([1, 2, 3], use_fat_leaves=True)
        True

        >>> is_leaf({1: 'a'})
        False

    """

    # Mappings like Bureau and dict are never
    # leaves of any sort, whereas atomic types
    # like int and float and bool are always
    # considered to be leaf items.
    #
    is_never_leaf = isinstance(obj, collections.abc.Mapping)
    if is_never_leaf:
        return False

    # If a type is not iterable, then it is
    # always considered to be a leaf. Strings,
    # generators and coroutines are similarly
    # always considered to be leaves, even though
    # they are iterable. Generators and coroutines
    # have to be considered as leaves as a
    # practical matter since they can easily loop
    # forever.
    #
    is_always_leaf = (    (not isinstance(obj, collections.abc.Iterable))
                       or is_string(obj)
                       or inspect.isgenerator(obj)
                       or inspect.iscoroutine(obj))
    if is_always_leaf:
        return True

    # Tuples and lists may or may not be leaves
    # depending on whether 'use_fat_leaves' is
    # enabled. ('Fat' leaves are lists or tuples
    # filled only with atomic data types).
    #
    is_maybe_leaf = use_fat_leaves and isinstance(obj, (list, tuple))
    if is_maybe_leaf:
        tup_atomic  = (int, float, complex, bool, str)
        is_fat_leaf = all((isinstance(it, tup_atomic) for it in obj))
        return is_fat_leaf

    # What we have left are any other iterable
    # data types. Possibly a bit risky, but for
    # now we assume that they are non-leaf
    # data types and attempt to iterate through
    # them. (Although may be safer in future
    # to change this to return True or at least
    # issue a warning.)
    #
    return False


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
def topological_sort(map_forward, map_backward = None):
    """
    Return nodes as list of sets of equivalent rank in topological order.

    Get the tranche list for the directed
    acyclic graph (data flow graph) of the
    entire diagram. Each tranche is a set
    of id_node strings indicating nodes with
    equivalent rank in the topological sort
    order.

    """
    # If the backward map has not been
    # specified, we can easily build it
    # by inverting the (bijective) forward
    # mapping.
    #
    if map_backward is None:
        map_backward = collections.defaultdict(set)
        for (key, set_value) in map_forward.items():
            for value in set_value:
                map_backward[value].add(key)

    set_node_out     = set(map_forward.keys())   # nodes with outbound edge(s)
    set_node_in      = set(map_backward.keys())  # nodes With inbound edge(s)
    set_node_sources = set_node_out - set_node_in

    # Build a map from id_node -> indegree
    # (count of inbound edges), populated
    # from the map_backward dict.
    #
    map_indegree = dict((key, 0) for key in set_node_sources)
    for (key, inbound) in map_backward.items():
        map_indegree[key] = len(inbound)

    # The output of the topological sort
    # is a partial ordering represented
    # as a list of sets; each set representing
    # nodes of equal rank. Here we create
    # the output list and fill it with
    # nodes at rank zero, removing them
    # from the graph.
    #
    set_rank_zero = _nodes_at_count_zero(map_indegree)
    list_set_ranks = [set_rank_zero]
    _del_items(map_indegree, set_rank_zero)

    # The topological sort algorithm
    # uses breadth first search. An
    # indegree number is maintained
    # for all nodes remaining in the
    # graph. At each iteration, the
    # 'source' nodes (indegree zero)
    # are taken from the graph and
    # added to the output, and the
    # indegree of immediate downstream
    # neighbors is decremented.
    #
    while True:

        # Maintain indegree number.
        set_prev = list_set_ranks[-1]
        for id_node in _list_downstream_neighbors(set_prev, map_forward):
            map_indegree[id_node] -= 1

        # Find the next rank - terminate
        # if it does not exist.
        #
        set_next = _nodes_at_count_zero(map_indegree)
        if not set_next:
            break

        # If the next rank does exist,
        # remove it from the graph and
        # add it to the list of ranks.
        #
        _del_items(map_indegree, set_next)
        list_set_ranks.append(set_next)

    return list_set_ranks


# -----------------------------------------------------------------------------
def _nodes_at_count_zero(map_indegree):
    """
    Return the set of id_node with input degree zero.

    """
    return set(key for (key, count) in map_indegree.items() if count == 0)


# -----------------------------------------------------------------------------
def _del_items(map_data, set_keys):
    """
    Delete the specified items from the dict.

    """
    for key in set_keys:
        del map_data[key]


# -----------------------------------------------------------------------------
def _list_downstream_neighbors(set_id_node, map_forward):
    """
    Return the list of downstream neighbors from the specified edge map.

    The edge map should be provided as a dict
    mapping from upstream nodes to downstream
    nodes.

    """
    list_neighbors = list()
    for id_node in set_id_node:
        if id_node in map_forward:
            for id_node_downstream in map_forward[id_node]:
                list_neighbors.append(id_node_downstream)
    return list_neighbors


# -------------------------------------------------------------------------
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
