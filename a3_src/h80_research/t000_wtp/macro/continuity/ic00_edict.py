# -*- coding: utf-8 -*-
"""
---

title:
    "Continuity process node."

description:
    "Continuity continuous process control node."

id:
    "cf5ae354-0370-48fc-93a4-e761d2c21b32"

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


import dspy


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine for continuity process node.

    """

    llm = dspy.LM(model   = "groq/llama3-8b-8192", 
                  api_key = cfg['apikey_groq'])
    dspy.configure(lm = llm)

    # module = ContinuousProcessImprovement(
    #             spec = """
    #             Translate the requirement to the SOPHIST method.
    #             """,)

    signal = None

    for key in outputs:
        outputs[key]['ena']  = False
        outputs[key]['list'] = list()

    while True:

        inputs = yield (outputs, signal)
        if not inputs['ctrl']['ena']:
            continue

        import pprint; pprint.pprint(inputs)

        for key in inputs.keys():
            if key in ('ctrl',):
                continue
            if not inputs[key]['ena']:
                continue

            # output_text = proc_ace(input_text)
            # print(output_text)

            import pprint; pprint.pprint(inputs[key])

        for key in outputs:
            outputs[key]['ena']  = False
            outputs[key]['list'].clear()


# =========================================================================
class ContinuousProcessImprovement(dspy.Module):
    """
    Continuous process improvement.

    """

    # ---------------------------------------------------------------------
    def __init__(self, spec, quantitative_rubric, qualitative_rubric):
        """
        Construct a continuous process improvement module.

        """

        self.spec                = spec
        self.quantitative_rubric = quantitative_rubric
        self.qualitative_rubric  = qualitative_rubric

        self.process_step = dspy.Predict(
            "context, spec, input -> output")

        self.quantitative_eval = dspy.Predict(
            "context, spec, input, output, rubric -> eval: float")

        self.qualitative_eval = dspy.Predict(
            "context, spec, input, output, rubric -> eval: str")

        self.determine_sentiment = dspy.Predict(
            "eval -> is_positive_sentiment: bool")

        self.make_example_worse = dspy.Predict(
            "spec, input, output, eval -> output_to_avoid")

        self.make_example_better = dspy.Predict(
            "spec, input, output, eval -> output_to_prefer")

    # ---------------------------------------------------------------------
    def forward(self, context, input):
        """
        Forward pass for the continuous process improvement module.

        """

        prediction_1 = self.process_step(
                                    context = context,
                                    spec    = self.spec,
                                    input   = input)

        prediction_2 = self.quantitative_eval(
                                    context = context,
                                    spec    = self.spec,
                                    input   = input, 
                                    output  = prediction_1.output, 
                                    rubric  = self.quantitative_rubric)

        prediction_3 = self.qualitative_eval(
                                    context = context,
                                    spec    = self.spec,
                                    input   = input, 
                                    output  = prediction_1.output, 
                                    rubric  = self.qualitative_rubric)

        quantitative_eval = prediction_2.eval
        qualitative_eval  = prediction_3.eval

        return prediction_1

