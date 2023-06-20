# -*- coding: utf-8 -*-
"""
Process level controller component.

"""


import datetime
import time

import pl.stableflow.signal


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the controller.

    """

    # Grab a reference to the list of exceptions.
    #
    state['list_signal'] = runtime['proc']['list_signal']

    # Store queues for backlog logging.
    #
    state['map_queue'] = dict()
    for node in runtime['proc']['list_node']:
        for (key, queue) in node.input_queues.items():
            tup_path = (node.id_node, 'inputs') + key
            state['map_queue']['.'.join(tup_path)] = queue
        for (key, queue) in node.output_queues.items():
            tup_path = (node.id_node, 'outputs') + key
            state['map_queue']['.'.join(tup_path)] = queue

    tup_key_out      = set(outputs.keys())
    tup_key_ctrl_out = tup_key_out - set(('feedback',))
    state['tup_key_ctrl_out'] = tup_key_ctrl_out

    # Reset control output(s).
    #
    for key_ctrl_out in tup_key_ctrl_out:
        outputs[key_ctrl_out].clear()
        outputs[key_ctrl_out]['ena'] = False

    # Reset feedback output.
    #
    if 'feedback' in outputs:
        outputs['feedback']['ena']         = False
        outputs['feedback']['map_load']    = dict()
        outputs['feedback']['list_signal'] = list()


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Send a message once per period.

    """

    # Reset control and feedback outputs.
    #
    for key_ctrl_out in state['tup_key_ctrl_out']:
        outputs[key_ctrl_out]['ena'] = False

    if 'feedback' in outputs:
        outputs['feedback']['ena'] = False
        outputs['feedback']['map_load'].clear()
        outputs['feedback']['list_ex'].clear()

    if not inputs['ctrl']['ena']:
        return

    # Set feedback outputs
    #
    if 'feedback' in outputs:

        if state['list_ex']:

            outputs['feedback']['ena'] = True
            outputs['feedback']['list_ex'].extend(state['list_ex'])

        for (key, queue) in state['map_queue'].items():
            outputs['feedback']['ena'] = True
            outputs['feedback']['map_load'][key] = queue.approx_size()

    # Set control outputs
    #
    for key_ctrl_out in state['tup_key_ctrl_out']:
        outputs[key_ctrl_out].clear()
        outputs[key_ctrl_out].update(inputs['ctrl'])

    if inputs['ctrl']['do_halt']:
        return (pl.stableflow.signal.exit_ok_controlled,)
