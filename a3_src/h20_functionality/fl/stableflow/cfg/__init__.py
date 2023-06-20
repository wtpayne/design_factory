# -*- coding: utf-8 -*-
"""
Package of functions that manipulate configuration data.

"""

import collections
import enum
import glob
import json
import os

import loguru

import fl.stableflow.cfg.data
import fl.stableflow.cfg.edge
import fl.stableflow.cfg.exception
import fl.stableflow.cfg.load
import fl.stableflow.cfg.override
import fl.stableflow.cfg.queue
import fl.stableflow.cfg.validate
import pl.stableflow.util
import pl.stableflow.util.serialization

from fl.stableflow.cfg.exception import CfgError


# -----------------------------------------------------------------------------
def set_launch_command(cfg, rootpath_env):
    """
    Set each launch command as required for each host environment.

    """

    for cfg_host in cfg['host'].values():

        id_env         = cfg_host.get('environment', None)
        dirpath_env    = os.path.join(rootpath_env, id_env)
        relpath_py     = 'bin/python3'
        filepath_py    = os.path.join(dirpath_env, relpath_py)
        spec_module    = 'pl.stableflow.cli.command'
        str_launch_cmd = '{python} -m {module}'.format(python = filepath_py,
                                                       module = spec_module)
        cfg_host['launch_cmd'] = str_launch_cmd


# -----------------------------------------------------------------------------
@loguru.logger.catch(exclude = CfgError)
def prepare(path_cfg       = None,  # pylint: disable=R0913
            string_cfg     = None,
            map_cfg        = None,
            do_make_ready  = False,
            is_local       = False,
            delim_cfg_addr = '.',
            tup_overrides  = None):
    """
    Load configuration and override fields as required.

    """

    has_cfg_files  = path_cfg is not None
    has_cfg_string = string_cfg is not None
    has_cfg_map    = map_cfg is not None
    has_cfg        = has_cfg_files or has_cfg_string or has_cfg_map
    if not has_cfg:
        raise CfgError('No configuration data has been provided.')

    # Load configuration from the specified
    # path, if it has been provided.
    #
    cfg = dict()
    if has_cfg_files:
        cfg_from_path = fl.stableflow.cfg.load.from_path(path_cfg)
        if cfg_from_path:
            cfg = merge_dicts(cfg, cfg_from_path)

    # Merge in any additional configuration
    # data passed in as a string, if
    # provided.
    #
    if has_cfg_string:
        cfg_from_string = pl.stableflow.util.serialization.deserialize(
                                                                string_cfg)
        if cfg_from_string:
            cfg = merge_dicts(cfg, cfg_from_string)

    # Merge in any additional configuration
    # data passed in as a dict, if
    # provided.
    #
    if has_cfg_map:
        cfg = merge_dicts(cfg, map_cfg)

    # Apply any command line or env-var
    # overrides that may have been
    # supplied.
    #
    cfg = fl.stableflow.cfg.override.apply(
                                        cfg            = cfg,
                                        tup_overrides  = tup_overrides,
                                        delim_cfg_addr = delim_cfg_addr)

    # Apply default values for each host.
    # for cfg_host in cfg['host'].values():
    #     if 'launch_cmd' not in cfg_host:
    #         cfg_host['launch_cmd'] = './da stableflow'

    # Calculate some UIDs for the file-path
    # and the config file content.
    #
    id_cfg = pl.stableflow.util.serialization.hexdigest(cfg)[0:8]
    if path_cfg:
        id_path = pl.stableflow.util.serialization.hexdigest(path_cfg)[0:8]
    else:
        id_path = '00000000'

    cfg['runtime']                         = dict()
    cfg['runtime']['opt']                  = dict()
    cfg['runtime']['id']                   = dict()
    cfg['runtime']['proc']                 = dict()
    cfg['runtime']['opt']['do_make_ready'] = do_make_ready
    cfg['runtime']['opt']['is_local']      = is_local
    cfg['runtime']['id']['path_cfg']       = path_cfg if path_cfg else ''
    cfg['runtime']['id']['id_path']        = id_path
    cfg['runtime']['id']['id_system']      = cfg['system']['id_system']
    cfg['runtime']['id']['id_cfg']         = id_cfg
    cfg['runtime']['id']['id_host']        = 'tbd'
    cfg['runtime']['id']['id_process']     = 'tbd'
    cfg['runtime']['id']['ts_run']         = '00000000000000'
    cfg['runtime']['id']['id_run']         = '00000000'

    # cfg = pl.stableflow.util.format_all_strings(cfg)  # ???
    cfg = fl.stableflow.cfg.validate.normalized(cfg)

    if cfg is None:
        raise fl.stableflow.cfg.exception.CfgError('No config.')

    return cfg


# -----------------------------------------------------------------------------
def denormalize(cfg):
    """
    Add redundant information to cfg to make it more convenient to use.

    The input configuration is designed
    to be DRY and succinct, at the cost
    of making some information implicit
    or otherwise requiring computation
    to infer. This function enriches
    the cfg data structure and makes
    such information explicit.

    """

    return fl.stableflow.cfg.queue.denormalize(
                fl.stableflow.cfg.edge.denormalize(
                    fl.stableflow.cfg.data.denormalize(cfg)))


# -----------------------------------------------------------------------------
def merge_dicts(first, second):
    """
    Merge two dictionaries. second takes priority.

    """

    return dict(_merge_dicts(first, second))


# -----------------------------------------------------------------------------
def _merge_dicts(first, second):
    """
    Merge two dictionaries (recursive function). second takes priority.

    """

    for key in set(first.keys()).union(second.keys()):
        _in_first  = key in first
        _in_second = key in second
        if _in_first and _in_second:
            _isdict_first  = isinstance(first[key], dict)
            _isdict_second = isinstance(second[key], dict)
            if _isdict_first and _isdict_second:
                yield (key, dict(_merge_dicts(first[key], second[key])))
            else:
                # second overwrites first if both are present.
                yield (key, second[key])
        elif _in_first:
            yield (key, first[key])
        else:
            yield (key, second[key])
