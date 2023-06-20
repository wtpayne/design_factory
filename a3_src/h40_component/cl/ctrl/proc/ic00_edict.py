# -*- coding: utf-8 -*-
"""
---

title:
    "Process controller stableflow-edict component."

description:
    "Process level controller component."

id:
    "0f6302ae-1b80-4eaf-bb56-2d0510212473"

type:
    dt004_python_stableflow_edict_component

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""


import datetime
import signal
import time

import pl.stableflow.signal


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the process controller state.

    """
    # Grab a reference to the list of application-level signals.
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
    Update output control and feedback messages.

    This component is intended to forward
    control messages from the system controller
    to all control message consumers in
    the current process.

    It is also intended to send a feedback
    message back to the system controller
    with information about queue loads and
    exceptions raised in the current process
    so that degraded mode flags for the
    entire system may be set as appropriate.

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
