# -*- coding: utf-8 -*-
"""
---

title:
    "Macro synthetic data generation."

description:
    "Macro synthetic data generation functionality."

id:
    "05f699d3-c346-4f6d-9a2f-a2787174ba28"

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


import random
import textwrap

import dspy


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine to generate synthetic data.

    """

    llm = dspy.LM(model       = "groq/llama3-8b-8192", 
                  api_key     = cfg['apikey_groq'],
                  cache       = False,
                  temperature = 0.5)
    dspy.configure(lm = llm)

    generation_spec = textwrap.dedent("""
        Generate a random requirements specification for a light urban
        transit system, then introduce issues into the spec which might
        cause excessive energy consumption. Write out ONLY the spec with
        no introduction or commentary.""")
    gen = SyntheticDataGeneration(generation_spec = generation_spec)

    count_sample = 2

    signal = None

    for key in outputs:
        outputs[key]['ena']  = False
        outputs[key]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        for key in outputs:
            outputs[key]['ena'] = False
            outputs[key]['list'].clear()

        if not inputs['ctrl']['ena']:
            continue

        list_spec = list()
        for idx_sample in range(count_sample):
            ord_sample = idx_sample + 1
            print(f'Generating sample {ord_sample} / {count_sample}')
            list_spec.append(dict(spec = gen().output))

        for key in outputs:
            outputs[key]['ena'] = True
            outputs[key]['list'].extend(list_spec)


# =============================================================================
class SyntheticDataGeneration(dspy.Module):
    """
    Synthetic data generation DSPy module.

    """

    # -------------------------------------------------------------------------
    def __init__(self, generation_spec):
        """
        Construct a synthetic data generation module.

        """

        self.generation_spec = generation_spec
        self.generate_step   = dspy.Predict("generation_spec -> output")

    # ---------------------------------------------------------------------
    def forward(self):
        """
        Forward pass for the synthetic data generation module.

        """

        return self.generate_step(generation_spec = self.generation_spec)
