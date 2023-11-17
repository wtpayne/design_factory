# -*- coding: utf-8 -*-
"""
Stableflow component for test output validation.

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

        if not isinstance(cursor, dict):
            assert cursor == expected_value
        else:

            print('#' * 80)
            import pprint
            pprint.pprint(cursor)
            print('#' * 80)

            for (key, value) in cursor.items():
                if key == 'ts':
                    continue
                assert cursor[key] == expected_value[key]
