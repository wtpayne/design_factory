# -*- coding: utf-8 -*-
"""
Module of functions for validating configuration data.

"""


import copy
import jsonschema

import fl.stableflow.cfg.exception
import pl.stableflow.log


# -----------------------------------------------------------------------------
def normalized(cfg):
    """
    Validate normalized config data.

    This is the config data as it appears on disk, prior to
    any denormalization and/or expansion.

    """

    return _validate_with_schema(cfg, _normalized_cfg_schema())


# -----------------------------------------------------------------------------
def denormalized(cfg):
    """
    Validate denormalized config data.

    This is the config data after it has been processed
    to make implicit information explicit.

    """

    return _validate_with_schema(cfg, _denormalized_cfg_schema())


# -----------------------------------------------------------------------------
def _validate_with_schema(cfg, schema):
    """
    Validate config using the specified schema.

    """

    try:
        jsonschema.validate(cfg, schema)
    except jsonschema.exceptions.ValidationError as err:
        msg = '\n\n{msg}\n\n'.format(msg = str(err))
        raise fl.stableflow.cfg.exception.CfgError(msg)
    _check_consistency(cfg)
    return cfg


# -----------------------------------------------------------------------------
def _normalized_cfg_schema():
    """
    Return a schema for normalized config data.

    """

    schema = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        '$id': 'http://xplain.systems/schemas/cfg_norm_v1.json',
        'definitions': {
            'numeric_string':      { 'type':    'string',
                                     'pattern': '^[0-9]*$'           },
            'hex_string':          { 'type':    'string',
                                     'pattern': '^[a-f0-9]*$'        },
            'lowercase_name':      { 'type':    'string',
                                     'pattern': '^[a-z0-9_]*$'       },
            'lowercase_dot_path':  { 'type':    'string',
                                     'pattern': '^[a-z0-9_.]*$'      },
            'list_of_strings':     { 'type': 'array',
                                     'items':   { 'type': 'string' } },
            'entry_point_obj_ref': { 'type':    'string',
                                     'pattern': '^[A-Za-z0-9_.:]*$'  },
            'id_edge':             { 'type':    'string',
                                     'pattern': '^[a-z0-9_./:]*$'    },
            'edge_direction':      { 'type':    'string',
                                     'pattern': '^feedforward|feedback$'    },
            'path_cfg':        { 'type': 'string'                           },
            'id_path':         { '$ref': '#/definitions/hex_string'         },
            'id_system':       { '$ref': '#/definitions/lowercase_name'     },
            'id_host':         { '$ref': '#/definitions/lowercase_name'     },
            'id_run':          { '$ref': '#/definitions/hex_string'         },
            'ts_run':          { '$ref': '#/definitions/numeric_string'     },
            'id_cfg':          { '$ref': '#/definitions/hex_string'         },
            'id_process':      { '$ref': '#/definitions/lowercase_name'     },
            'id_node':         { '$ref': '#/definitions/lowercase_name'     },
            'id_req_host_cfg': { '$ref': '#/definitions/lowercase_name'     },
            'id_data_type':    { '$ref': '#/definitions/lowercase_name'     },
            'ipc_type':        { '$ref': '#/definitions/lowercase_name'     },
            'path_part':       { '$ref': '#/definitions/lowercase_dot_path' },
            'spec_functionality': {
                'type': 'object',
                'properties': {
                    'py_module': {
                        '$ref': '#/definitions/entry_point_obj_ref'
                    },
                    'py_src': {
                        'type': 'object',
                        'properties': {
                            'reset': {
                                'type': 'string'
                            },
                            'step': {
                                'type': 'string'
                            }
                        }
                    }  # ,
                    # 'py_dill': {
                    #     'type': 'object',
                    #     'properties': {
                    #         'reset': {
                    #             'type': 'string'
                    #         },
                    #         'step': {
                    #             'type': 'string'
                    #         }
                    #     }
                    # }
                },
                'required': [],
            }
        },
        'type': 'object',
        'properties': {
            'system': {
                'type': 'object',
                'properties': {
                    'id_system': { '$ref': '#/definitions/id_system' } },
                'required': [ 'id_system' ],
                'additionalProperties': False
            },
            'host': {
                'type': 'object',
                'propertyNames': { 'type': 'string' },
                'additionalProperties': {
                    'type': 'object',
                    'properties': {
                        'hostname':        { 'type': 'string' },
                        'acct_run':        { 'type': 'string' },
                        'acct_provision':  { 'type': 'string' },
                        'port_range':      { 'type': 'string' },
                        'password':        { 'type': 'string' },
                        'key_filename':    { 'type': 'string' },
                        'environment':     { 'type': 'string' },
                        'launch_cmd':      { 'type': 'string' },
                        'dirpath_log':     { 'type': 'string' },
                        'log_level':       { 'type': 'string' }
                    },
                    'required': [],
                    'additionalProperties': False
                }
            },
            'process': {
                'type': 'object',
                'propertyNames': { 'type': 'string' },
                'additio7nalProperties': {
                    'type': 'object',
                    'properties': {
                        'host': { '$ref': '#/definitions/id_host' }
                    },
                    'required': [ 'host' ],
                    'additionalProperties': False
                }
            },
            'node': {
                'type': 'object',
                'propertyNames': { 'type': 'string' },
                'additionalProperties': {
                    'type': 'object',
                    'properties': {
                        'process':       { '$ref': '#/definitions/id_process'         },  # noqa pylint: disable=C0301
                        'req_host_cfg':  { '$ref': '#/definitions/id_req_host_cfg'    },  # noqa pylint: disable=C0301
                        'functionality': { '$ref': '#/definitions/spec_functionality' },  # noqa pylint: disable=C0301
                        'state_type':    { '$ref': '#/definitions/id_data_type'       },  # noqa pylint: disable=C0301
                        'config':        { 'type': 'object'                           },  # noqa pylint: disable=C0301
                        'class':         {
                            'type': 'array',
                            'items': { '$ref': '#/definitions/lowercase_name' }
                        }
                    },
                    'required': [ 'process', 'functionality' ],
                    'additionalProperties': False
                }
            },
            'edge': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'owner': { '$ref': '#/definitions/id_node'        },
                        'data':  { '$ref': '#/definitions/id_data_type'   },
                        'src':   { '$ref': '#/definitions/path_part'      },
                        'dst':   { '$ref': '#/definitions/path_part'      },
                        'dirn':  { '$ref': '#/definitions/edge_direction' }
                    },
                    'required': [
                        'owner',
                        'data',
                        'src',
                        'dst'
                    ],
                    'additionalProperties':  False
                }
            },
            'queue': {
                'type': 'object'
            },
            'req_host_cfg': {
                'type': 'object'
            },
            'roles': {
                'type': 'object'
            },
            'data': {
                'type': 'object'
            },
            'runtime': {
                'type': 'object',
                'properties': {
                    'opt':  {
                        'type': 'object',
                        'properties': {
                            'do_make_ready': { 'type': 'boolean' },
                            'is_local':      { 'type': 'boolean' }
                        },
                        'required': [
                            'do_make_ready',
                            'is_local' ],
                        'additionalProperties':  False
                    },
                    'id':  {
                        'type': 'object',
                        'properties': {
                            'path_cfg':   { '$ref': '#/definitions/path_cfg'   },  # noqa pylint: disable=C0301
                            'id_path':    { '$ref': '#/definitions/id_path'    },  # noqa pylint: disable=C0301
                            'id_system':  { '$ref': '#/definitions/id_system'  },  # noqa pylint: disable=C0301
                            'id_system':  { '$ref': '#/definitions/id_system'  },  # noqa pylint: disable=C0301
                            'id_system':  { '$ref': '#/definitions/id_system'  },  # noqa pylint: disable=C0301
                            'id_cfg':     { '$ref': '#/definitions/id_cfg'     },  # noqa pylint: disable=C0301
                            'id_host':    { '$ref': '#/definitions/id_host'    },  # noqa pylint: disable=C0301
                            'id_process': { '$ref': '#/definitions/id_process' },  # noqa pylint: disable=C0301
                            'id_node':    { '$ref': '#/definitions/id_node'    },  # noqa pylint: disable=C0301
                            'ts_run':     { '$ref': '#/definitions/ts_run'     },  # noqa pylint: disable=C0301
                            'id_run':     { '$ref': '#/definitions/id_run'     }   # noqa pylint: disable=C0301
                        },
                        'required': [
                            'id_host',
                            'id_run',
                            'ts_run',
                            'id_cfg' ],
                        'additionalProperties':  False
                    },
                    'proc': {
                        'type': 'object'
                    }
                },
                'required': [
                    'opt',
                    'id',
                    'proc' ],
                'additionalProperties':  False
            }
        },
        'required': ['system',
                     'host',
                     'process',
                     'node',
                     'edge',
                     'data']
    }
    return schema


