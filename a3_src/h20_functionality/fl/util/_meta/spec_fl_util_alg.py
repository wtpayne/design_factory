# -*- coding: utf-8 -*-
"""
Functional specification for fl.util.alg

"""


import textwrap
import time
import warnings

import pytest


# =============================================================================
class SpecifyFlUtilIo:
    """
    Spec for the fl.util.alg module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        fl.util.alg can be imported with no errors.

        """
        import fl.util.alg

# =============================================================================
class SpecifyFlUtilIsLeaf:
    """
    Spec for the fl.util.alg.is_leaf function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_detects_simple_data_types_as_leaf_nodes(self):
        """
        fl.util.alg.is_leaf detects simple data typees as leaf elements.

        """
        import fl.util.alg

        # Test with simple data types
        assert fl.util.alg.is_leaf(5)
        assert fl.util.alg.is_leaf(5.5)
        assert fl.util.alg.is_leaf("Hello")
        assert fl.util.alg.is_leaf(True)
        assert fl.util.alg.is_leaf(3+4j)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_detects_coroutines_and_generators_as_leaf_nodes(self):
        """
        fl.util.alg.is_leaf detects coroutines and generators as non-leaf elements.

        """
        import fl.util.alg

        # Test with generator
        generator = (x for x in range(10))
        assert fl.util.alg.is_leaf(generator)

        # Test with coroutine
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            async def coroutine():
                pass
            assert fl.util.alg.is_leaf(coroutine())

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_detects_containers_as_non_leaf_nodes(self):
        """
        fl.util.alg.is_leaf detects containers as non-leaf elements.

        """
        import fl.util.alg

        # Test with mapping
        assert not fl.util.alg.is_leaf({"a": 1, "b": 2})

        # Test with iterable types
        assert not fl.util.alg.is_leaf([1, 2, 3])
        assert not fl.util.alg.is_leaf((1, 2, 3))
        assert not fl.util.alg.is_leaf({1, 2, 3})

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_detects_lists_of_simple_data_types_as_fat_leaf_nodes(self):
        """
        fl.util.alg.is_leaf detects lists of simple data types as fat leaves.

        """
        import fl.util.alg

        # Test with 'fat leaves' option
        assert fl.util.alg.is_leaf([1, 2, 3],     use_fat_leaves = True)
        assert fl.util.alg.is_leaf((1, 2, 3),     use_fat_leaves = True)
        assert fl.util.alg.is_leaf([1, 2.3, '4'], use_fat_leaves = True)
        assert fl.util.alg.is_leaf((1, 2.3, '4'), use_fat_leaves = True)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_detects_lists_of_complex_data_types_as_non_fat_leaf_nodes(self):
        """
        fl.util.alg.is_leaf detects lists of complex data types as non fat leaves.

        """
        import fl.util.alg

        # Test with 'fat leaves' option
        assert not fl.util.alg.is_leaf([1, dict(),  3], use_fat_leaves = True)
        assert not fl.util.alg.is_leaf([1, dict(),  3], use_fat_leaves = True)
        assert not fl.util.alg.is_leaf((1, tuple(), 3), use_fat_leaves = True)
        assert not fl.util.alg.is_leaf((1, tuple(), 3), use_fat_leaves = True)
        assert not fl.util.alg.is_leaf((1, list(),  3), use_fat_leaves = True)
        assert not fl.util.alg.is_leaf((1, list(),  3), use_fat_leaves = True)
