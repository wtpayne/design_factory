# -*- coding: utf-8 -*-
"""
Stableflow component for printing data to a stream.

"""


import os.path
import pprint
import sys


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the pretty printer.

    """

    # Ensure any existing open files are closed.
    # (Ignore stdout and stderr)
    if 'stream' in state and not state['stream'].name.startswith('<std'):
        state['stream'].close()

    # Select the stream to use for output.
    state['stream'] = sys.stdout
    if 'output' in cfg:
        name_output = cfg['output']
        if name_output == 'stdout':
            state['stream'] = sys.stdout
        elif name_output == 'stderr':
            state['stream'] = sys.stderr
        else:
            filepath = name_output
            dirpath  = os.path.dirname(filepath)
            os.makedirs(dirpath, exist_ok = True)
            state['stream'] = open(filepath, 'wt')

    state['pretty'] = False
    if 'pretty' in cfg:
        state['pretty'] = cfg['pretty']


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the pretty printer.

    """

    if state['pretty']:
        pprint.pprint(inputs, stream = state['stream'])
    else:
        print(inputs, file = state['stream'])


# -----------------------------------------------------------------------------
def finalize(runtime, cfg, inputs, state, outputs):
    """
    Finalize the pretty printer.

    """

    pass
