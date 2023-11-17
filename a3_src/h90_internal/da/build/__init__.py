# -*- coding: utf-8 -*-
"""
---

title:
    "Build utility package."

description:
    "This package provides utility functions to
    build and publish binaries, packages and
    other deliverable items"

id:
    "ec9aa6b0-aef0-48bb-9484-ff9138af4395"

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


import shutil

import da.env
import da.env.run


# -----------------------------------------------------------------------------
def kivy(control_tier,
         relpath,
         id_env_build,
         profile           = None,   # (None, str)
         do_verbose        = False,  # (True, False)
         target            = None,   # (None, 'ios', 'android')
         build             = False,  # (False, 'debug', 'release')
         do_appclean       = False,  # (True, False) target = None only.
         do_distclean      = False,  # (True, False) target = None only.
         do_help           = False,  # (True, False) target = None only.
         do_init           = False,  # (True, False) target = None only.
         do_serve          = False,  # (True, False) target = None only.
         do_setdefault     = False,  # (True, False) target = None only.
         do_version        = False,  # (True, False) target = None only.
         do_clean          = False,  # (True, False) target != None only.
         do_update         = False,  # (True, False) target != None only.
         do_deploy         = False,  # (True, False) target != None only.
         do_run            = False,  # (True, False) target != None only.
         do_android_adb    = False,  # (True, False) target = android.
         do_android_clean  = False,  # (True, False) target = android.
         do_android_logcat = False,  # (True, False) target = android.
         do_android_p4a    = False,  # (True, False) target = android.
         android_adb_args  = None,   # (None, str) do_android_adb only.
         android_p4a_args  = None,   # (None, str) do_android_p4a only.
         do_ios_list_ident = False,  # (True, False) target = ios.
         do_ios_open_xcode = False,  # (True, False) target = ios.
         do_display_cmd    = False):
    """
    Build the specified Kivy app using buildozer.

    Usage:
      buildozer [--profile <name>] [--verbose] [target] <command>...
      buildozer --version

    Available targets:
      android       Android target, based on
                    python-for-android project
      ios           iOS target, based on kivy-ios
                    project

    Global commands (without target):
      appclean      Clean the .buildozer folder
                    in the app directory.
      distclean     Clean the whole Buildozer
                    environment.
      help          Show the Buildozer help.
      init          Create a initial buildozer.spec
                    in the current directory
      serve         Serve the bin directory
                    via SimpleHTTPServer
      setdefault    Set the default command
                    to run when no arguments
                    are given
      version       Show the Buildozer version

    Target commands:
      clean         Clean the target environment
      update        Update the target dependencies
      debug         Build the application in debug mode
      release       Build the application in release mode
      deploy        Deploy the application on the device
      run           Run the application on the device
      serve         Serve the bin directory via SimpleHTTPServer

    Target "android" commands:
      adb           Run adb from the Android SDK.
                    Args must come after --, or
                    use --alias to make an alias
      clean         Clean the build and distribution
      logcat        Show the log from the device
      p4a           Run p4a commands. Args must
                    come after --, or use --alias
                    to make an alias

    Target "ios" commands:
      list_identities  List the available identities
                       to use for signing.
      xcode            Open the xcode project.


    """

    # Validate input arguments.
    #
    NONETYPE = type(None)
    assert isinstance(profile, (str, NONETYPE))
    assert do_verbose        in (True, False)
    assert target            in ('android', 'ios', None)
    assert build             in ('debug', 'release', None)
    assert do_appclean       in (True, False)
    assert do_distclean      in (True, False)
    assert do_help           in (True, False)
    assert do_init           in (True, False)
    assert do_serve          in (True, False)
    assert do_setdefault     in (True, False)
    assert do_version        in (True, False)
    assert do_clean          in (True, False)
    assert do_update         in (True, False)
    assert do_deploy         in (True, False)
    assert do_run            in (True, False)
    assert do_serve          in (True, False)
    assert do_ios_list_ident in (True, False)
    assert do_ios_open_xcode in (True, False)
    assert do_android_clean  in (True, False)
    assert do_android_logcat in (True, False)
    assert do_android_adb    in (True, False)
    assert isinstance(android_adb_args, (str, NONETYPE))
    assert do_android_p4a    in (True, False)
    assert isinstance(android_p4a_args, (str, NONETYPE))

    list_opts = _build_list_opts(profile           = profile,
                                 do_verbose        = do_verbose,
                                 target            = target,
                                 build             = build,
                                 do_appclean       = do_appclean,
                                 do_distclean      = do_distclean,
                                 do_help           = do_help,
                                 do_init           = do_init,
                                 do_serve          = do_serve,
                                 do_setdefault     = do_setdefault,
                                 do_version        = do_version,
                                 do_clean          = do_clean,
                                 do_update         = do_update,
                                 do_deploy         = do_deploy,
                                 do_run            = do_run,
                                 do_android_adb    = do_android_adb,
                                 do_android_clean  = do_android_clean,
                                 do_android_logcat = do_android_logcat,
                                 do_android_p4a    = do_android_p4a,
                                 android_adb_args  = android_adb_args,
                                 android_p4a_args  = android_p4a_args,
                                 do_ios_list_ident = do_ios_list_ident,
                                 do_ios_open_xcode = do_ios_open_xcode)

    if do_display_cmd:
        str_option_delimiter = ' \\\n   '  # Newlines to make it readable.
    else:
        str_option_delimiter = ' '

    command = 'cd {dir}{delim}&&{delim}buildozer{delim}{opts}'.format(
                                dir   = da.env.path(
                                                process_area = 'a4_tmp',
                                                control_tier = control_tier,
                                                relpath      = relpath),
                                opts  = str_option_delimiter.join(list_opts),
                                delim = str_option_delimiter)

    if do_display_cmd:
        print(command)

    _copy_to_temporary_build_area(
                            control_tier = control_tier,
                            relpath      = relpath)

    return da.env.run.shell_command(
                            command = command,
                            id_env  = id_env_build)


# -----------------------------------------------------------------------------
def _copy_to_temporary_build_area(control_tier, relpath):
    """
    Recursively copy the source design
    documents to the temporary build
    area.

    """
    shutil.copytree(da.env.path(process_area = 'a3_src',
                                control_tier = control_tier,
                                relpath      = relpath),
                    da.env.path(process_area = 'a4_tmp',
                                control_tier = control_tier,
                                relpath      = relpath),
                    dirs_exist_ok = True)


# -----------------------------------------------------------------------------
def _build_list_opts(profile,
                     do_verbose,
                     target,
                     build,
                     do_appclean,
                     do_distclean,
                     do_help,
                     do_init,
                     do_serve,
                     do_setdefault,
                     do_version,
                     do_clean,
                     do_update,
                     do_deploy,
                     do_run,
                     do_android_adb,
                     do_android_clean,
                     do_android_logcat,
                     do_android_p4a,
                     android_adb_args,
                     android_p4a_args,
                     do_ios_list_ident,
                     do_ios_open_xcode):
    """
    Build a list of command options and positional args.

    """

    list_command_options = list()  # Command options come before the '--'.
    list_positional_args = list()  # Positional args come after the '--'.

    if profile is not None:
        list_command_options.extend(('--profile', profile))

    if do_verbose:
        list_command_options.append('--verbose')

    # Global commands (without target)
    #
    if target is None:
        for (is_ena, str_cmd) in ((do_appclean,   'appclean'   ),
                                  (do_distclean,  'distclean'  ),
                                  (do_help,       'help'       ),
                                  (do_init,       'init'       ),
                                  (do_serve,      'serve'      ),
                                  (do_setdefault, 'setdefault' ),
                                  (do_version,    'version'    )):
            if is_ena:
                list_command_options.append(str_cmd)

    # Target commands
    #
    else:

        list_command_options.append(target)     # ios or android

        if build is not None:
            list_command_options.append(build)  # debug or release

        for (is_ena, str_cmd) in ((do_clean,  'clean'  ),
                                  (do_update, 'update' ),
                                  (do_deploy, 'deploy' ),
                                  (do_run,    'run'    ),
                                  (do_serve,  'serve'  )):
            if is_ena:
                list_command_options.append(str_cmd)

        # Android target commands.
        #
        if target == 'android':
            for (is_ena, str_cmd) in ((do_android_adb,    'adb'),
                                      (do_android_clean,  'clean'),
                                      (do_android_logcat, 'logcat'),
                                      (do_android_p4a,    'p4a')):
                if is_ena:
                    list_command_options.append(str_cmd)

            if do_android_adb and android_adb_args is not None:
                list_positional_args.append(android_adb_args)

            if do_android_p4a and android_p4a_args is not None:
                list_positional_args.append(android_p4a_args)

        # ios target commands.
        #
        elif target == 'ios':
            for (is_ena, str_cmd) in ((do_ios_list_ident, 'list_identities'),
                                      (do_ios_open_xcode, 'xcode')):
                if is_ena:
                    list_command_options.append(str_cmd)

    if list_positional_args:
        list_opts = list_command_options + ['--'] + list_positional_args
    else:
        list_opts = list_command_options

    return list_opts
