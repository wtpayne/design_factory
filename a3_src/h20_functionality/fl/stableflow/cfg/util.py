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

    for key in addr_parts[:-1]:
        if key not in subtree:
            subtree[key] = dict()
        subtree = subtree[key]
    key = addr_parts[-1]
    subtree[key] = value
    return data


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
