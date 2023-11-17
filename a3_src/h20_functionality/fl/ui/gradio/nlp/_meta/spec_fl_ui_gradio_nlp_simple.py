# -*- coding: utf-8 -*-
"""
Functional specification for fl.ui.gradio.nlp.simple

"""


import pytest


# =============================================================================
class SpecifyFlUiGradioText:
    """
    Spec for the fl.ui.gradio.nlp.simple module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_ui_gradio_text(self):
        """
        fl.ui.gradio.nlp.simple can be imported.

        """

        import fl.ui.gradio.nlp.simple
