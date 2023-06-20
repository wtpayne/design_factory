# -*- coding: utf-8 -*-
"""
Functional specification for the fl.stableflow.cfg.override module.

"""

import copy

import pytest


# =============================================================================
class SpecifyApply:
    """
    Spec for the apply function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_changes_nothing_when_no_override_is_given(
                                                self, valid_normalized_config):
        """
        Check apply makes no changes when the override is None.

        """
        import fl.stableflow.cfg.override  # pylint: disable=C0415

        cfg_orig = copy.deepcopy(valid_normalized_config)
        cfg_mod = fl.stableflow.cfg.override.apply(valid_normalized_config, None)

        assert cfg_orig == cfg_mod

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_override_a_single_field(self, valid_normalized_config):
        """
        Check apply makes no changes when the override is None.

        """
        import fl.stableflow.cfg.override  # pylint: disable=C0415

        cfg         = valid_normalized_config
        id_sys_orig = copy.deepcopy(cfg['system']['id_system'])

        fl.stableflow.cfg.override.apply(
                                cfg, ('system.id_system', 'some_other_name'))

        id_sys_mod  = cfg['system']['id_system']
        assert id_sys_orig != id_sys_mod
        assert id_sys_mod  == 'some_other_name'

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_override_multiple_fields(self, valid_normalized_config):
        """
        Check apply makes no changes when the override is None.

        """
        import fl.stableflow.cfg.override  # pylint: disable=C0415

        cfg           = valid_normalized_config
        id_sys_orig   = copy.deepcopy(cfg['system']['id_system'])
        hostname_orig = copy.deepcopy(cfg['host']['some_host']['hostname'])

        fl.stableflow.cfg.override.apply(
                            cfg,
                            ('system:id_system', 'some_other_name',
                             'host:some_host:hostname', '111.111.111.111'),
                            delim_cfg_addr = ':')

        id_sys_mod           = cfg['system']['id_system']
        assert id_sys_orig   != id_sys_mod
        assert id_sys_mod    == 'some_other_name'

        hostname_mod         = cfg['host']['some_host']['hostname']
        assert hostname_orig != hostname_mod
        assert hostname_mod  == '111.111.111.111'