# -----------------------------------------------------------------------------
def _denormalized_cfg_schema():
    """
    Return a schema for denormalized config data.

    """

    schema        = copy.deepcopy(_normalized_cfg_schema())
    schema['$id'] = 'http://xplain.systems/schemas/cfg_denorm_v1.json'

    _denormalize_host_section(schema)
    _denormalize_node_section(schema)
    _denormalize_edge_section(schema)
    schema['required'].append('queue')

    return schema


# -----------------------------------------------------------------------------
def _denormalize_host_section(schema):
    """
    Modify schema to add denormalized fields in the host config section.

    """

    host_schema = schema['properties']['host']['additionalProperties']
    host_schema['properties']['is_inter_host_edge_owner'] = {'type': 'boolean'}
    host_schema['required'].append('is_inter_host_edge_owner')


# -----------------------------------------------------------------------------
def _denormalize_node_section(schema):
    """
    Modify schema to add denormalized fields in the node config section.

    """

    node_schema = schema['properties']['node']['additionalProperties']
    node_schema['properties']['host'] = {'type': 'string'}
    node_schema['required'].append('host')


# -----------------------------------------------------------------------------
def _denormalize_edge_section(schema):
    """
    Modify schema to add denormalized fields in the edge config section.

    """

    edge_schema = schema['properties']['edge']['items']
    edge_props  = edge_schema['properties']

    # The edge id is used to index the queue database.
    edge_props['id_edge'] = { '$ref': '#/definitions/id_edge' }

    # The node id is used to index the node database
    edge_props['id_node_src'] = { '$ref': '#/definitions/id_node' }
    edge_props['id_node_dst'] = { '$ref': '#/definitions/id_node' }

    # Relative paths are used to set the input and output data pointers.
    edge_props['relpath_src'] = { 'type': 'array' }
    edge_props['relpath_dst'] = { 'type': 'array' }

    # The IPC type is used to determine the queue type to use for the edge.
    edge_props['ipc_type'] = { '$ref': '#/definitions/ipc_type' }

    # The edge index is used to determine the port number for remote queues.
    edge_props['idx_edge'] = { 'oneOf': [ { 'type': 'number' },
                                          { 'type': 'null'   } ]}

    # Process and host id lists control when edges should be ignored.
    edge_props['list_id_process'] = { 'type': 'array' }
    edge_props['list_id_host']    = { 'type': 'array' }

    # The host that owns the edge must serve any remote queues.
    edge_props['id_host_owner'] = { '$ref': '#/definitions/id_host' }

    # Remote queues are configured differently for sending vs. receiving.
    edge_props['id_host_src'] = { '$ref': '#/definitions/id_host' }
    edge_props['id_host_dst'] = { '$ref': '#/definitions/id_host' }

    set_required = set(edge_schema['properties'].keys()) - set(('dirn',))
    edge_schema['required'] = list(set_required)


