# -*- coding: utf-8 -*-
"""
Xact component for test output validation.

"""


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the signal validator.

    """
    state['channels'] = cfg['channels']
    for channel in state['channels']:
        channel['num_samples'] = len(channel['signal'])


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the signal validator.

    """
    for channel in state['channels']:

        offset = inputs['ctrl']['ts']['idx'] % channel['num_samples']
        expected_value = channel['signal'][offset]

        cursor = inputs
        for name in channel['path']:
            cursor = cursor[name]

        assert cursor == expected_value
