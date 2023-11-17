# -*- coding: utf-8 -*-
"""
Functional specification for the pl.stableflow.host package.

"""

# =============================================================================
class SpecifyStableflowHost:
    """
    Spec for pl.stableflow.host package.

    """

    # -------------------------------------------------------------------------
    def it_can_be_imported(self):
        """
        pl.stableflow.host can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """

        import pl.stableflow.host
