# -*- coding: utf-8 -*-
"""
Module of commands and command groups for the stableflow command line interface.

The command line interface consists of a number
of commands, organized into command groups. This
module contains definitions for all of the
command groups and commands used by stableflow.

This file can also be executed as a script to
provide an entry point to a stableflow system.

Argument parsing and the display of command line
help messages is implemented with the help of the
python click library.

    https://click.palletsprojects.com/en/7.x/

Our cli module provides a thin wrapper around the
click library as well as some light customization.

Note that the pl.stableflow.cli.util.OrderedGroup
command class uses the order in which command
functions are defined  in this file to  determine
the order in which the corresponding help text
appears. Please be aware of this when adding,
removing or re-ordering commands.

Finally, please note that since the click library
supports running multiple commands in a single
invocation, it makes the design decision to throw
away the return value from each command function
rather than  propagating it back to the command
line return value. For this reason, we make an
explicit call  to sys.exit() inside each command
function so that we can terminate execution and
return to the command line with an appropriate
return code.


"""


import importlib.metadata
import sys

import click
import pudb

import pl.stableflow.cli.util
import pl.stableflow.log


_set_envvar = set()

pl.stableflow.log.setup()


# -----------------------------------------------------------------------------
def _envvar(name):
    """
    Return the specified name with the common envvar prefix prepended.

    This function accepts as input a single string and returns as output the
    same string prepended with the common prefix that is used to identify
    environment variables of the stableflow system.

    For example, if the string 'FOO' was given as input, the string
    'STABLEFLOW_FOO' would be returned.

    A record is kept of all environment variables in the module level variable
    _set_envvar.

    """
    name_envvar = 'STABLEFLOW_' + name
    _set_envvar.add(name_envvar)
    return name_envvar


# -----------------------------------------------------------------------------
def _stableflow_version():
    """
    Return the version string for stableflow.

    """
    try:
        return importlib.metadata.version("stableflow")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.126"


# -----------------------------------------------------------------------------
@click.group(
        name             = 'main',
        cls              = pl.stableflow.cli.util.OrderedGroup,
        context_settings = { 'max_content_width': 50 })
@click.version_option(
        version          = _stableflow_version())
def grp_main():
    """
    Stableflow command line interface.

    The stableflow command line interface provides the user with the ability to
    start, stop, pause and step a stableflow system.

    A stableflow system is composed of one or more process-hosts, each of which
    contains one or more processes, each of which contains one or more compute
    nodes.

    """
    pass


# -----------------------------------------------------------------------------
@grp_main.group(name = 'system',
                cls  = pl.stableflow.cli.util.OrderedGroup)
def grp_system():
    """
    Control the system as a whole.

    """
    pass


# -----------------------------------------------------------------------------
@grp_main.group(name = 'host',
                cls  = pl.stableflow.cli.util.OrderedGroup)
def grp_host():
    """
    Control a single process host.

    """
    pass


# -----------------------------------------------------------------------------
@grp_system.command()
@click.option(
    '-p', '--cfg-path', 'path_cfg',
    help     = 'File system path for configuration file(s).',
    required = False,
    default  = None,
    type     = click.Path(exists = True),
    nargs    = 1,
    envvar   = _envvar('CFG_PATH'))
