# -*- coding: utf-8 -*-
"""
Functional specification for cl.net.openai.template.ic00_edict

"""


import inspect
import logging

import pytest

import da.env
import fl.test.component
import pl.stableflow.sys


# =============================================================================
class SpecifyClNetOpenAiClientIc00_edict:
    """
    Spec for the cl.net.openai.template.ic00_edict component.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    @pytest.mark.e003_discord
    def it_supports_import_of_cl_net_openai_client_e00_edict(self):
        """
        cl.net.openai.template.ic00_edict can be imported.

        """

        import cl.net.openai.template.ic00_edict

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    @pytest.mark.e003_discord
    def it_supports_creation_of_the_main_coroutine(self):
        """
        cl.net.openai.template.ic00_edict:coro() can be created.

        """

        import cl.net.openai.template.ic00_edict

        component = cl.net.openai.template.ic00_edict.coro(
                                    runtime = None,
                                    cfg     = {},
                                    inputs  = dict(),
                                    state   = dict(),
                                    outputs = dict())

        assert inspect.isgenerator(component)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    @pytest.mark.e003_discord
    def it_runs(self):
        """
        cl.net.openai.template.ic00_edict:coro() rybs.

        """

        id_endpoint    = 'chat_completions'
        uid_workflow   = 'e6150ce3-8ebc-4553-9a9a-b1ebdc038f7e'
        uid_template   = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
        uid_variant    = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
        uid_params     = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
        id_model       = 'gpt-3.5-turbo-0301'
        messages_test  = [{'role':    'system',
                           'content': 'chat_completions_test_msg_content'}]
        filepath_env   = da.env.path(
                              process_area  = 'a3_src',
                              control_tier  = 'h10_resource',
                              relpath       = 'key/default.env')
        cfg_client     = dict(filepath_env  = filepath_env,
                              envvar_key    = 'APIKEY_OPENAI',
                              secs_interval = 0.001,
                              is_bit        = True,  # Built-in-test.
                              is_async      = False, # Asynchronous.
                              default       = dict(id_endpoint = id_endpoint,
                                                   model       = id_model),
                              id_system     = 'test',
                              id_node       = 'openai-client',
                              level_log     = logging.INFO)
        type_template  = dict(id            = 'prompt_template',
                              ver           = '1.0')
        template_valid = dict(id_endpoint   = id_endpoint,
                              type          = type_template,
                              uid_variant   = uid_variant,  # Improvement.
                              uid_template  = uid_template, # Process step.
                              uid_workflow  = uid_workflow, # Process id.
                              kwargs_req    = {'model': id_model},
                              messages      = messages_test )
        type_param     = dict(id            = 'prompt_params',
                              ver           = '1.0')
        param_valid    = dict(type          = type_param,
                              uid_params    = uid_params,
                              uid_template  = uid_template,
                              uid_workflow  = uid_workflow,
                              kwargs_tmpl   = dict(), # <-- Args for template.
                              kwargs_req    = dict(), # <-- Args for request.
                              state         = dict()) # <-- Process state.
        message_valid  = dict(role          = 'assistant',
                              content       = '\n\nTest')
        choices_valid  = dict(finish_reason = 'stop',
                              index         = 0,
                              message       = message_valid)
        response_valid = dict(choices       = [choices_valid],
                              created       = 1677858242,
                              id            = 'chatcmpl-abc123',
                              model         = id_model,
                              object        = 'chat.completion',
                              usage         = {'completion_tokens': 20,
                                               'prompt_tokens':     10,
                                               'total_tokens':      30})
        result_valid   = dict(type          = 'openai_result',
                              error         = None,
                              request       = {'messages': messages_test,
                                               'model':    id_model},
                              response      =  response_valid,
                              state         = {})

        edict_input_ena     = dict(ena  = True,
                                   ts   = dict(),
                                   list = [template_valid, param_valid])
        edict_input_none    = dict(ena  = False,
                                   ts   = dict(),
                                   list = list())

        edict_output_ena    = dict(ena  = True,
                                   ts   = dict(),
                                   list = [result_valid])
        edict_output_none   = dict(ena  = False,
                                   ts   = dict(),
                                   list = list())


        cfg_sys = fl.test.component.functional_test_cfg(
                  module = 'cl.net.openai.template.ic00_edict',
                  config = cfg_client,
                  script = [{'in':  { 'to_api':   edict_input_ena   },
                             'out': { 'from_api': edict_output_ena  }},
                            {'in':  { 'to_api':   edict_input_none  },
                             'out': { 'from_api': edict_output_none }}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg_sys,
                                                     is_local = True)

        assert exit_code == 0
