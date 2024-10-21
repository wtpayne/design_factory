# -*- coding: utf-8 -*-
"""
---

title:
    "Virtual environment management package."

description:
    "This package is used to create and update
    virtual environments of various types."

id:
    "1535294d-eedc-4d08-8721-31be6ecbef43"

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
import collections
import datetime
import json
import os
import os.path
import shutil
import subprocess
import sys
import time


# -----------------------------------------------------------------------------
def tup_control_tier():
    """
    Return a tuple with all control tiers in it.

    """

    return ('h00_thirdparty',
            'h10_resource',
            'h20_functionality',
            'h30_platform',
            'h40_component',
            'h50_subsystem',
            'h60_system',
            'h70_bespoke',
            'h80_research',
            'h90_internal')


# -----------------------------------------------------------------------------
def iter_id_env():
    """
    Yield all known id_env in the current workspace.

    """

    str_ext = '.envspec.json'
    num_ext = len(str_ext)

    for name in sorted(os.listdir(path(process_area = 'a3_src',
                                       control_tier = 'h10_resource',
                                       relpath      = 'envspec'))):
        if name.endswith(str_ext):
            id_env = name[0:-num_ext]
            yield id_env


# -----------------------------------------------------------------------------
def iter_cfg_env():
    """
    Yield all known env config in the current workspace.

    """

    str_ext = '.envspec.json'
    num_ext = len(str_ext)
    dirpath = path(process_area = 'a3_src',
                   control_tier = 'h10_resource',
                   relpath      = 'envspec')
    for name in sorted(os.listdir(dirpath)):
        if name.endswith(str_ext):
            id_env = name[0:-num_ext]
            with open(os.path.join(dirpath, name), 'rt') as file:
                yield (id_env, json.load(file))


# -----------------------------------------------------------------------------
def dirpath_env_root():
    """
    Return the directory path to the environment root.

    """

    return os.path.join(rootpath(), 'a0_env', 'venv')


# -----------------------------------------------------------------------------
def path(process_area = 'a3_src',
         control_tier = None,
         id_env       = None,
         relpath      = '.'):
    """
    Return an absolute file or directory path in the current workspace.

    """

    dirpath_root = rootpath()

    # Ensure we have a valid process area.
    #
    tup_valid_process_area = ('a0_env',
                              'a1_cfg',
                              'a2_dat',
                              'a3_src',
                              'a4_tmp',
                              'a5_cms')
    assert process_area in tup_valid_process_area

    # A control_tier only makes sense
    # in the src and tmp process areas.
    #
    if process_area in ('a3_src', 'a4_tmp'):
        assert control_tier in tup_control_tier()
        tup_path_parts = (dirpath_root,
                          process_area,
                          control_tier,
                          relpath)

    # An id_env only makes sense in the
    # a0_env process area
    elif process_area in ('a0_env',):
        assert id_env is not None and id_env.startswith('e')
        tup_path_parts = (dirpath_env_root(),
                          id_env,
                          relpath)

    # All other process areas are
    # currently more freeform.
    #
    else:
        tup_path_parts = (dirpath_root,
                          process_area,
                          relpath)

    return os.path.normpath(os.path.join(*tup_path_parts))


# -----------------------------------------------------------------------------
def rootpath():
    """
    Return an absolute directory path to the root of the current workspace.

    """

    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    relpath_root = '../../../..'
    dirpath_root = os.path.normpath(os.path.join(dirpath_self, relpath_root))
    return dirpath_root


# -----------------------------------------------------------------------------
def do_ensure_updated(dirpath_root, id_env):
    """
    Ensure that the specified environment is up to date.

    This public function is used by the design
    factory to update environments as needed.

    """

    dirpath_env = _dirpath_env(dirpath_root, id_env)

    # Ensure the virtual environment exists,
    # recreating it from scratch if any problems
    # are detected.
    #
    _delete_env_if_corrupted(dirpath_env)
    is_new_env  = _create_env_if_not_exists(dirpath_env)

    # If the virtual environment is not up to date
    # then perform an update, generating the
    # requirements file and pip installing
    # any newly added requirements.
    #
    is_up_to_date    = _is_up_to_date(dirpath_root, id_env, dirpath_env)
    is_stale         = not is_up_to_date
    is_update_needed = is_new_env or is_stale

    if is_update_needed:

        if is_new_env:
            print(f'Creating new environment: {id_env}')
        else:
            print(f'Updating stale environment: {id_env}')

        do_update(dirpath_root, id_env)


# -----------------------------------------------------------------------------
def do_update(dirpath_root, id_env):
    """
    Update the specified environment with the latest envspec.

    This public function is used by the top level
    'da' script to update the environment
    e000_design_automation_core if required.

    """

    # Set the envspec config file modification
    # time to two seconds in the past. This
    # ensures that once the update process is
    # completed, the envspec file will have a
    # last-modified timestamp that is guaranteed
    # to be older than any of the last modified
    # timestamps that are generated by any of
    # the subsequent update operations.
    #
    # This eliminates the possibility of an
    # invalid or corrupt last-modified timestamp
    # on the envspec file causing the update
    # process to run multiple times, making
    # diagnosis of such issues easier.
    #
    filepath_spec = _filepath_envspec(dirpath_root = dirpath_root,
                                      id_env       = id_env)
    _touch(filepath = filepath_spec, delta_secs = -2)

    try:

        map_map_filepath = _prepare_cfg_pack(
                                    dirpath_root = dirpath_root,
                                    id_env       = id_env,
                                    envspec      = _load_json(filepath_spec))

        _apply_cfgpack(dirpath_root     = dirpath_root,
                       id_env           = id_env,
                       map_map_filepath = map_map_filepath)

    except Exception as error:
        _delete_virtualenv(dirpath_root = dirpath_root,
                           id_env       = id_env)
        raise error


# -----------------------------------------------------------------------------
def _load_json(filepath_json):
    """
    Return the deserialized content from the specified file.

    """

    with open(filepath_json, 'rt') as file_json:
        return json.load(file_json)


# -----------------------------------------------------------------------------
def _touch(filepath, delta_secs = 0):
    """
    Set last-accessed and last-modified times of filepath.

    """

    timestamp_now = time.time()
    datetime_now  = datetime.datetime.fromtimestamp(timestamp_now)
    datetime_mod  = datetime_now + datetime.timedelta(seconds = delta_secs)
    timestamp_mod = datetime_mod.timestamp()
    os.utime(filepath, (timestamp_mod, timestamp_mod))


# -----------------------------------------------------------------------------
def _dirpath_env(dirpath_root, id_env):
    """
    Return the directory path of the specified environment.

    """

    return os.path.join(dirpath_root, "a0_env", "venv", id_env)


# -----------------------------------------------------------------------------
def _delete_env_if_corrupted(dirpath_env):
    """
    Delete the specified environment if corruption is detected.

    """

    filepath_activate = os.path.join(dirpath_env, "bin", "activate")
    if os.path.isdir(dirpath_env) and not os.path.isfile(filepath_activate):
        shutil.rmtree(dirpath_env)


# -----------------------------------------------------------------------------
def _create_env_if_not_exists(dirpath_env):
    """
    Return True if a new environment was created, false otherwise.

    This function will create the specified
    environment if it does not already exist.

    """

    if os.path.isdir(dirpath_env):
        is_new_env = False
    else:
        subprocess.check_call(["python3", "-m", "venv", dirpath_env])
        is_new_env = True
    return is_new_env


# -----------------------------------------------------------------------------
def _is_up_to_date(dirpath_root, id_env, dirpath_env):
    """
    Return true if the specified environment is up to date, false otherwise.

    """

    mtime_envspec  = os.path.getmtime(_filepath_envspec(dirpath_root, id_env))
    mtime_venv_pkg = os.path.getmtime(_dirpath_venv_pkg(dirpath_env))
    is_updated_pkg = mtime_venv_pkg > mtime_envspec

    dirpath_venv_whl = _dirpath_venv_whl(dirpath_env)
    if os.path.exists(dirpath_venv_whl):
        mtime_venv_whl  = os.path.getmtime(dirpath_venv_whl)
        is_updated_whl  = mtime_venv_whl > mtime_envspec
        is_updated_venv = is_updated_pkg or is_updated_whl
    else:
        is_updated_venv = is_updated_pkg
    return is_updated_venv


# -----------------------------------------------------------------------------
def _filepath_envspec(dirpath_root, id_env):
    """
    Return the filepath of the envspec file for the specified environment.

    """

    filename = '{id_env}.envspec.json'.format(id_env = id_env)
    return os.path.join(dirpath_root,
                        'a3_src',
                        'h10_resource',
                        'envspec',
                        filename)


# -----------------------------------------------------------------------------
def _dirpath_venv_pkg(dirpath_env):
    """
    Return the path of the virtual environment site packages directory.

    """

    version_python = '.'.join(sys.version.split('.')[0:2])
    dirname_python = 'python{version}'.format(version = version_python)
    return os.path.join(dirpath_env, 'lib', dirname_python, 'site-packages')


# -----------------------------------------------------------------------------
def _dirpath_venv_whl(dirpath_env):
    """
    Return the path of the virtual environment python wheels directory.

    """

    return os.path.join(dirpath_env, 'share', 'python-wheels')


# -----------------------------------------------------------------------------
def _prepare_cfg_pack(dirpath_root, id_env, envspec):
    """
    Create a set of configuration scripts for the specified environment.

    """

    # Work out the set of installation
    # phases we need to manage, also
    # adding to the set a default
    # phase id for items without an
    # explicitly specified phase id.
    #
    set_id_phase = set()
    for item in envspec['list_item']:
        try:
            set_id_phase.add(item['phase'])
        except (KeyError, TypeError):
            continue
    id_phase_default = max(set_id_phase) + 1 if set_id_phase else 1
    set_id_phase.add(id_phase_default)

    # For each phase and type work out
    # which configuration items are
    # used.
    #
    ddict = collections.defaultdict
    ddict_of_lists = lambda: ddict(list)
    map_map_list_item = ddict(ddict_of_lists)
    for item in envspec['list_item']:
        try:
            id_phase = item['phase']
            id_type  = item['type']
        except (KeyError, TypeError):
            continue
        set_type_req_legacy = {'legacy-pip', 'legacy-git', 'legacy-editable'}
        set_type_req_pep517 = {'pep517-pip', 'pep517-git', 'pep517-editable'}
        match id_type:
            case 'shell':
                id_method = 'cfg-script-shell'
            case _ if id_type in set_type_req_legacy:
                id_method = 'cfg-pip-legacy'
            case _ if id_type in set_type_req_pep517:
                id_method = 'cfg-pip-pep517'
            case _:
                raise ValueError(
                        f'Unknown envspec item type ({id_type}) in {id_env}.')
        map_map_list_item[id_phase][id_method].append(item)


    # Create a directory to hold all of the
    # scripts and requirements.txt files
    # needed to configure this environment.
    #
    dirpath_cfgpack = _dirpath_cfgpack(dirpath_root, id_env)
    if not os.path.exists(dirpath_cfgpack):
        os.makedirs(dirpath_cfgpack)

    # Create configuration scripts and
    # requirements.txt files for each
    # configuration phase and type.
    #
    map_map_filepath = collections.defaultdict(dict)
    for (id_phase, map_list_item) in sorted(map_map_list_item.items()):
        for (id_method, list_item) in sorted(map_list_item.items()):
            match id_method:
                case 'cfg-script-shell':
                    filepath = _prepare_shell_script(
                                            dirpath_root    = dirpath_root,
                                            dirpath_cfgpack = dirpath_cfgpack,
                                            id_phase        = id_phase,
                                            list_item       = list_item)

                case 'cfg-pip-legacy':
                    filepath = _prepare_requirements_file(
                                            dirpath_root    = dirpath_root,
                                            dirpath_cfgpack = dirpath_cfgpack,
                                            id_phase        = id_phase,
                                            list_item       = list_item,
                                            id_std          = 'legacy')

                case 'cfg-pip-pep517':
                    filepath = _prepare_requirements_file(
                                            dirpath_root    = dirpath_root,
                                            dirpath_cfgpack = dirpath_cfgpack,
                                            id_phase        = id_phase,
                                            list_item       = list_item,
                                            id_std          = 'pep517')
                case _:
                    raise ValueError(
                        f'Unknown configuration method ({id_method}).')

            assert filepath is not None
            map_map_filepath[id_phase][id_method] = filepath

    return map_map_filepath


# -----------------------------------------------------------------------------
def _dirpath_cfgpack(dirpath_root, id_env):
    """
    Return the directory path of the temporary cfgpack for the specified env.

    """

    return os.path.join(dirpath_root, 'a4_tmp', 'cfgpack', id_env)


# -----------------------------------------------------------------------------
def _prepare_shell_script(dirpath_root, dirpath_cfgpack, id_phase, list_item):
    """
    Create a shell script for the specified list of configuration items.

    """

    filename_script = f'configure_{id_phase:02d}.sh'
    filepath_script = os.path.join(dirpath_cfgpack, filename_script)
    with open(filepath_script, 'wt') as file_script:
        print('#!/usr/bin/env bash', file = file_script)
        print('set -o errexit',      file = file_script)
        print('set -o nounset',      file = file_script)
        print('set -o pipefail',     file = file_script)
        for item in list_item:
            _prepare_shell_script_line_item(dirpath_root, item, file_script)
        print('exit 0', file = file_script)
    os.chmod(filepath_script, 0o755)
    return filepath_script


# -----------------------------------------------------------------------------
def _prepare_shell_script_line_item(dirpath_root, item, file_script):
    """
    Write a single configuration item to the shell script.

    """

    for str_spec_lineitem in item['spec']:
        if '{dirpath_root}' in str_spec_lineitem:
            str_spec_lineitem = str_spec_lineitem.format(
                                                dirpath_root = dirpath_root)
        print(str_spec_lineitem, file = file_script)


# -----------------------------------------------------------------------------
def _prepare_requirements_file(dirpath_root,
                             dirpath_cfgpack,
                             id_phase,
                             list_item,
                             id_std = 'legacy'):
    """
    Create a requirements file for the specified list of configuration items.

    """

    filename_reqs = f'requirements_{id_std}_{id_phase:02d}.txt'
    filepath_reqs = os.path.join(dirpath_cfgpack, filename_reqs)
    with open(filepath_reqs, 'wt') as file_reqs:
        for item in list_item:
            _prepare_requirements_file_line_item(dirpath_root, item, file_reqs)
    return filepath_reqs


# -----------------------------------------------------------------------------
def _prepare_requirements_file_line_item(dirpath_root, item, file_reqs):
    """
    Write a single lines to the requirements file.

    """

    id_type = item['type']
    if id_type in {'legacy-editable', 'pep517-editable'}:
        dirpath_dep = os.path.join(dirpath_root, item['relpath'])
        print(f'-e {dirpath_dep}', file = file_reqs)
    elif id_type in {'legacy-git', 'pep517-git'}:
        dirpath_dep = _ensure_cloned_fron_github(
                                            url_remote   = item['remote'],
                                            tag          = item['tag'],
                                            dirpath_root = dirpath_root)
        print(f'-e {dirpath_dep}', file = file_reqs)
    elif id_type in {'legacy-pip', 'pep517-pip'}:
        print(item['spec'], file = file_reqs)
    else:
        raise ValueError(f'Unknown envspec item type: {id_type}')


# -----------------------------------------------------------------------------
def _ensure_cloned_fron_github(url_remote, tag, dirpath_root):
    """
    Ensure that specified github repository is cloned to local storage.

    """

    (_, user_and_path) = url_remote.split(':')
    (user, repo_path)  = user_and_path.split('/', maxsplit = 1)
    (repo_name, _)     = repo_path.rsplit('.', maxsplit = 1)
    dirpath_env        = os.path.join(dirpath_root, 'a0_env', 'src')
    dirpath_dep        = os.path.join(dirpath_env, user, repo_name)
    is_already_cloned  = os.path.exists(dirpath_dep)
    list_cmd_clone     = ['git', 'clone', url_remote, dirpath_dep]
    str_cmd_clone      = ' '.join(list_cmd_clone)
    list_cmd_fetch     = ['git', 'fetch']
    str_cmd_fetch      = ' '.join(list_cmd_fetch)
    list_cmd_checkout  = ['git', 'checkout', tag]
    str_cmd_checkout   = ' '.join(list_cmd_checkout)

    if not is_already_cloned:
        os.makedirs(dirpath_dep)
        print(f'Cloning repository: {str_cmd_clone}')
        subprocess.run(list_cmd_clone)

    print(f'Fetching repository: {str_cmd_fetch}')
    subprocess.run(list_cmd_fetch, cwd = dirpath_dep)

    print(f'Checking out version: {str_cmd_checkout} in {dirpath_dep}')
    subprocess.run(list_cmd_checkout, cwd = dirpath_dep)

    return dirpath_dep


# -----------------------------------------------------------------------------
def _apply_cfgpack(dirpath_root, id_env, map_map_filepath):
    """
    Configure the environment using the specified configuration package.

    """

    dirpath_env        = _dirpath_env(dirpath_root, id_env)
    filepath_activate  = os.path.join(dirpath_env, 'bin', 'activate')
    activate           = f'. {filepath_activate}'
    filepath_pip3      = os.path.join(dirpath_env, 'bin', 'pip3')
    pip_legacy         = f'{filepath_pip3} install -r'
    pip_pep517         = f'{filepath_pip3} install --use-pep517 -r'

    # Install requirements items one phase at
    # a time, in order of ascending id_phase.
    #
    print('=' * 80)
    print(f'Configuring environment: {id_env}')

    for (id_phase, map_filepath) in sorted(map_map_filepath.items()):

        print('')
        print('')
        print(f'Configuration phase: {id_phase}')

        for (id_method, filepath) in sorted(map_filepath.items()):

            match id_method:
                case 'cfg-script-shell':
                    command = f'{activate} && {filepath}'
                case 'cfg-pip-legacy':
                    command = f'{activate} && {pip_legacy} {filepath}'
                case 'cfg-pip-pep517':
                    command = f'{activate} && {pip_pep517} {filepath}'
                case _:
                    raise ValueError(
                        f'Unknown configuration method ({id_method}).')

            print('-' * 80)
            print(f'{command}')
            print('')
            result = subprocess.run(command,
                                    shell          = True,
                                    check          = False,
                                    capture_output = False,
                                    text           = True)
            if result.returncode != 0:
                pass
                # raise ValueError(f'Configuration phase {id_phase} failed.')


# -----------------------------------------------------------------------------
def _delete_virtualenv(dirpath_root, id_env):
    """
    Delete the virtual environment so it can be recreated.

    """

    print(f'Deleting environment: {id_env}')
    dirpath_env     = _dirpath_env(dirpath_root, id_env)
    shutil.rmtree(dirpath_env)


