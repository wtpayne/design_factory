# -*- coding: utf-8 -*-
"""
---

title:
    "Virtual environment run utilities module."

description:
    "This module contains functions to run
    various different programs in virtual
    environments of various types."

id:
    "cb568718-71d7-443d-b2ce-918faf27bd99"

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


"""


# Since this module is called during the bootstrap
# process, we need to be careful not to depend on
# too many things that won't be present in the
# host environment. (i.e. before any of our
# managed environments get activated).
#
# We make an exception for the shell commands
# pip3 and git, which we require to be installed
# beforehand -- but other than that we should
# seek to stick to python3 builtin libraries
# and unix coreutils only.
#
import os.path
import subprocess
import sys

import da.env


# -----------------------------------------------------------------------------
def stableflow_start(path_cfg      = None,
                     map_cfg       = None,
                     is_local      = False,
                     tup_overrides = None):
    """
    Run a python module in the specified environment.

    """
    import fl.stableflow.cfg
    import fl.stableflow.cfg.exception
    import pl.stableflow.log
    import pl.stableflow.sys

    with pl.stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):

        try:
            if map_cfg and (not path_cfg) and (not tup_overrides):
                cfg = map_cfg
            else:
                cfg = fl.stableflow.cfg.prepare(
                                        path_cfg      = path_cfg,
                                        is_local      = is_local,
                                        tup_overrides = tup_overrides)
            _update_all_environments(cfg)
            _configure_all_launch_commands(cfg)

        except fl.stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            return 1

        else:
            try:
                return pl.stableflow.sys.start(cfg)
            except Exception as err:
                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                return 1


# -----------------------------------------------------------------------------
def stableflow_stop(path_cfg, tup_overrides = None):
    """
    Run a python module in the specified environment.

    """
    import fl.stableflow.cfg
    import fl.stableflow.cfg.exception
    import pl.stableflow.log
    import pl.stableflow.sys

    with pl.stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):

        try:

            cfg = fl.stableflow.cfg.prepare(path_cfg      = path_cfg,
                                            tup_overrides = tup_overrides)
            _configure_all_launch_commands(cfg)

        except fl.stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            return 1

        else:
            try:
                return pl.stableflow.sys.stop(cfg)
            except Exception as err:
                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                return 1


# -----------------------------------------------------------------------------
def _update_all_environments(cfg):
    """
    Update all environments used by the specified cfg.

    TODO: We still need logic to bootstrap the
          setup of remote environments.

    """
    for cfg_host in cfg['host'].values():
        _update_env(id_env = cfg_host.get('environment', None),
                    acct   = cfg_host.get('acct_run',    None),
                    host   = cfg_host.get('hostname',    None))


# -----------------------------------------------------------------------------
def _configure_all_launch_commands(cfg):
    """
    Set each launch command as required for each host environment.

    """
    dirpath_root = da.env.rootpath()
    for cfg_host in cfg['host'].values():
        id_env = cfg_host.get('environment', None)
        cmd    = '{python} -m {module}'.format(
                            python = da.env.path(process_area = 'a0_env',
                                                 id_env       = id_env,
                                                 relpath      = 'bin/python3'),
                            module = 'pl.stableflow.cli.command')
        cfg_host['launch_cmd'] = cmd


# -----------------------------------------------------------------------------
def python_interpreter(id_env,
                       id_env_boot = None,
                       acct        = None,
                       host        = None):
    """
    Run a python interpreter in the specified environment.

    """
    _python(option      = '',
            parameter   = '',
            id_env      = id_env,
            id_env_boot = id_env_boot,
            acct        = acct,
            host        = host)


# -----------------------------------------------------------------------------
def python_source(source,
                  id_env,
                  id_env_boot = None,
                  acct        = None,
                  host        = None):
    """
    Run a python source string in the specified environment.

    """
    _python(option      = '-c',
            parameter   = "'{source}'".format(source = source),
            id_env      = id_env,
            id_env_boot = id_env_boot,
            acct        = acct,
            host        = host)