# -----------------------------------------------------------------------------
def _check_consistency(cfg):
    """
    Raise an exception if cfg is inconsistent.

    """

    _check_process_consistency(cfg)
    _check_node_consistency(cfg)
    _check_edge_consistency(cfg)
    _check_edge_end_uniqueness(cfg)
    _check_required_host_configuration(cfg)


# -----------------------------------------------------------------------------
def _check_process_consistency(cfg):
    """
    Raise an exception if process configuration is inconsistent.

    """

    set_id_host = set(cfg['host'].keys())
    for cfg_process in cfg['process'].values():
        _check(item      = cfg_process['host'],
               set_valid = set_id_host,
               msg       = 'Unkown id_host in cfg: {id}')


# -----------------------------------------------------------------------------
def _check_node_consistency(cfg):
    """
    Raise an exception if node configuration is inconsistent.

    """

    set_id_process      = set(cfg['process'].keys())
    set_id_data         = set(cfg['data'].keys())
    set_id_req_host_cfg = set(cfg['req_host_cfg'].keys()) if \
                                            'req_host_cfg' in cfg else set()
    for cfg_node in cfg['node'].values():
        _check(item      = cfg_node['process'],
               set_valid = set_id_process,
               msg       = 'Unkown id_process in cfg: {id}')

        if 'state_type' in cfg_node:
            _check(item      = cfg_node['state_type'],
                   set_valid = set_id_data,
                   msg       = 'Unkown id_data in cfg: {id}')

        if 'req_host_cfg' in cfg_node:
            _check(item      = cfg_node['req_host_cfg'],
                   set_valid = set_id_req_host_cfg,
                   msg       = 'Unkown id_req_host_cfg in cfg: {id}')


