# -*- coding: utf-8 -*-
"""
---

title:
    "Utility I/O functions module."

description:
    "This module contains various bits of
    general purpose I/O utility functionality."

id:
    "ecc24c2b-7ee9-4e25-a83a-a4931754d465"

type:
    dt003_python_module

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


import glob
import os.path


# -----------------------------------------------------------------------------
def load_from_dirpath(dirpath):
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
        cfg = _apply_override(cfg,
                              section_address,
                              load_from_filepath(filepath_cfg),
                              delim_cfg_addr = '.')
    return cfg


# -----------------------------------------------------------------------------
def _apply_override(data, address, value, delim_cfg_addr = '.'):
    """
    Apply a single configuration field override on the specified path.

    """
    addr_parts = address.split(delim_cfg_addr)
    subtree    = data

    for key in addr_parts[:-1]:
        if key not in subtree:
            subtree[key] = dict()
        subtree = subtree[key]
    key = addr_parts[-1]
    subtree[key] = value
    return data


# -----------------------------------------------------------------------------
def save_to_filepath(map_data, filepath, str_format = None):
    """
    Write the specified dict to the specified file in the specified format.

    """

    if str_format is None:
        (_, str_ext) = os.path.splitext(filepath)
        str_format   = str_ext[1:]

    if str_format == 'pickle':
        filemode = 'wb'
    else:
        filemode = 'wt'

    (serial_data, map_error) = serialize(map_data, str_format)

    if serial_data is not None:
        with open(filepath, filemode) as file:
            file.write(serial_data)

    return map_error


# -----------------------------------------------------------------------------
def load_from_filepath(filepath, str_format = None):
    """
    Return data loaded from the specified file as a dict.

    """

    if str_format is None:
        (_, str_ext) = os.path.splitext(filepath)
        str_format   = str_ext[1:]

    if str_format in ('pkl', 'pickle'):
        filemode = 'rb'
    else:
        filemode = 'rt'

    with open(filepath, filemode) as file:
        serial_data = file.read()

    (map_data, map_error) = deserialize(serial_data, str_format)

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize(map_data, str_format):
    """
    Return the specified data as a serialised string in the specified format.

    """

    lut = dict(pickle = serialize_to_pickle_bytes,
               pkl    = serialize_to_pickle_bytes,
               xml    = serialize_to_xml_string,
               json   = serialize_to_json_string,
               toml   = serialize_to_toml_string,
               yaml   = serialize_to_yaml_string,
               yml    = serialize_to_yaml_string)
    return lut[str_format](map_data)


# -----------------------------------------------------------------------------
def deserialize(str_data, str_format):
    """
    Return the data encoded in the the specified string as a dict.

    """

    lut = dict(pickle = deserialize_from_pickle_bytes,
               pkl    = deserialize_from_pickle_bytes,
               xml    = deserialize_from_xml_string,
               json   = deserialize_from_json_string,
               toml   = deserialize_from_toml_string,
               yaml   = deserialize_from_yaml_string,
               yml    = deserialize_from_yaml_string)
    return lut[str_format](str_data)


# -----------------------------------------------------------------------------
def serialize_to_pickle_bytes(map_data):
    """
    Return the specified data as pickled bytes.

    """

    import pickle # pylint: disable=C0415

    bytes_pickle = None
    map_error    = None

    try:

        bytes_pickle = pickle.dumps(obj             = map_data,
                                    protocol        = pickle.DEFAULT_PROTOCOL,
                                    fix_imports     = False,
                                    buffer_callback = None)

    except pickle.PicklingError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    return (bytes_pickle, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_pickle_bytes(bytes_pickle):
    """
    Return the data encoded in the the specified pickled bytes as a dict.

    """

    import pickle # pylint: disable=C0415

    map_data  = None
    map_error = None

    try:

        map_data = pickle.loads(bytes_pickle,
                                fix_imports = False)

    except pickle.UnpicklingError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    return (map_data, map_error)



# -----------------------------------------------------------------------------
def serialize_to_xml_string(map_data):
    """
    Return the specified data as an XML string.

    """

    import xmltodict # pylint: disable=C0415

    str_xml   = None
    map_error = None

    if len(map_data) > 1:
        map_data = dict(root = map_data)

    try:

        str_xml = xmltodict.unparse(input_dict = map_data,
                                    encoding = 'utf-8',
                                    pretty     = True,
                                    newl       = '\n'.format(),
                                    indent     = '  ')

    except TypeError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_xml = str_xml.strip()

    return (str_xml, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_xml_string(str_xml, xml_attribs = False):
    """
    Return the data encoded in the the specified XML string as a dict.

    """

    import xmltodict          # pylint: disable=C0415
    import xml.parsers.expat  # pylint: disable=C0415

    map_data  = None
    map_error = None

    str_xml = str_xml.strip()

    # -------------------------------------------------------------------------
    def _postproc(path, key, value):
        """
        """
        tup_ctor_type = (int, float)
        for ctor_type in tup_ctor_type:
            try:
                value = ctor_type(value)
            except (ValueError, TypeError):
                continue
            else:
                break
        return (key, value)

    try:

        map_data = xmltodict.parse(str_xml,
                                   encoding      = 'utf-8',
                                   xml_attribs   = xml_attribs,
                                   postprocessor = _postproc)

    except xml.parsers.expat.ExpatError as err:

        map_error = dict(exception = err,
                         message   = str(err),
                         idx_line  = err.lineno - 1,
                         idx_col   = err.offset)

    else:

        if tuple(map_data.keys()) == ('root',):
            map_data = map_data['root']

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize_to_json_string(map_data):
    """
    Return the specified data as a JSON string.

    """

    import json  # pylint: disable=C0415

    str_json  = None
    map_error = None

    try:

        str_json = json.dumps(map_data, indent = 2)

    except TypeError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_json = str_json.strip()

    return (str_json, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_json_string(str_json):
    """
    Return the data encoded in the the specified JSON string.

    """

    import json  # pylint: disable=C0415

    map_data  = None
    map_error = None

    # Remove comment lines.
    #
    list_str_line = []
    for str_line in str_json.strip().splitlines():
        str_line_naked = str_line.strip()
        if str_line_naked.startswith('//') or str_line_naked.startswith('#'):
            continue
        list_str_line.append(str_line)
    str_json = ''.join(list_str_line)

    try:

        map_data = json.loads(str_json)

    except json.JSONDecodeError as err:

        map_error = dict(exception      = err,
                         message        = str(err),
                         idx_char_start = err.pos)

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize_to_toml_string(map_data):
    """
    Return the specified data as a TOML string.

    """

    import toml  # pylint: disable=C0415

    str_toml  = None
    map_error = None

    try:

        str_toml = toml.dumps(map_data)

    except TypeError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_toml = str_toml.strip()

    return (str_toml, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_toml_string(str_toml):
    """
    Return the data encoded in the specified TOML string.

    """

    import toml  # pylint: disable=C0415

    map_data  = None
    map_error = None

    str_toml  = str_toml.strip()

    try:

        map_data = toml.loads(str_toml)

    except toml.TomlDecodeError as err:

        map_error = dict(exception      = err,
                         message        = err.msg,
                         idx_char_start = err.pos,
                         idx_line       = err.lineno - 1,
                         idx_col        = err.colno)

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize_to_yaml_string(map_data):
    """
    Return the specified data as a YAML string.

    """

    import yaml  # pylint: disable=C0415

    str_yaml  = None
    map_error = None

    try:

        str_yaml = yaml.dump(map_data, default_flow_style = False)

    except yaml.YAMLError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_yaml = str_yaml.strip()
        #str_yaml = _reindent_yaml(str_yaml)

    return (str_yaml, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_yaml_string(str_yaml):
    """
    Return the data encoded in the specified YAML string.

    """

    import yaml  # pylint: disable=C0415

    map_data  = None
    map_error = None

    loader = yaml.SafeLoader
    yaml.add_constructor('!regex',
                         lambda l, n: str(n.value),
                         Loader = loader)

    str_yaml = str_yaml.strip()

    try:

        map_data = yaml.load(str_yaml, Loader = loader)

    except yaml.YAMLError as err:

        map_error = dict(exception = err,
                         message   = str(err))

        if hasattr(err, 'problem_mark'):
            mark = err.problem_mark
            map_error['idx_line'] = mark.line
            map_error['idx_col']  = mark.column

    return (map_data, map_error)


