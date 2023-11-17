# -*- coding: utf-8 -*-
"""
---

title:
    "Environment specific utility commands package."

description:
    "This package provides commands to run
    various utilities in specific managed
    environments."

id:
    "541bcca6-bcf1-42d5-ab6d-6dd2145702c4"

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
import json
import os
import re
import subprocess

import click

import da.cli.group
import da.env


# -----------------------------------------------------------------------------
def add_env_tools(grp_parent):
    """
    Add environment specific tools to the specified click command group.

    """

    for (id_env, cfg_env) in da.env.iter_cfg_env():

        # Add a click command group for each
        # environment with an envspec file in
        # the h10_resource/envspec directory.
        #
        str_help   = '{env} utils.'.format(env = id_env)
        num_env    = id_env.split(sep = '_', maxsplit = 1)[0]
        grp_id_env = da.cli.group.Ordered(id_env, help = str_help)
        grp_parent.add_command(grp_id_env, name = num_env)

        # Add a command for each tool which
        # is compatible with the current
        # environment, as determined by the
        # content of the envspec file.
        #
        set_env_deps = set(_iter_name_deps(cfg_env))
        tool_table   = (
            ('bash', 'bash',     'shell', _bash, ()                 ),
            ('cpy',  'cpython',  'repl',  _cpy,  ()                 ),
            ('ipy',  'ipython',  'repl',  _ipy,  ('ptpython',
                                                  'ipython')        ),
            ('ptpy', 'ptpython', 'repl',  _ptpy, ('ptpython',)      ),
            ('bpy',  'bpython',  'repl',  _bpy,  ('prompt-toolkit',
                                                  'bpython')        ))

        for (abbrev, toolname, tooltype, callback, tool_deps) in tool_table:

            # It is easy to miss out the trailing
            # comma on a single-item tuple, so
            # we put a sanity check here to make
            # sure that all required deps are
            # actually given as tuples of strings.
            #
            assert isinstance(tool_deps, tuple)

            fcn_partial = functools.partial(callback, id_env)

            if set(tool_deps).issubset(set_env_deps):
                grp_id_env.add_command(
                    name = toolname,
                    cmd  = click.Command(
                            name     = toolname,
                            callback = fcn_partial,
                            help     = 'Start a {name} {type}.'.format(
                                                            name = toolname,
                                                            type = tooltype)))


# -----------------------------------------------------------------------------
def _iter_name_deps(cfg_env):
    """
    Yield the name of each dependency in the specified environment config.

    """

    for item in cfg_env['list_item']:

        try:
            type_item = item['type']
        except (KeyError, TypeError):
            continue

        if type_item == 'local':
            continue

        elif type_item == 'pep508':
            yield re.split(pattern  = r'<=|<|!=|==|>=|>|~=|===',
                           string   = item['spec'],
                           maxsplit = 1)[0]

        elif type_item == 'github':
            yield item['remote'].rsplit(sep      = '/',
                                        maxsplit = 1)[1].split(sep      = '.',
                                                               maxsplit = 1)[0]

        else:
            raise RuntimeError('envspec line-item type not recognised.')


# -----------------------------------------------------------------------------
def _bash(id_env):
    """
    Start a bash shell.

    """

    dirpath_self  = os.path.dirname(os.path.realpath(__file__))
    filepath_init = os.path.join(dirpath_self, 'bash_init.sh')

    da.env.run.shell_command(
            command = 'bash --init-file {file}'.format(file = filepath_init),
            id_env  = id_env)


# -----------------------------------------------------------------------------
def _cpy(id_env):
    """
    Start a cpython repl.

    """

    return da.env.run.python_interpreter(id_env = id_env)


# -----------------------------------------------------------------------------
def _ipy(id_env):
    """
    Start a ipython repl.

    """

    source = 'import ptpython.ipython; ptpython.ipython.embed()'
    return da.env.run.python_source(source = source,
                                    id_env = id_env)


# -----------------------------------------------------------------------------
def _ptpy(id_env):
    """
    Start a ptpython repl.

    """

    source = 'import ptpython.repl; ptpython.repl.embed(globals(), locals())'
    return da.env.run.python_source(source = source,
                                    id_env = id_env)


# -----------------------------------------------------------------------------
def _bpy(id_env):
    """
    Start a bpython repl.

    """

    source = 'import bpython; bpython.embed()'
    return da.env.run.python_source(source = source,
                                    id_env = id_env)


# # -----------------------------------------------------------------------------
# def _browser(dirpath_root, id_env):
#     """
#     Start a design index browser.

#     """
#     import os
#     import da.cli.env.browser
#     da.cli.env.browser.run()


# # -----------------------------------------------------------------------------
# def _direpl(dirpath_root, id_env):
#     """
#     Start a design index repl.

#     """
#     import os
#     import da.cli.env.direpl
#     da.cli.env.direpl.run()
