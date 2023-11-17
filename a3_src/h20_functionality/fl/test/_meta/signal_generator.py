# -*- coding: utf-8 -*-
"""
Stableflow component for test vector generation.

"""


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the signal generator.

    """

    state['channels'] = cfg['channels']
    for channel in state['channels']:
        channel['num_samples'] = len(channel['signal'])


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the signal generator.

    """

    for channel in state['channels']:
        offset = inputs['ctrl']['ts']['idx'] % channel['num_samples']
        sample_value = channel['signal'][offset]

        path   = channel['path']
        cursor = outputs
        for name in path[:-1]:
            if name in cursor and isinstance(cursor[name], dict):
                pass
                # cursor[name].clear()
            else:
                cursor[name] = dict()
            cursor = cursor[name]

        if len(path) == 1:
            cursor[path[-1]].update(sample_value)
        else:
            cursor[path[-1]] = sample_value
