# -*- coding: utf-8 -*-
"""
Functional specification for the pl.stableflow.test.util module.

"""


# =============================================================================
class SpecifySimplePipeline:
    """
    Spec for the simple_pipeline function.

    """

    # -------------------------------------------------------------------------
    def it_returns_valid_configuration(self):
        """
        simple_pipeline returns a valid configuration dict.

        """

        import pl.stableflow.test.util
        import fl.stableflow.cfg.validate
        cfg = pl.stableflow.test.util.simple_pipeline(
                            repr           = 'py_dill',
                            iface          = 'step',
                            is_closed_loop = False,
                            proc_a         = {'node_a': simple_counter,
                                              'node_b': simple_messager})
        fl.stableflow.cfg.validate.normalized(cfg)


# -----------------------------------------------------------------------------
def simple_counter(inputs, state, outputs):  # pylint: disable=W0613
    """
    Step function for a simple test node that counts to ten.

    """

    if 'count' not in state:
        state['count'] = 0
    else:
        state['count'] += 1
    outputs['output']['count'] = state['count']
    if state['count'] >= 10:
        import pl.stableflow.exception  # pylint: disable=C0415
        return pl.stableflow.exception.GracefulHalt(0)


# -----------------------------------------------------------------------------
def simple_messager(inputs, state, outputs):  # pylint: disable=W0613
    """
    Step function for a test node that prints a message after ten steps.

    """

    import pl.stableflow.test.util

    if inputs['input']['count'] >= 10:
        pl.stableflow.test.util.send(message = 'TEST OK')
        import pl.stableflow.exception  # pylint: disable=C0415
        raise pl.stableflow.exception.GracefulHalt(0)
