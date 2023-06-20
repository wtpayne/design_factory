# -*- coding: utf-8 -*-
"""
Functional specification for cl.ui.gradio.nlp.simple.ic00_edict

"""


import inspect

import pytest

import da.env
import fl.test.component
import pl.stableflow.sys


# =============================================================================
class SpecifyClUiGradioNlpSimpleIc00_edict:
    """
    Spec for the cl.ui.gradio.nlp.simple.ic00_edict component.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        cl.net.openai.client.ic00_edict can be imported.

        """
        import cl.ui.gradio.nlp.simple.ic00_edict
