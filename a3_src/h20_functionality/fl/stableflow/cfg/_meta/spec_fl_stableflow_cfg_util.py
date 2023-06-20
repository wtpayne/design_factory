# -*- coding: utf-8 -*-
"""
Functional specification for the fl.stableflow.cfg.util module.

"""


import pytest


# =============================================================================
class SpecifyApply:
    """
    Spec for the fl.stableflow.cfg.util.apply() function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_modifies_nested_struct_field_values_by_path(self):
        """
        Check apply can be used to modify nested struct fields.

        """
        import fl.stableflow.cfg.util  # pylint: disable=C0415

        data = {'a': {'b': 1}}
        data = fl.stableflow.cfg.util.apply(data, 'a.b', 2)
        assert data['a']['b'] == 2

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_use_different_delimiters(self):
        """
        Check apply can be used to modify nested struct fields.

        """
        import fl.stableflow.cfg.util  # pylint: disable=C0415

        data = {'a': {'b': 1}}
        data = fl.stableflow.cfg.util.apply(
                                        data, 'a:b', 2, delim_cfg_addr=':')
        assert data['a']['b'] == 2
