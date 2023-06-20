# -*- coding: utf-8 -*-
"""
Test fixtures for fl.stableflow.cfg.data package functional requirements tests.

"""


import pytest


# -----------------------------------------------------------------------------
@pytest.fixture
def valid_partly_denormalized_config():
    """
    Return a test data structure.

    Fields only have strings to accomodate the
    fact that XML handling delays parsing of
    data fields until the point at which the
    structure is validated.

    """
    return {
        'system':  {
            'id_system': 'some_system'
        },
        'host': {
            'some_host': {
                'hostname':                 '123.123.123.123',
                'acct_run':                 'stableflow',
                'acct_provision':           'stableflow',
                'is_inter_host_edge_owner': True
            }
        },
        'process': {
            'some_process': {
                'host': 'some_host'
            }
        },
        'node': {
            'some_node': {
                'host':           'some_host',
                'process':        'some_process',
                'state_type':     'some_data_type',
                'req_host_cfg':   'some_requirement_on_host_cfg',
                'functionality':  {
                    'py_module':    'some.importable.module'
                }
            }
        },
        'edge': [
            {
                'owner':        'some_node',
                'data':         'some_data_type',
                'src':          'some_node.outputs.port',
                'dst':          'some_node.inputs.port',
                'id_edge':      'some_node.outputs.port:some_node.inputs.port',
                'relpath_src':  ['some_node', 'outputs', 'port'],
                'relpath_dst':  ['some_node', 'inputs', 'port'],
                'id_node_src':  'some_node',
                'id_node_dst':  'some_node',
                'list_id_process': ['some_process'],
                'list_id_host': ['some_host'],
                'ipc_type':     'some_ipc_type',
                'id_host_owner':'some_host',
                'id_host_src':  'some_host',
                'id_host_dst':  'some_host',
                'idx_edge':     0,
            }
        ],
        'req_host_cfg': {
            'some_requirement_on_host_cfg': {
                'role': ['some_role']
            }
        },
        'role': {
            'some_role': {
                'some_ansible_role_structure'
            }
        },
        'data': {
            'some_data_type':  [
                {
                    'some_field_name': []
                }
            ],
            'some_type_alias': 'py_dict'
        },
        'queue': {

        }
    }
