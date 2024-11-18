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


import contextlib
import os
import hashlib
import random
import textwrap

import dspy
import sqlitedict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Synthetic data generation coroutine.

    This stableflow component generates synthetic
    data samples.

    """

    dspy.configure(lm = dspy.LM(model       = cfg['id_model'], 
                                api_key     = cfg['apikey_model'],
                                cache       = False,
                                temperature = cfg['temperature']))
    generation_spec = textwrap.dedent("""
        Generate a random requirements specification for a light urban
        transit system, then introduce issues into the spec which might
        cause excessive energy consumption. Write out ONLY the spec with
        no introduction or commentary.""")
    module = SyntheticDataGeneration(generation_spec = generation_spec)

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

        # Generate a list of predictions of type
        # dspy.primitives.Prediction.
        # 
        with _cache_context(filepath_cache = cfg['filepath_cache']) as cache:
            list_prediction = list()
            for idx_sample in range(cfg['count_sample']):

                # TODO: ALLOW RANDOM SAMPLING TO 
                #       CONTROL THE DISTRIBUTION
                #       OF THE SYNTHETIC DATA.
                # 
                args      = tuple()
                kwargs    = dict()

                idx_step  = inputs['ctrl']['ts']['idx']
                str_id    = '{sample}-{step}-{arg}-{kwarg}'.format(
                                                        sample = idx_sample,
                                                        step   = idx_step,
                                                        arg    = repr(args),
                                                        kwarg  = repr(kwargs))
                key_cache = hashlib.sha256(str_id.encode()).hexdigest()
                try:
                    prediction = cache[key_cache]
                except KeyError:
                    prediction = module.forward(*args, **kwargs)
                    cache[key_cache] = prediction.toDict()
                list_prediction.append(prediction)

            # Outputs.
            # 
            for key in outputs:
                outputs[key]['ena'] = True
                outputs[key]['list'].extend(list_prediction)


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _cache_context(filepath_cache):
    """
    Return an instance of the sqlitedict cache database.

    """

    dirpath_cache = os.path.dirname(filepath_cache)
    if not os.path.isdir(dirpath_cache):
        os.makedirs(dirpath_cache, exist_ok = True)
    cache = sqlitedict.SqliteDict(filepath_cache)
    yield cache
    cache.commit()
    cache.close()


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
