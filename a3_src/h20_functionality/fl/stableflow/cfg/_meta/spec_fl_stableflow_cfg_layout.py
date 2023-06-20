# -*- coding: utf-8 -*-
"""
Functional specification for the fl.stableflow.cfg.layout module.

"""


import pytest


# =============================================================================
class SpecifyFlStableflowCfgLayout:
    """
    Spec for the fl.stableflow.cfg.layout module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        fl.stableflow.cfg.layout can be imported with no errors.

        """
        import fl.stableflow.cfg.layout


# =============================================================================
class SpecifyFlStableflowCfgLayout_acyclincDataFlow:
    """
    Spec for the fl.stableflow.cfg.layout._acyclic_data_flow function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_handles_fan_out(self, valid_normalized_config):
        """
        Check fl.stableflow.cfg.layout._acyclic_data_flow does stuff.

        """
        import fl.stableflow.cfg.layout  # pylint: disable=C0415

        list_cfg_edge = [{'ipc_type':         'intra_process',
                          'list_id_process':  (),
                          'id_node_src':      'a',
                          'id_node_dst':      'b',
                          'dirn':             'feedforward'},
                         {'ipc_type':         'intra_process',
                          'list_id_process':  (),
                          'id_node_src':      'a',
                          'id_node_dst':      'c',
                          'dirn':             'feedforward'},
                         {'ipc_type':         'intra_process',
                          'list_id_process':  (),
                          'id_node_src':      'a',
                          'id_node_dst':      'd',
                          'dirn':             'feedforward'}]
        (map_forward,
         map_backward) = fl.stableflow.cfg.layout._acyclic_data_flow(
                                                iter_cfg_edge = list_cfg_edge)

        assert dict(map_forward)  == {'a': {'b', 'c', 'd'}}
        assert dict(map_backward) == {'b': {'a',},
                                      'c': {'a',},
                                      'd': {'a',}}
