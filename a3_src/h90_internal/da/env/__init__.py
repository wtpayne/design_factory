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
import datetime
import json
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
        do_update(dirpath_root, id_env)


# -----------------------------------------------------------------------------
def do_update(dirpath_root, id_env):
    """
    Update the specified environment with the latest envspec.

    This public function is used by the top level
    'da' script to update the environment
    e000_design_automation_core if required.

    By setting the last-modified time of the
    envspec file to be one second prior to the
    update, we ensure that once the update
    process is completed, the envspec file will
    have a last-modified timestamp that is
    guaranteed to be older than any of the last
    modified timestamps that are generated by any
    of the subsequent update operations.

    This eliminates the possibility of an invalid
    or corrupt last-modified timestamp on the
    envspec file causing the update process to
    run multiple times, making diagnosis of such
    issues easier.

    """
    filepath_envspec = _filepath_envspec(
                                dirpath_root = dirpath_root,
                                id_env       = id_env)

    filepath_reqs    = _create_requirements_file(
                                dirpath_root = dirpath_root,
                                id_env       = id_env,
                                envspec      = _load_envspec(filepath_envspec))

    _touch(
        filepath   = filepath_envspec,
        delta_secs = -1) # Set mtime to one second in the past.

    _install_requirements(
        dirpath_root  = dirpath_root,
        id_env        = id_env,
        filepath_reqs = filepath_reqs)

    # dirpath_env      = _dirpath_env(dirpath_root, id_env)
    # dirpath_venv_pkg = _dirpath_venv_pkg(dirpath_env)
    # dirpath_venv_whl = _dirpath_venv_whl(dirpath_env)
    # _touch(filepath  = dirpath_venv_pkg)
    # _touch(filepath  = dirpath_venv_whl)

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
def _create_requirements_file(dirpath_root, id_env, envspec):
    """
    Return temporary requirements.txt filepath after writing envspec data to it.

    """

    filepath = _filepath_requirements(dirpath_root, id_env)
    dirpath  = os.path.dirname(filepath)
    if not os.path.exists(dirpath):
       os.makedirs(dirpath)

    with open(filepath, 'wt') as file_reqs:
        _write = lambda msg: print(msg, file = file_reqs)
        for item in envspec['list_item']:
            _process_requirement_item(dirpath_root, item, _write)
        _write('')

    return filepath


# -----------------------------------------------------------------------------
def _filepath_requirements(dirpath_root, id_env):
    """
    Return the path of the temporary requirements file for the specified env.

    """
    return os.path.join(dirpath_root, 'a4_tmp', id_env, 'requirements.txt')


# -----------------------------------------------------------------------------
def _process_requirement_item(dirpath_root, item, _write):
    """
    Write a single lines to the requirements file.

    """
    if isinstance(item, str):

        _write(item)

    elif item['type'] == 'pep508':

        _write(item['spec'])

    elif item['type'] == 'local':


        _write('-e {dirpath_dep}'.format(
                    dirpath_dep = os.path.join(dirpath_root, item['relpath'])))

    elif item['type'] == 'github':

        _write('-e {dirpath_dep}'.format(
                    dirpath_dep = _ensure_cloned_fron_github(
                                            url_remote   = item['remote'],
                                            tag          = item['tag'],
                                            dirpath_root = dirpath_root)))


# -----------------------------------------------------------------------------
def _ensure_cloned_fron_github(url_remote, tag, dirpath_root):
    """
    Ensure that specified github repository is cloned to local storage.

    """
    (_, user_and_path) = url_remote.split(':')
    (user, repo_path)  = user_and_path.split('/', maxsplit = 1)
    (repo_name, _)     = repo_path.rsplit('.', maxsplit = 1)
    dirpath_env        = os.path.join(dirpath_root, 'a0_env/src')
    dirpath_dep        = os.path.join(dirpath_env, user, repo_name)
    is_already_cloned  = os.path.exists(dirpath_dep)

    if not is_already_cloned:
        os.makedirs(dirpath_dep)
        subprocess.run(['git', 'clone', url_remote, dirpath_dep])

    subprocess.run(['git', 'checkout', tag], cwd = dirpath_dep)

    return dirpath_dep


# -----------------------------------------------------------------------------
def _load_envspec(filepath_envspec):
    """
    Return the envspec data for the specified environment id.

    """
    with open(filepath_envspec, 'rt') as file:
        return json.load(file)


# -----------------------------------------------------------------------------
def _touch(filepath, delta_secs = 0):
    """
    Set last-accessed and last-modified times of filepath.

    """
    timestamp_now  = time.time()
    datetime_now   = datetime.datetime.fromtimestamp(timestamp_now)
    datetime_mod   = datetime_now + datetime.timedelta(seconds = delta_secs)
    timestamp_mod  = datetime_mod.timestamp()
    os.utime(filepath, (timestamp_mod, timestamp_mod))


# -----------------------------------------------------------------------------
def _install_requirements(dirpath_root, id_env, filepath_reqs):
    """
    Install the dependencies specified in the given requirements file.

    We also always ensure that the wheel package
    is installed first, as some of the other
    packages require it before they can be
    installed.

    """
    dirpath_env        = _dirpath_env(dirpath_root, id_env)
    filepath_activate  = os.path.join(dirpath_env, 'bin', 'activate')
    filepath_pip       = os.path.join(dirpath_env, 'bin', 'pip3')

    cmd_activate       = '. {act}'.format(
                                    act = filepath_activate)

    cmd_pip_self       = '{pip} install pip==22.3.1'.format(
                                    pip = filepath_pip)

    cmd_pip_wheel      = '{pip} install wheel==0.38.4'.format(
                                    pip = filepath_pip)

    cmd_pip_setuptools = '{pip} install setuptools==66.1.1'.format(
                                    pip = filepath_pip)

    cmd_pip_reqs       = '{pip} install -r {reqs}'.format(
                                    pip  = filepath_pip,
                                    reqs = filepath_reqs)

    cmd_full           = '{act} && {self} && {whl} && {stls} && {reqs}'.format(
                                    act  = cmd_activate,
                                    self = cmd_pip_self,
                                    whl  = cmd_pip_wheel,
                                    stls = cmd_pip_setuptools,
                                    reqs = cmd_pip_reqs)

    subprocess.run(cmd_full, shell = True)