@click.option(
    '-c', '--cfg', 'cfg',
    help     = 'Serialized configuration data.',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
@click.option(
    '--makeready/--no-makeready',
    help     = 'Provision and deploy to all hosts before running.',
    required = False,
    default  = False,
    envvar   = _envvar('MAKEREADY'))
@click.option(
    '--local/--no-local',
    help     = 'Run locally.',
    required = False,
    default  = False,
    envvar   = _envvar('LOCAL'))
@click.option(
    '--debug/--no-debug',
    help     = 'Run debugger.',
    required = False,
    default  = False,
    envvar   = _envvar('DEBUG'))
@click.option(
    '-s', '--cfg-addr-delim', 'delim_cfg_addr',
    help     = 'The character to use as a delimiter in config override addresses.',  # noqa pylint: disable=C0301
    required = False,
    default  = '.',
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG_ADDR_DELIM'))
@click.argument(
    'cfg_override',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = -1,
    envvar   = _envvar('CFG_OVERRIDE'))
def start(path_cfg       = None,  # pylint: disable=R0913
          cfg            = None,
          makeready      = False,
          local          = False,
          debug          = False,
          delim_cfg_addr = '.',
          cfg_override   = None):
    """
    Start the specified system.

    This command exposes options and arguments which are useful during
    development and test.

    In particular, CFG_OVERRIDE consists of a sequence of alternating address
    value pairs so that any number of configuration items may be overridden
    from the command line.

    > stableflow system start first:key first_value second:key second_value

    """
    import fl.stableflow.cfg            # pylint: disable=C0415,W0621
    import fl.stableflow.cfg.exception  # pylint: disable=C0415,W0621
    import pl.stableflow.sys            # pylint: disable=C0415,W0621

    if debug:
        pudb.set_trace()

    with pl.stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):
        try:
            cfg = fl.stableflow.cfg.prepare(path_cfg       = path_cfg,
                                            string_cfg     = cfg,
                                            do_make_ready  = makeready,
                                            is_local       = local,
                                            delim_cfg_addr = delim_cfg_addr,
                                            tup_overrides  = cfg_override)
        except fl.stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            sys.exit(1)
        else:
            try:
                sys.exit(pl.stableflow.sys.start(cfg))
            except Exception as err:

                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                sys.exit(1)


# -----------------------------------------------------------------------------
@grp_system.command()
@click.option(
    '-p', '--cfg-path', 'path_cfg',
    help     = 'Directory path for configuration files.',
    required = False,
    default  = None,
    type     = click.Path(exists = True),
    nargs    = 1,
    envvar   = _envvar('CFG_PATH'))
@click.option(
    '-c', '--cfg', 'cfg',
    help     = 'Serialized configuration data.',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
@click.option(
    '-s', '--cfg-addr-delim', 'delim_cfg_addr',
    help     = 'The character to use as a delimiter in config override addresses.',  # noqa pylint: disable=C0301
    required = False,
    default  = '.',
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG_ADDR_DELIM'))
@click.argument(
    'cfg_override',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = -1,
    envvar   = _envvar('CFG_OVERRIDE'))
def stop(path_cfg       = None,
         cfg            = None,
         delim_cfg_addr = '.',
         cfg_override   = None):
    """
    Stop the specified system.

    """
    import fl.stableflow.cfg            # pylint: disable=C0415,W0621
    import fl.stableflow.cfg.exception  # pylint: disable=C0415,W0621
    import pl.stableflow.sys            # pylint: disable=C0415,W0621

    with pl.stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):
        try:
            cfg = fl.stableflow.cfg.prepare(path_cfg       = path_cfg,
                                            string_cfg     = cfg,
                                            do_make_ready  = False,
                                            is_local       = False,
                                            delim_cfg_addr = delim_cfg_addr,
                                            tup_overrides  = cfg_override)
        except fl.stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            sys.exit(1)
        else:
            try:
                sys.exit(pl.stableflow.sys.stop(cfg))
            except Exception as err:

                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                sys.exit(1)


# -----------------------------------------------------------------------------
@grp_system.command()
@click.option(
    '-p', '--cfg-path', 'path_cfg',
    help     = 'Directory path for configuration files.',
    required = False,
    default  = None,
    type     = click.Path(exists = True),
    nargs    = 1,
    envvar   = _envvar('CFG_PATH'))
@click.option(
    '-c', '--cfg', 'cfg',
    help     = 'Serialized configuration data.',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
@click.option(
    '-s', '--cfg-addr-delim', 'delim_cfg_addr',
    help     = 'The character to use as a delimiter in config override addresses.',  # noqa pylint: disable=C0301
    required = False,
    default  = '.',
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG_ADDR_DELIM'))
@click.argument(
    'cfg_override',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = -1,
    envvar   = _envvar('CFG_OVERRIDE'))
def pause(path_cfg       = None,
          cfg            = None,
          delim_cfg_addr = '.',
          cfg_override   = None):
    """
    Pause the specified system.

    """
    import fl.stableflow.cfg            # pylint: disable=C0415,W0621
    import fl.stableflow.cfg.exception  # pylint: disable=C0415,W0621
    import pl.stableflow.sys            # pylint: disable=C0415,W0621

    with pl.stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):
        try:
            cfg = fl.stableflow.cfg.prepare(path_cfg       = path_cfg,
                                            string_cfg     = cfg,
                                            do_make_ready  = False,
                                            is_local       = False,
                                            delim_cfg_addr = delim_cfg_addr,
                                            tup_overrides  = cfg_override)
        except fl.stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            sys.exit(1)
        else:
            try:
                sys.exit(pl.stableflow.sys.pause(cfg))
            except Exception as err:

                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                sys.exit(1)


# -----------------------------------------------------------------------------
@grp_system.command()
@click.option(
    '-p', '--cfg-path', 'path_cfg',
    help     = 'Directory path for configuration files.',
    required = False,
    default  = None,
    type     = click.Path(exists = True),
    nargs    = 1,
    envvar   = _envvar('CFG_PATH'))
@click.option(
    '-c', '--cfg', 'cfg',
    help     = 'Serialized configuration data.',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
@click.option(
    '-s', '--cfg-addr-delim', 'delim_cfg_addr',
    help     = 'The character to use as a delimiter in config override addresses.',  # noqa pylint: disable=C0301
    required = False,
    default  = '.',
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG_ADDR_DELIM'))
@click.argument(
    'cfg_override',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = -1,
    envvar   = _envvar('CFG_OVERRIDE'))
def step(path_cfg       = None,
         cfg            = None,
         delim_cfg_addr = '.',
         cfg_override   = None):
    """
    Single step the specified system.

    """
    import fl.stableflow.cfg            # pylint: disable=C0415,W0621
    import fl.stableflow.cfg.exception  # pylint: disable=C0415,W0621
    import pl.stableflow.sys            # pylint: disable=C0415,W0621

    with pl.stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):
        try:
            cfg = fl.stableflow.cfg.prepare(path_cfg       = path_cfg,
                                            string_cfg     = cfg,
                                            do_make_ready  = False,
                                            is_local       = False,
                                            delim_cfg_addr = delim_cfg_addr,
                                            tup_overrides  = cfg_override)
        except fl.stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            sys.exit(1)
        else:
            try:
                sys.exit(pl.stableflow.sys.step(cfg))
            except Exception as err:

                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                sys.exit(1)


# -----------------------------------------------------------------------------
@grp_system.command()
@click.option(
    '-p', '--cfg-path', 'path_cfg',
    help     = 'Directory path for configuration files.',
    required = False,
    default  = None,
    type     = click.Path(exists = True),
    nargs    = 1,
    envvar   = _envvar('CFG_PATH'))
@click.option(
    '-c', '--cfg', 'cfg',
    help     = 'Serialized configuration data.',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
@click.option(
    '-s', '--cfg-addr-delim', 'delim_cfg_addr',
    help     = 'The character to use as a delimiter in config override addresses.',  # noqa pylint: disable=C0301
    required = False,
    default  = '.',
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG_ADDR_DELIM'))
@click.argument(
    'cfg_override',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = -1,
    envvar   = _envvar('CFG_OVERRIDE'))
def ps(path_cfg       = None,
       cfg            = None,
       delim_cfg_addr = '.',
       cfg_override   = None):
    """
    Print the process status for the the specified system.

    """
    import fl.stableflow.cfg            # pylint: disable=C0415,W0621
    import fl.stableflow.cfg.exception  # pylint: disable=C0415,W0621
    import pl.stableflow.sys            # pylint: disable=C0415,W0621

    with pl.stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):
        try:
            cfg = fl.stableflow.cfg.prepare(path_cfg       = path_cfg,
                                            string_cfg     = cfg,
                                            do_make_ready  = False,
                                            is_local       = False,
                                            delim_cfg_addr = delim_cfg_addr,
                                            tup_overrides  = cfg_override)
        except fl.stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            sys.exit(1)
        else:
            try:
                sys.exit(pl.stableflow.sys.print_process_status(cfg))
            except Exception as err:

                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                sys.exit(1)


# -----------------------------------------------------------------------------
@grp_host.command()
@click.argument(
    'cfg',
    required = True,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
def start_host(cfg = None):
    """
    Start the local process host.

    This command takes a single argument, CFG, which is expected to be a
    serialized configuration structure.

    """
    import pl.stableflow.util.serialization  # pylint: disable=C0415,W0621
    import pl.stableflow.host                # pylint: disable=C0415,W0621
    sys.exit(
        pl.stableflow.host.start(
            pl.stableflow.util.serialization.deserialize(cfg)))


# -----------------------------------------------------------------------------
@grp_host.command()
@click.argument(
    'cfg',
    required = True,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
def stop_host(cfg = None):
    """
    Stop the local process host.

    This command takes a single argument, CFG, which is expected to be a
    serialized configuration structure.

    """
    import pl.stableflow.util.serialization  # pylint: disable=C0415,W0621
    import pl.stableflow.host                # pylint: disable=C0415,W0621
    sys.exit(
        pl.stableflow.host.stop(
            pl.stableflow.util.serialization.deserialize(cfg)))


# -----------------------------------------------------------------------------
@grp_host.command()
@click.argument(
    'cfg',
    required = True,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
def pause_host(cfg = None):
    """
    Pause the local process host.

    This command takes a single argument, CFG, which is expected to be a
    serialized configuration structure.

    """
    import pl.stableflow.util.serialization  # pylint: disable=C0415,W0621
    import pl.stableflow.host                # pylint: disable=C0415,W0621
    sys.exit(
        pl.stableflow.host.pause(
            pl.stableflow.util.serialization.deserialize(cfg)))


# -----------------------------------------------------------------------------
@grp_host.command()
@click.argument(
    'cfg',
    required = True,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
def step_host(cfg = None):
    """
    Single step the local process host.

    This command takes a single argument, CFG, which is expected to be a
    serialized configuration structure.

    """
    import pl.stableflow.util.serialization  # pylint: disable=C0415,W0621
    import pl.stableflow.host                # pylint: disable=C0415,W0621
    sys.exit(
        pl.stableflow.host.step(
            pl.stableflow.util.serialization.deserialize(cfg)))


# -----------------------------------------------------------------------------
@grp_host.command()
@click.argument(
    'cfg',
    required = True,
    type     = click.STRING,
    nargs    = 1,
    envvar   = _envvar('CFG'))
def ps_host(cfg = None):
    """
    Print the process summary for the local process host.

    This command takes a single argument, CFG, which is expected to be a
    serialized configuration structure.

    """
    import pl.stableflow.util.serialization  # pylint: disable=C0415,W0621
    import pl.stableflow.host                # pylint: disable=C0415,W0621
    sys.exit(
        pl.stableflow.host.get_process_summary(
            pl.stableflow.util.serialization.deserialize(cfg)))


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    grp_main()