# -*- coding: utf-8 -*-
"""
Functional specification for cl.ctrl.sys.ic00_edict.

"""

import pytest


# =============================================================================
class SpecifyClCtrlSysIc00_edict:
    """
    Spec for the cl.ctrl.sys.ic00_edict component.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        cl.ctrl.sys.ic00_edict can be imported.

        """
        import cl.ctrl.sys.ic00_edict

