# -*- coding: utf-8 -*-
"""
Functional specification for fl.test.component

"""


import pytest


# =============================================================================
class SpecifyFlTestComponent:
    """
    Spec for the fl.test.component module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_test_component(self):
        """
        fl.test.component can be imported with no errors.

        """

        import fl.test.component


# =============================================================================
class SpecifyFlTestComponent_baselineConfiguration:
    """
    Spec for the _baseline_configuration function.

    """

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_baseline_configuration(self):
        """
        _baseline_configuration generates the expected configuration data.

        """

        import fl.test.component

        assert fl.test.component._baseline_configuration() == {
            'data':         { 'python_dict': 'py_dict' },
            'edge':         [],
            'host':         { 'localhost': {
                                'acct_provision':   'stableflow',
                                'acct_run':         'stableflow',
                                'hostname':         '127.0.0.1' }},
            'node':         {},
            'process':      { 'main_process':       {'host': 'localhost'}},
            'req_host_cfg': { 'test_configuration': {}},
            'system':       { 'id_system':          'stableflow_test'}}


# =============================================================================
class SpecifyFlTestComponent_pipelineConfiguration:
    """
    Spec for the pipeline_test_cfg function.

    """

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_pipeline_test_cfg(self):
        """
        pipeline_test_cfg generates the expected configuration data.

        """

        import fl.test.component

        ctrl_sys             = 'cl.ctrl.sys.ic00_edict'
        ctrl_proc            = 'cl.ctrl.proc.ic00_edict'
        signal_generator     = 'fl.test._meta.signal_generator'
        signal_validator     = 'fl.test._meta.signal_validator'
        component_under_test = 'fl.test._meta.multiply_by_two'
        cfg_output           = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules     = [component_under_test],
                list_pipeline_node_config = [{}],
                list_pipeline_edge_info   = [],
                list_test_vectors         = [{'path':    ['data'],
                                              'signal':  [1, 2, 3, 4, 5]}],
                list_expected_outputs     = [{'path':    ['data'],
                                              'signal':  [2, 4, 6, 8, 10]}])

        cfg_expected = {

            'system': {
                'id_system':            'stableflow_test'},

            'host': {
                'localhost':            {'acct_provision':  'stableflow',
                                         'acct_run':        'stableflow',
                                         'hostname':        '127.0.0.1'}},

            'process': {
                'main_process':         {'host':            'localhost'}},

            'node': {
                'ctrl_sys': {
                    'config':           {'idx_max': 2},
                    'functionality':    {'py_module':    ctrl_sys},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'ctrl_proc': {
                    'config':           {},
                    'functionality':    {'py_module':    ctrl_proc},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'signal_generator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [1, 2, 3, 4, 5]}]},
                    'functionality':    {'py_module':   signal_generator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'pipeline_node_000': {
                    'config':           {},
                    'functionality':    {'py_module':   component_under_test},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'output_evaluator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [2, 4, 6, 8, 10]}]},
                    'functionality':    {'py_module':   signal_validator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'}},

            'edge': [
                {'owner':   'ctrl_sys',
                 'src':     'ctrl_sys.outputs.ctrl',
                 'dst':     'ctrl_proc.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'ctrl_proc',
                 'src':     'ctrl_proc.outputs.ctrl_000',
                 'dst':     'output_evaluator.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'ctrl_proc',
                 'src':     'ctrl_proc.outputs.ctrl_001',
                 'dst':     'pipeline_node_000.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'ctrl_proc',
                 'src':     'ctrl_proc.outputs.ctrl_002',
                 'dst':     'signal_generator.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'signal_generator',
                 'src':     'signal_generator.outputs.data',
                 'dst':     'pipeline_node_000.inputs.data',
                 'data':    'python_dict'},
                {'owner':   'pipeline_node_000',
                 'src':     'pipeline_node_000.outputs.data',
                 'dst':     'output_evaluator.inputs.data',
                 'data':    'python_dict'}],

            'data': {
                'python_dict': 'py_dict'},

            'req_host_cfg': {
                'test_configuration': {}}}

        assert cfg_output['system']       == cfg_expected['system']
        assert cfg_output['host']         == cfg_expected['host']
        assert cfg_output['process']      == cfg_expected['process']
        assert cfg_output['node']         == cfg_expected['node']
        assert cfg_output['data']         == cfg_expected['data']
        assert cfg_output['req_host_cfg'] == cfg_expected['req_host_cfg']

        for cfg_edge in cfg_output['edge']:
            assert cfg_edge in cfg_expected['edge']

        for cfg_edge in cfg_expected['edge']:
            assert cfg_edge in cfg_output['edge']

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_functional_configuration(self):
        """
        functional_configuration generates the expected configuration data.

        """

        import fl.test.component

        ctrl_sys             = 'cl.ctrl.sys.ic00_edict'
        ctrl_proc            = 'cl.ctrl.proc.ic00_edict'
        signal_generator     = 'fl.test._meta.signal_generator'
        signal_validator     = 'fl.test._meta.signal_validator'
        component_under_test = 'fl.test._meta.multiply_by_two'
        cfg_output           = fl.test.component.functional_test_cfg(
                                    module = component_under_test,
                                    config = dict(),
                                    script = [{'in':  { 'data':  1 },
                                               'out': { 'data':  2 }},
                                              {'in':  { 'data':  2 },
                                               'out': { 'data':  4 }},
                                              {'in':  { 'data':  3 },
                                               'out': { 'data':  6 }},
                                              {'in':  { 'data':  4 },
                                               'out': { 'data':  8 }},
                                              {'in':  { 'data':  5 },
                                               'out': { 'data': 10 }}])
        cfg_expected = {

            'system': {
                'id_system':            'stableflow_test'},

            'host': {
                'localhost':            {'acct_provision':  'stableflow',
                                         'acct_run':        'stableflow',
                                         'hostname':        '127.0.0.1'}},

            'process': {
                'main_process':         {'host':            'localhost'}},

            'node': {
                'ctrl_sys': {
                    'config':           {'idx_max': 2},
                    'functionality':    {'py_module':    ctrl_sys},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'ctrl_proc': {
                    'config':           {},
                    'functionality':    {'py_module':    ctrl_proc},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'signal_generator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [1, 2, 3, 4, 5]}]},
                    'functionality':    {'py_module':   signal_generator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'pipeline_node_000': {
                    'config':           {},
                    'functionality':    {'py_module':   component_under_test},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'output_evaluator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [2, 4, 6, 8, 10]}]},
                    'functionality':    {'py_module':   signal_validator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'}},

            'edge': [
                {'owner':   'ctrl_sys',
                 'src':     'ctrl_sys.outputs.ctrl',
                 'dst':     'ctrl_proc.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'ctrl_proc',
                 'src':     'ctrl_proc.outputs.ctrl_000',
                 'dst':     'output_evaluator.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'ctrl_proc',
                 'src':     'ctrl_proc.outputs.ctrl_001',
                 'dst':     'pipeline_node_000.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'ctrl_proc',
                 'src':     'ctrl_proc.outputs.ctrl_002',
                 'dst':     'signal_generator.inputs.ctrl',
                 'data':    'python_dict'},
                {'owner':   'signal_generator',
                 'src':     'signal_generator.outputs.data',
                 'dst':     'pipeline_node_000.inputs.data',
                 'data':    'python_dict'},
                {'owner':   'pipeline_node_000',
                 'src':     'pipeline_node_000.outputs.data',
                 'dst':     'output_evaluator.inputs.data',
                 'data':    'python_dict'}],

            'data': {
                'python_dict': 'py_dict'},

            'req_host_cfg': {
                'test_configuration': {}}}

        assert cfg_output['system']       == cfg_expected['system']
        assert cfg_output['host']         == cfg_expected['host']
        assert cfg_output['process']      == cfg_expected['process']
        assert cfg_output['data']         == cfg_expected['data']
        assert cfg_output['req_host_cfg'] == cfg_expected['req_host_cfg']

        for id_node in cfg_output['node'].keys():
            assert cfg_output['node'][id_node] == cfg_expected['node'][id_node]

        for cfg_edge in cfg_output['edge']:
            assert cfg_edge in cfg_expected['edge']

        for cfg_edge in cfg_expected['edge']:
            assert cfg_edge in cfg_output['edge']
