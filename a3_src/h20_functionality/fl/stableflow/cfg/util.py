# -*- coding: utf-8 -*-
"""
Module of configuration related utility functions.

"""


# -----------------------------------------------------------------------------
def apply(data, address, value, delim_cfg_addr = '.'):
    """
    Apply a single configuration field override on the specified path.

    """

    addr_parts = address.split(delim_cfg_addr)
    subtree    = data

    for (key, key_next) in zip(addr_parts[:-1], addr_parts[1:]):
        subtree = _extend_subtree_if_reuqired(subtree, key, key_next)
        if isinstance(subtree, list):
            subtree = subtree[int(key)]
        else:
            subtree = subtree[key]

    key = addr_parts[-1]
    if isinstance(subtree, list):
        subtree[int(key)] = value
    else:
        subtree[key] = value
    return data


# -----------------------------------------------------------------------------
def _extend_subtree_if_reuqired(subtree, key, key_next):
    """
    Extend the subtree if the key is not present.

    This function assumes that the tree is made
    of lists and/or dictionaries and that lists 
    are uniform and contain only dictionaries
    or only other lists.

    """

    if isinstance(key_next, int) or key_next.isdigit():
        type_next = list
    else:
        type_next = dict

    if isinstance(subtree, list):
        idx_new = int(key)
        idx_max = len(subtree) - 1
        if idx_new > idx_max:
            count_missing = idx_new - idx_max
            for _ in range(count_missing):  # Assumes uniform list.
                subtree.append(type_next())

    else:  # is dictionary
        if key not in subtree:
            subtree[key] = type_next()

    return subtree


# =============================================================================
class SubstitutionTable():  # pylint: disable=R0903
    """
    Provide a nice syntax for conditional substitution logic.

    """

    # -------------------------------------------------------------------------
    def __init__(self, lut):
        """
        Construct a SubstitutionTable instance with the specified LUT.

        """

        self._lut = lut

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Return self._lut[key] if key in self._lut else key.

        """

        try:
            return self._lut[key] if key in self._lut else key
        except TypeError:
            return key