# -----------------------------------------------------------------------------
def _check_edge_consistency(cfg):
    """
    Raise an exception if edge configuration is inconsistent.

    """

    set_id_node = set(cfg['node'].keys())
    set_id_data = set(cfg['data'].keys())
    for cfg_edge in cfg['edge']:

        _check(item      = cfg_edge['owner'],
               set_valid = set_id_node,
               msg       = 'Unkown id_node in cfg: {id}')

        _check(item      = cfg_edge['data'],
               set_valid = set_id_data,
               msg       = 'Unkown id_data in cfg: {id}')

        _check(item      = cfg_edge['src'].split('.')[0],
               set_valid = set_id_node,
               msg       = 'Unkown id_node in cfg: {id}')

        _check(item      = cfg_edge['dst'].split('.')[0],
               set_valid = set_id_node,
               msg       = 'Unkown id_node in cfg: {id}')

        if cfg_edge['src'].split('.')[1] != 'outputs':
            msg = 'Edge source needs to be an output.'
            raise fl.stableflow.cfg.exception.CfgError(msg)

        if cfg_edge['dst'].split('.')[1] != 'inputs':
            msg = 'Edge destination needs to be an input.'
            raise fl.stableflow.cfg.exception.CfgError(msg)


# -----------------------------------------------------------------------------
def _check_edge_end_uniqueness(cfg):
    """
    Raise an exception if edge sources or destinations are duplicated.

    """

    set_edge_path = set()
    for cfg_edge in cfg['edge']:
        if cfg_edge['src'] in set_edge_path:
            msg = 'Repeated edge source: {src}'.format(src = cfg_edge['src'])
            raise fl.stableflow.cfg.exception.CfgError(msg)
        set_edge_path.add(cfg_edge['src'])

        if cfg_edge['dst'] in set_edge_path:
            msg = 'Repeated edge destination: {dst}'.format(
                                                        dst = cfg_edge['dst'])
            raise fl.stableflow.cfg.exception.CfgError(msg)
        set_edge_path.add(cfg_edge['dst'])


# -----------------------------------------------------------------------------
def _check_required_host_configuration(cfg):
    """
    Raise an exception if req_host_cfg roles are inconsistent.

    """

    set_id_role = set(cfg['role'].keys()) if 'role' in cfg else set()
    if 'req_host_cfg' in cfg:
        for cfg_req_host_cfg in cfg['req_host_cfg'].values():
            if 'role' not in cfg_req_host_cfg:
                continue
            for id_role in cfg_req_host_cfg['role']:
                if id_role not in set_id_role:
                    msg = 'Unknown id_role in cfg: {id}'.format(id = id_role)
                    raise fl.stableflow.cfg.exception.CfgError(msg)


# -----------------------------------------------------------------------------
def _check(item, set_valid, msg):
    """
    Raise an exception if item is not in the specified collection.

    """

    if item not in set_valid:
        raise fl.stableflow.cfg.exception.CfgError(msg.format(id = item))
