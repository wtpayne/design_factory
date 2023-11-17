# -*- coding: utf-8 -*-
"""
---

title:
    "Build system commands package."

description:
    "This package provides commands to run
    various build system processes and
    operations."

id:
    "4edea1be-2fb8-42f4-aae2-aaeea56a3997"

type:
    dt002_python_package

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


import functools
import importlib
import inspect
import os
import os.path

import click

import da.cli.group
import da.env.run


# -----------------------------------------------------------------------------
def add_demos(grp_parent):
    """
    Add a command group for each demo.

    """

    dirpath_root      = _dirpath_root()
    dirpath_internal  = os.path.join(dirpath_root,     'a3_src/h90_internal')
    dirpath_demo_root = os.path.join(dirpath_internal, 'da/demo')

    for id_demo in sorted(os.listdir(dirpath_demo_root)):

        dirpath_demo = os.path.join(dirpath_demo_root, id_demo)
        if not _is_demo_dir(dirpath_demo):
            continue
 
        grp_demo     = _create_group_for_demo(      grp_parent,   id_demo)
        filepath_py  = _filepath_python_module(     dirpath_demo, id_demo)
        filepath_cfg = _filepath_stableflow_config( dirpath_demo, id_demo)

        if os.path.exists(filepath_py):
            _add_functions_from_python_module_to_group(
                                                group    = grp_demo,
                                                filepath = filepath_py,
                                                rootpath = dirpath_internal)

        elif os.path.exists(filepath_cfg):
            _add_start_stop_commands_for_stableflow_config(
                                                group    = grp_demo,
                                                filepath = filepath_cfg,
                                                id_demo  = id_demo)


# -----------------------------------------------------------------------------
def _dirpath_root():
    """
    Return the directory path of the root of the repository.

    """

    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    relpath_root = '../../../../..'
    dirpath_root = os.path.normpath(os.path.join(dirpath_self, relpath_root))
    return dirpath_root


# -----------------------------------------------------------------------------
def _is_demo_dir(path):
    """
    Return true if and only if the specified directory name is a demo.

    """

    dirname = os.path.basename(path)
    is_demo = os.path.isdir(path) and dirname.startswith('dm')
    return is_demo


# -----------------------------------------------------------------------------
def _create_group_for_demo(grp_parent, id_demo):
    """
    Return a click command group for the specified demo id.
    
    """

    str_help     = 'Demo {id}.'.format(id = id_demo)
    grp_demo     = da.cli.group.Ordered(id_demo, help = str_help)
    num_demo     = id_demo.split(sep = '_', maxsplit = 1)[0]
    grp_parent.add_command(grp_demo, name = num_demo)
    return grp_demo


# -----------------------------------------------------------------------------
def _filepath_python_module(dirpath, id_demo):
    """
    Return the filepath of the demo entrypoint module.

    """

    return os.path.join(dirpath, '{id}.py'.format(id = id_demo))


# -----------------------------------------------------------------------------
def _filepath_stableflow_config(dirpath, id_demo):
    """
    Return the filepath of the demo stableflow configuration file.

    """

    return os.path.join(dirpath,
                        '{id}.stableflow.cfg.yaml'.format(id = id_demo))


# -----------------------------------------------------------------------------
def _add_functions_from_python_module_to_group(group, filepath, rootpath):
    """
    Add functions from the specified python module to the group as commands.

    """

    spec_module  = _spec_module(filepath, rootpath)
    module       = importlib.import_module(spec_module)
    iter_members = inspect.getmembers(module)
    list_fcn     = sorted((item for item in iter_members 
                                                if inspect.isfunction(item[1])),
                        key = lambda tup: inspect.getsourcelines(tup[1])[1])

    for (name, callback) in list_fcn:

        # Ignore all functions that start
        # with an underscore as these are
        # by convention considered to be
        # private.
        #
        if name.startswith('_'):

            continue

        else:

            _add_command_to_group(group       = group,
                                  spec_module = spec_module,
                                  name        = name,
                                  callback    = callback)


# -----------------------------------------------------------------------------
def _spec_module(filepath, rootpath):
    """
    Return the module spec for the specified python file and root directory.

    """

    rel_path = os.path.relpath(filepath, rootpath)

    return rel_path[:-3].replace(os.sep, '.')
    

# -----------------------------------------------------------------------------
def _add_command_to_group(group, spec_module, name, callback):
    """
    Add a command to the specified group using the provided parameters.

    """

    if hasattr(callback, '__doc__'):
        str_help = callback.__doc__.strip()
    else:
        str_help = 'Call {mod}.{fcn}.'.format(
                                        mod = spec_module,
                                        fcn = name)

    group.add_command(name = name,
                      cmd  = click.Command(name     = name,
                                           callback = callback,
                                           help     = str_help))


# -----------------------------------------------------------------------------
def _add_start_stop_commands_for_stableflow_config(group, filepath, id_demo):
    """
    Add start and stop commands for the specified stableflow config.

    """

    fcn_start = functools.partial(da.env.run.stableflow_start,
                                  path_cfg = filepath)
    group.add_command(
        name = 'start',
        cmd  = click.Command(
                        name     = 'start',
                        callback = fcn_start,
                        help     = 'Start {id}.'.format(id = id_demo)))

    fcn_stop = functools.partial(da.env.run.stableflow_stop,
                                 path_cfg = filepath)
    group.add_command(
        name = 'stop',
        cmd  = click.Command(
                        name     = 'stop',
                        callback = fcn_stop,
                        help     = 'Stop {id}.'.format(id = id_demo)))
