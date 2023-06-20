# -*- coding: utf-8 -*-
"""
Test component
"""


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Simple multiply-by-two component

    """

    signal = None
    for id_out in outputs.keys():
        outputs[id_out] = None

    while True:

        inputs = yield (outputs, signal)

        for id_out in outputs.keys():
            outputs[id_out] = None

        value = None
        for id_in in inputs.keys():
            value = inputs[id_in] * 2
            break

        for id_out in outputs.keys():
            outputs[id_out] = value