# -*- coding: utf-8 -*-
"""
Module of functions for serializing and deserializing configuration data.

"""


import base64
import hashlib
import zlib

import yaml


# -----------------------------------------------------------------------------
def hexdigest(data):
    """
    Return a string hash of the specified data.

    """
    if isinstance(data, bytes):
        bytes_buffer = data
    elif isinstance(data, str):
        bytes_buffer = data.encode('utf-8')
    else:
        bytes_buffer = yaml.dump(data).encode('utf-8')
    return hashlib.sha512(bytes_buffer).hexdigest()


# -----------------------------------------------------------------------------
def serialize(data):
    """
    Return a string representation of the specified config data.

    TODO: 1. Find a secure way to do key sharing across hosts.
          2. Encrypt the configuration data.
          3. Check the integrity of the configuration data.

    """
    string_yaml_encoded = yaml.dump(data)
    bytes_yaml_encoded  = string_yaml_encoded.encode('utf-8')
    bytes_zipped        = zlib.compress(bytes_yaml_encoded, 9)
    bytes_b64_encoded   = base64.b64encode(bytes_zipped)
    string_b64_encoded  = bytes_b64_encoded.decode('utf-8')
    return string_b64_encoded


# -----------------------------------------------------------------------------
def deserialize(codestring):
    """
    Return config data from the specified string.

    """
    bytes_zipped        = base64.b64decode(codestring)
    bytes_yaml_encoded  = zlib.decompress(bytes_zipped)
    string_yaml_encoded = bytes_yaml_encoded.decode('utf-8')
    cfg                 = yaml.load(string_yaml_encoded,
                                    Loader = yaml.FullLoader)
    return cfg
