# -*- coding: utf-8 -*-
"""
Test fixtures for fl.stableflow.cfg package functional requirements tests.

"""


import io
import json

import pytest
import yaml
import xmltodict


# -----------------------------------------------------------------------------
@pytest.fixture
def dict_of_strings():
    """
    Return a test data structure.

    Fields only have strings to accomodate the
    fact that XML handling delays parsing of
    data fields until the point at which the
    structure is validated.

    """
    return { 'some':      'sort',
             'of':        'data',
             'structure': 'with',
             'multiple':  'fields',
             'and':       'only',
             'textual':   'data' }


# -----------------------------------------------------------------------------
@pytest.fixture
def invalid_config():
    """
    Return a test data structure.

    """
    return { 'some':   'sort',
             'of':     'invalid',
             'config': 100 }


# -----------------------------------------------------------------------------
@pytest.fixture
def valid_normalized_config():
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
                'hostname':       '123.123.123.123',
                'acct_run':       'stableflow',
                'acct_provision': 'stableflow'
            }
        },
        'process': {
            'some_process': {
                'host': 'some_host'
            }
        },
        'node': {
            'some_node': {
                'process':        'some_process',
                'state_type':     'some_data_type',
                'req_host_cfg':   'some_requirement_on_host_cfg',
                'functionality': {
                    'py_module':    'some_pkg.importable.module'
                }
            }
        },
        'edge': [
            {
                'owner': 'some_node',
                'data':  'some_data_type',
                'src':   'some_node.outputs.port',
                'dst':   'some_node.inputs.port'
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
        }
    }


# -----------------------------------------------------------------------------
@pytest.fixture
def filepath_cfg_yaml(tmp_path, dict_of_strings):
    """
    Return the file path to a mock config file as a string.

    """
    return _create_cfg_file(dirpath_root = tmp_path,
                            cfg_data     = dict_of_strings,
                            ext          = 'yaml',
                            dumper       = _dump_as_yaml)


# -----------------------------------------------------------------------------
@pytest.fixture
def filepath_cfg_json(tmp_path, dict_of_strings):
    """
    Return the file path to a mock config file as a string.

    """
    return _create_cfg_file(dirpath_root = tmp_path,
                            cfg_data     = dict_of_strings,
                            ext          = 'json',
                            dumper       = _dump_as_json)


# -----------------------------------------------------------------------------
@pytest.fixture
def filepath_cfg_xml(tmp_path, dict_of_strings):
    """
    Return the file path to a mock config file as a string.

    """
    return _create_cfg_file(dirpath_root = tmp_path,
                            cfg_data     = dict_of_strings,
                            ext          = 'xml',
                            dumper       = _dump_as_xml)


# -----------------------------------------------------------------------------
@pytest.fixture
def dirpath_cfg_yaml(tmp_path, dict_of_strings):
    """
    Return the directory path of a mock config directory as a string.

    """
    return _create_cfg_dir(dirpath_root = tmp_path,
                           cfg_data     = dict_of_strings,
                           ext          = 'yaml',
                           dumper       = _dump_as_yaml)


# -----------------------------------------------------------------------------
@pytest.fixture
def dirpath_cfg_json(tmp_path, dict_of_strings):
    """
    Return the directory path of a mock config directory as a string.

    """
    return _create_cfg_dir(dirpath_root = tmp_path,
                           cfg_data     = dict_of_strings,
                           ext          = 'json',
                           dumper       = _dump_as_json)


# -----------------------------------------------------------------------------
@pytest.fixture
def dirpath_cfg_xml(tmp_path, dict_of_strings):
    """
    Return the directory path of a mock config directory as a string.

    """
    return _create_cfg_dir(dirpath_root = tmp_path,
                           cfg_data     = dict_of_strings,
                           ext          = 'xml',
                           dumper       = _dump_as_xml)


# -----------------------------------------------------------------------------
def _create_cfg_file(dirpath_root, cfg_data, ext, dumper):
    """
    Create sample configuration as a single config file.

    """
    filename     = 'test.cfg.{ext}'.format(ext = ext)
    dirpath_cfg  = dirpath_root / 'cfg'
    filepath_cfg = dirpath_cfg / filename
    dirpath_cfg.mkdir()
    filepath_cfg.write_text(dumper(cfg_data))
    return filepath_cfg.as_posix()


# -----------------------------------------------------------------------------
def _create_cfg_dir(dirpath_root, cfg_data, ext, dumper):
    """
    Create sample configuration as a directory of separate config files.

    """
    dirpath_cfg = dirpath_root / 'cfg'
    dirpath_cfg.mkdir()
    for key in cfg_data.keys():
        filename_cfg = '{key}.cfg.{ext}'.format(key = key, ext = ext)
        filepath_cfg = dirpath_cfg / filename_cfg
        filepath_cfg.write_text(dumper(cfg_data[key]))
    return dirpath_cfg.as_posix()


# -----------------------------------------------------------------------------
def _dump_as_json(data):
    """
    Serialize the specified data structure to a JSON format string.

    """
    return json.dumps(data)


# -----------------------------------------------------------------------------
def _dump_as_yaml(data):
    """
    Serialize the specified data structure to a YAML format string.

    """
    stream_cfg = io.StringIO()
    yaml.dump(data, stream_cfg)
    stream_cfg.seek(0)
    return stream_cfg.read()


# -----------------------------------------------------------------------------
def _dump_as_xml(data):
    """
    Serialize the specified data structure to a XML format string.

    """
    return xmltodict.unparse({'root': data}, pretty = True)
