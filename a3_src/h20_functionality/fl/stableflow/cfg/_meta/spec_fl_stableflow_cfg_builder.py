# -*- coding: utf-8 -*-
"""
Functional specification for the fl.stableflow.cfg.builder module.

"""


import pytest


# =============================================================================
class SpecifySetSystemId:
    """
    Spec for the builder.set_system_id function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.set_system_id returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.set_system_id(
                                        cfg       = valid_normalized_config,
                                        id_system = 'new_system_id')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyAddHost:
    """
    Spec for the builder.add_host function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.add_host returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_host(
                                        cfg     = valid_normalized_config,
                                        id_host = 'new_host_id')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyRemoveHost:
    """
    Spec for the builder.remove_host function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.remove_host returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_host(
                                        cfg     = valid_normalized_config,
                                        id_host = 'new_host_id')
        fl.stableflow.cfg.builder.remove_host(
                                        cfg     = valid_normalized_config,
                                        id_host = 'new_host_id')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyAddProcess:
    """
    Spec for the builder.add_process function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.add_process returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_process(
                                        cfg        = valid_normalized_config,
                                        id_process = 'new_process_id',
                                        id_host    = 'some_host')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyRemoveProcess:
    """
    Spec for the builder.remove_process function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.remove_process returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_process(
                                        cfg        = valid_normalized_config,
                                        id_process = 'new_process_id',
                                        id_host    = 'some_host')
        fl.stableflow.cfg.builder.remove_process(
                                        cfg        = valid_normalized_config,
                                        id_process = 'new_process_id')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyAddNode:
    """
    Spec for the builder.add_node function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.add_node returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_node(
                        cfg           = valid_normalized_config,
                        id_node       = 'new_node_id',
                        functionality = {
                            'requirement': 'some_requirement',
                            'py_module':   'some.importable.module'},
                        id_process    = 'some_process')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyRemoveNode:
    """
    Spec for the builder.remove_node function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.remove_node returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_node(
                    cfg           = valid_normalized_config,
                    id_node       = 'new_node_id',
                    functionality = {'py_module': 'some.importable.module'},
                    id_process    = 'some_process')
        fl.stableflow.cfg.builder.remove_node(
                                        cfg     = valid_normalized_config,
                                        id_node = 'new_node_id')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyAddEdge:
    """
    Spec for the builder.add_edge function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.add_edge returns valid configuration.

        """

        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_edge(
                                        cfg     = valid_normalized_config,
                                        id_src  = 'some_node',
                                        src_ref = 'outputs.foo',
                                        id_dst  = 'some_node',
                                        dst_ref = 'inputs.foo',
                                        data    = 'some_data_type')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyRemoveEdge:
    """
    Spec for the builder.remove_edge function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.remove_edge returns valid configuration.

        """
        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_edge(
                                        cfg     = valid_normalized_config,
                                        id_src  = 'some_node',
                                        src_ref = 'output.new_port',
                                        id_dst  = 'some_node',
                                        dst_ref = 'input.new_port',
                                        data    = 'some_data_type')
        fl.stableflow.cfg.builder.remove_edge(
                                            cfg = valid_normalized_config,
                                            src = 'some_node.output.new_port',
                                            dst = 'some_node.input.new_port')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyAddData:
    """
    Spec for the builder.add_data function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.add_data returns valid configuration.

        """
        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_data(cfg       = valid_normalized_config,
                                           id_data   = 'new_type_alias',
                                           spec_data = 'py_dict')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)


# =============================================================================
class SpecifyRemoveData:
    """
    Spec for the builder.remove_data function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_valid_configuration(self, valid_normalized_config):
        """
        Check builder.remove_data returns valid configuration.

        """
        import fl.stableflow.cfg.builder   # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        fl.stableflow.cfg.builder.add_data(cfg       = valid_normalized_config,
                                           id_data   = 'new_type_alias',
                                           spec_data = 'py_dict')
        fl.stableflow.cfg.builder.remove_data(
                                            cfg     = valid_normalized_config,
                                            id_data = 'new_type_alias')
        fl.stableflow.cfg.validate.normalized(valid_normalized_config)
