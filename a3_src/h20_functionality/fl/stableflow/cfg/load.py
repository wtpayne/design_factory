# -*- coding: utf-8 -*-
"""
Module of functions for reading saved configuration data in various formats.

---
type:
    python_extension

name_extension:
    fl.stableflow.cfg.load
...

"""


import glob
import os.path

import fl.stableflow.cfg.util

from fl.stableflow.cfg.exception import CfgError


# -----------------------------------------------------------------------------
def from_path(path_cfg):
    """
    Return configuration loaded from the specified path.

    """
    if path_cfg is None:
        return dict()

    if os.path.isdir(path_cfg):
        return from_dirpath(dirpath_cfg = path_cfg)

    if os.path.isfile(path_cfg):
        return from_filepath(path_cfg)

    raise CfgError(
            'The specified configuration path does not exist: ' + path_cfg)


# -----------------------------------------------------------------------------
def from_dirpath(dirpath_cfg):
    """
    Return configuration loaded from the specified directory path.

    Files with the shortest filenames are loaded
    first. These files correspond to branches
    rooted close to the overall root of the
    configuration tree.

    Files with the longest filenames are loaded
    last, overriding any previously loaded values.
    These files correspond to the narrowest, most
    specific branches and leaves of the
    configuration tree.

    In this way, files containing configuration
    which is more specific and narrower in scope
    overrides the configuration loaded earlier
    on in the process, from files which are
    broader in scope and less specific.

    """
    suffix        = '.cfg.*'
    glob_expr     = dirpath_cfg + os.sep + '*' + suffix
    glob_result   = glob.glob(glob_expr)
    list_fileinfo = []
    for filepath_cfg in glob_result:
        filepath_parts  = os.path.split(filepath_cfg)
        filename        = filepath_parts[-1]
        filename_parts  = filename.split('.')
        filename_prefix = '.'.join(filename_parts[:-2])
        section_address = filename_prefix
        if section_address == 'root':
            sort_key = 0
        else:
            sort_key = len(section_address)
        list_fileinfo.append((sort_key, filepath_cfg, section_address))

    cfg = dict()
    for (_, filepath_cfg, section_address) in sorted(list_fileinfo):
        cfg = fl.stableflow.cfg.util.apply(cfg,
                                  section_address,
                                  from_filepath(filepath_cfg),
                                  delim_cfg_addr = '.')
    return cfg


# -----------------------------------------------------------------------------
def from_filepath(filepath_cfg):
    """
    Return confiuguration data loaded from the specified file path.

    """
    map_reader = {
        '.xml':  _from_xml_file,
        '.json': _from_json_file,
        '.yaml': _from_yaml_file,
        '.toml': _from_toml_file,
    }
    for (str_ext, fcn_reader) in map_reader.items():
        if filepath_cfg.endswith(str_ext):
            with open(filepath_cfg) as file_cfg:
                return fcn_reader(filepath_cfg, file_cfg)
    raise CfgError('Did not recognize filename extension.')


# -----------------------------------------------------------------------------
def _from_xml_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified XML file path.

    """
    import xmltodict  # pylint: disable=C0415
    cfg = xmltodict.parse(file_cfg.read())
    if tuple(cfg.keys()) == ('root',):
        cfg = cfg['root']
    return cfg


# -----------------------------------------------------------------------------
def _from_json_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified JSON file path.

    """
    import json  # pylint: disable=C0415
    list_str_line = []
    for str_line in file_cfg:
        str_line_naked = str_line.strip()
        if str_line_naked.startswith('//') or str_line_naked.startswith('#'):
            continue
        list_str_line.append(str_line)
    return json.loads(''.join(list_str_line))


# -----------------------------------------------------------------------------
def _from_yaml_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified YAML file path.

    """
    return from_yaml_string(str_yaml     = file_cfg.read(),
                            filepath_cfg = filepath_cfg)


# -----------------------------------------------------------------------------
def from_yaml_string(str_yaml, filepath_cfg = 'memory'):
    """
    Return confiuguration data loaded from the specified YAML format string.

    """
    try:
        import yaml  # pylint: disable=C0415
        loader = yaml.SafeLoader
        yaml.add_constructor('!regex',
                             lambda l, n: str(n.value),
                             Loader = loader)
        return yaml.load(str_yaml, Loader = loader)
    except yaml.YAMLError as err:
        if hasattr(err, 'problem_mark'):
            mark = err.problem_mark
            location = '({line}:{column})'.format(line   = mark.line   + 1,
                                                  column = mark.column + 1)
        else:
            location = ''
        raise fl.stableflow.cfg.exception.CfgError(
                'Error reading file: {path} {loc}\n\n{msg}\n'.format(
                                                        path = filepath_cfg,
                                                        loc  = location,
                                                        msg  = str(err)))


# -----------------------------------------------------------------------------
def _from_toml_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified TOML file path.

    """
    import toml  # pylint: disable=C0415
    return toml.loads(file_cfg.read())
