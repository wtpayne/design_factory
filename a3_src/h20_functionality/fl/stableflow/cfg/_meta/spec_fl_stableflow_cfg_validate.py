# -*- coding: utf-8 -*-
"""
Functional specification for the fl.stableflow.cfg.validate module.

"""


import pytest


# =============================================================================
class SpecifyNormalized:
    """
    Spec for the normalized validation function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_accepts_valid_data(self, valid_normalized_config):
        """
        Check normalized does not throw when given valid data.

        """
        import fl.stableflow.cfg.validate  # pylint: disable=C0415

        fl.stableflow.cfg.validate.normalized(valid_normalized_config)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_rejects_invalid_data(self, invalid_config):
        """
        Check normalized raises an exception when given invalid data.

        """
        import fl.stableflow.cfg.exception  # pylint: disable=C0415
        import fl.stableflow.cfg.validate   # pylint: disable=C0415

        with pytest.raises(fl.stableflow.cfg.exception.CfgError):
            fl.stableflow.cfg.validate.normalized(invalid_config)


# =============================================================================
class SpecifyDenormalized:
    """
    Spec for the denormalized validation function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_accepts_valid_data(self, valid_normalized_config):
        """
        Check normalized does not throw when given valid data.

        """
        import fl.stableflow.cfg           # pylint: disable=C0415
        import fl.stableflow.cfg.validate  # pylint: disable=C0415

        valid_denormalized_config = fl.stableflow.cfg.denormalize(
                                                    valid_normalized_config)
        fl.stableflow.cfg.validate.denormalized(valid_denormalized_config)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_rejects_invalid_data(self, invalid_config):
        """
        Check normalized raises an exception when given invalid data.

        """
        import fl.stableflow.cfg.exception  # pylint: disable=C0415
        import fl.stableflow.cfg.validate   # pylint: disable=C0415

        with pytest.raises(fl.stableflow.cfg.exception.CfgError):
            fl.stableflow.cfg.validate.denormalized(invalid_config)
