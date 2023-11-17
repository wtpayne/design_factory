# -*- coding: utf-8 -*-
"""
Functional specification for the pl.stableflow.node package.

"""

# =============================================================================
class SpecifyStableflowNode:
    """
    Spec for pl.stableflow.node package.

    """

    # -------------------------------------------------------------------------
    def it_can_be_imported(self):
        """
        pl.stableflow.node can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """

        import pl.stableflow.node