# -----------------------------------------------------------------------------
def python_function(spec,
                    id_env,
                    iter_args   = None,
                    map_kwargs  = None,
                    id_env_boot = None,
                    acct        = None,
                    host        = None):
    """
    Run a python module in the specified environment.

    """
    (name_module, name_function) = spec.rsplit('.', 1)

    str_args = ''

    if iter_args:
        list_args = list()
        for arg in iter_args:
            list_args.append('\"{arg}\"'.format(arg = arg))
        str_args += ','.join(list_args)

    if map_kwargs:
        list_kwargs = list()
        for (key, value) in map_kwargs.items():
            if isinstance(value, str):
                list_kwargs.append('{key} = "{value}"'.format(
                                                        key   = key,
                                                        value = repr(value)))
            else:
                list_kwargs.append('{key} = {value}'.format(
                                                        key   = key,
                                                        value = repr(value)))

        str_args += ','.join(list_kwargs)


    str_python_source = "'import {mod}; {mod}.{fcn}({arg})'".format(
                                                        mod = name_module,
                                                        fcn = name_function,
                                                        arg = str_args)

    _python(option      = '-c',
            parameter   = str_python_source,
            id_env      = id_env,
            id_env_boot = id_env_boot,
            acct        = acct,
            host        = host)


# -----------------------------------------------------------------------------
def python_module(module,
                  id_env,
                  id_env_boot = None,
                  acct        = None,
                  host        = None):
    """
    Run a python module in the specified environment.

    """
    _python(option      = '-m',
            parameter   = module,
            id_env      = id_env,
            id_env_boot = id_env_boot,
            acct        = acct,
            host        = host)


# -----------------------------------------------------------------------------
def _python(option,
            parameter,
            id_env,
            id_env_boot = None,
            acct        = None,
            host        = None):
    """
    Run a python module or source string in the specified environment.

    """
    import da.env
    filepath_python = da.env.path(process_area = 'a0_env',
                                  id_env       = id_env,
                                  relpath      = 'bin/python3')

    str_fmt = '{py3} {opt} {param}'

    return shell_command(
                str_fmt.format(
                            py3   = filepath_python,
                            opt   = option,
                            param = parameter),
                id_env      = id_env,
                id_env_boot = id_env_boot,
                acct        = acct,
                host        = host)


# -----------------------------------------------------------------------------
def shell_command(command,
                  id_env,
                  id_env_boot = None,
                  acct        = None,
                  host        = None):
    """
    Run a shell command in the specified environment.

    """
    (id_env_boot, acct, host) = _apply_defaults(id_env_boot, acct, host)

    _update_env(
            id_env      = id_env,
            id_env_boot = id_env_boot,
            acct        = acct,
            host        = host)

    is_remote = (acct is not None) and (host is not None)
    if is_remote:
        command.replace("'", "")
        str_fmt = "{ssh} {acct}@{host} '. {activ} && {cmd}'"
    else:
        str_fmt = ". {activ} && {cmd}"

    return _run(str_fmt = str_fmt,
                ssh     = 'ssh -X',
                acct    = acct,
                host    = host,
                cmd     = command,
                activ   = da.env.path(process_area = 'a0_env',
                                      id_env       = id_env,
                                      relpath      = 'bin/activate'))


# -----------------------------------------------------------------------------
def _update_env(id_env,
                id_env_boot = None,
                acct        = None,
                host        = None):
    """
    Update the specified environment.

    A specific bootstrap environment can also be specified.

    """
    (id_env_boot, acct, host) = _apply_defaults(id_env_boot, acct, host)

    bootenv = da.env.path(process_area = 'a0_env',
                          id_env       = id_env_boot)

    # Local or remote via SSH?
    #
    is_remote = (acct is not None) and (host is not None)
    if is_remote:
        str_fmt = "{ssh} {acct}@{host} '. {activ} && {py3} -m {mod} {root} {env}'"
    else:
        str_fmt = '. {activ} && {py3} -m {mod} {root} {env}'

    return _run(str_fmt = str_fmt,
                ssh     = 'ssh',
                acct    = acct,
                host    = host,
                activ   = os.path.join(bootenv, 'bin/activate'),
                py3     = os.path.join(bootenv, 'bin/python3'),
                mod     = 'da.env.ensure_updated',
                root    = da.env.rootpath(),
                env     = id_env)


# -----------------------------------------------------------------------------
def _apply_defaults(id_env_boot, acct, host):
    """
    Apply default values for any missing parameters.

    """
    if id_env_boot is None:
        id_env_boot = 'e000_design_automation_core'

    if acct is not None or host is not None:
        if acct is None:
            acct = os.getlogin()

        if host is None:
            host = 'localhost'

    return (id_env_boot, acct, host)


# -----------------------------------------------------------------------------
def _run(str_fmt, debug_print = False, **kwargs):
    """
    Format and run the specified string as a shell script in a subprocess.

    This function exists so we can intercept
    the command and print it if needed for
    diagnostic and debugging purposes.

    """
    str_command = str_fmt.format(**kwargs)
    if debug_print:
        print(str_command)
    try:
        result = subprocess.run(str_command, shell = True, check = True)
        return result.returncode
    except subprocess.CalledProcessError as err:
        return err.returncode
