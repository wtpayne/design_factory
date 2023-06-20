# -*- coding: utf-8 -*-
"""
Module with class for tracking unbound references in data type configurations.

"""


import collections
import copy


# =============================================================================
class GapTable():
    """
    Tracks the location of unbound type references in data configuration.

    """

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Construct a new GapTable instance.

        """
        ddict       = collections.defaultdict
        self._table = ddict(lambda: ddict(list))

    # -------------------------------------------------------------------------
    def add(self,
            incomplete_type,
            missing_type,
            gap_parent_path,
            gap_field):
        """
        Append new gap information to the relevant gap table entry.

        """
        self._table[incomplete_type][missing_type].append(
                                                (gap_parent_path, gap_field))

    # -------------------------------------------------------------------------
    def fill_all(self, output):
        """
        Fill all the gaps in the output data structure.

        This method uses a greedy algorithm, filling
        as many gaps as possible on each iteration.

        Each iteration of the below loop exhausts
        all available 'ready_types' to fill as many
        gaps as possible.

        This will then result in newly complete
        types which can be used in the next iteration.

        This process continues until all types are
        completely defined.

        We can only fill a gap if the type that is
        missing from the gap has been fully defined
        at the time of the current iteration.
        The set of such types is called the ready set:

          ready_set = missing_set - incomplete_set

        When all of the gaps are filled in a structure,
        it is then removed from the incomplete_set.
        This means that if it is needed by one or
        more gaps, it will then be part of the ready
        set on the next iteration.

        """
        sanity_limit = 16
        for _ in range(sanity_limit):

            if self._is_finished():  # No gaps left to fill.
                break

            ready_set = self._ready_set()
            if not ready_set:
                # We have gaps but no ready types.
                # Error is either cyclic reference, or undefined type.
                # TODO: Detect error type and give useful error message.
                raise RuntimeError('Undefined type or cyclic reference.')

            self._fill_gaps_with_ready_types(output, ready_set)

        if not self._is_finished():
            raise RuntimeError('Logic error')

    # -------------------------------------------------------------------------
    def _is_finished(self):
        """
        Return true if all gaps have been filled.

        """
        return len(self._table) == 0

    # -------------------------------------------------------------------------
    def _ready_set(self):
        """
        Return the set of items which are missing and complete.

        I.e. the set of types which is needed (in the missing set) and also
        ready to be inserted (not in the incomplete set).

        """
        return self._missing_set() - self._incomplete_set()

    # -------------------------------------------------------------------------
    def _missing_set(self):
        """
        Return the set of data types missing from at least one incomplete type.

        """
        return set((
                key for item in self._table.values() for key in item.keys()))

    # -------------------------------------------------------------------------
    def _incomplete_set(self):
        """
        Return the set of all data types which are incomplete.

        """
        return set(self._table.keys())

    # -------------------------------------------------------------------------
    def _fill_gaps_with_ready_types(self, output, ready_set):
        """
        Use all available ready_type to fill gaps in incomplete_type.

        """
        incomplete_set = self._incomplete_set()
        for ready_type in ready_set:
            for incomplete_type in incomplete_set:
                self._fill_gaps_of_type(output, incomplete_type, ready_type)

    # -------------------------------------------------------------------------
    def _fill_gaps_of_type(self, output, incomplete_type, ready_type):
        """
        Fill any missing gaps of type 'ready_type' gaps in 'incomplete_type'.

        """
        for gap_tuple in self._table[incomplete_type][ready_type]:
            (parent_path, field)       = gap_tuple
            ready_path                 = (ready_type,)
            output[parent_path][field] = copy.deepcopy(output[ready_path])

        # Delete gap table entries after they are filled.
        del self._table[incomplete_type][ready_type]
        if not self._table[incomplete_type]:
            del self._table[incomplete_type]
