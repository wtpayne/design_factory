# -*- coding: utf-8 -*-
"""
Functional specification for the fl.stableflow.cfg.data package.

"""


# =============================================================================
class SpecifyDenormalize:
    """
    Spec for the fl.stableflow.cfg.data.denormalize function.

    """

    # -------------------------------------------------------------------------
    def it_returns_valid_data(self, valid_partly_denormalized_config):
        """
        Check denormalize returns a valid denormalized config structure.

        """

        import fl.stableflow.cfg.data      # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415
        denormalized_config = fl.stableflow.cfg.data.denormalize(
                                            valid_partly_denormalized_config)
        fl.stableflow.cfg.validate.denormalized(denormalized_config)


# =============================================================================
class Specify_ExpandNode:
    """
    Spec for the fl.stableflow.cfg.data.denormalize function.

    """

    # -------------------------------------------------------------------------
    def it_returns_an_expanded_node(self):
        """
        Check denormalize returns a valid denormalized config structure.

        """

        import fl.stableflow.cfg.data  # pylint: disable=C0415
        named_type = fl.stableflow.cfg.data.FieldCategory.named_type
        SubsTab    = fl.stableflow.cfg.util.SubstitutionTable
        output     = fl.stableflow.cfg.data._expand_node(
                        node = fl.stableflow.cfg.data.Node(line     = 1,
                                                        col      = 2,
                                                        level    = 3,
                                                        path     = [],
                                                        name     = 'name',
                                                        spec     = 'my_param',
                                                        category = named_type),
                        subs     = SubsTab({'my_param': 'some_float_type'}),
                        typeinfo = {'some_float_type': {'py': float}},
                        idx      = 4)

        expected_output = {
            '_node_info': {
                'category':     'named_type',
                'memory_order': 'C',
                'preset':       0.0,
                'shape':        None,
                'src_line':     1,
                'src_col':      2,
                'src_level':    3,
                'src_path':     ['name'],
                'src_seqnum':   4,
                'typeinfo': {
                    'py': float
                }
            }
        }

        assert output == expected_output
