# -*- coding: utf-8 -*-
"""
Functional specification for cl.ctrl.proc.ic00_edict.

"""

import pytest


# =============================================================================
class SpecifyClCtrlProcIc00_edict:
    """
    Spec for the cl.ctrl.proc.ic00_edict component.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        cl.ctrl.proc.ic00_edict can be imported.

        """
        import cl.ctrl.proc.ic00_edict

