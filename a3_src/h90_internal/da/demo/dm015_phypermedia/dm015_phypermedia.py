# -*- coding: utf-8 -*-
"""
---

title:
    "dm015_phypermedia demo commands."

description:
    "This module defines commands for the
    dm015_phypermedia demonstration."

id:
    "2d2b8c9b-ee61-402e-ab31-6c6c2fb27435"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2024 William Payne"

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


import os.path
import sys


NAME_DEMO = 'phypermedia'


# -----------------------------------------------------------------------------
def start():
    """
    Start the dm015 phypermedia system.

    """

    import da.env.run
    import key

    tup_overrides = (

        'node.static.config.list.0.filepath',
        _filepath_static('htmx/v2.0.3/htmx.js'),

        'node.static.config.list.1.filepath',
        _filepath_static('htmx/v2.0.3/htmx.min.js'),

        'node.static.config.list.2.filepath',
        _filepath_static('htmx-ext-sse/v2.2.2/sse.js'),

        'node.static.config.list.3.filepath',
        _filepath_static('htmx-ext-sse/v2.2.2/sse.min.js'))

    sys.exit(da.env.run.stableflow_start(path_cfg      = _filepath_cfg(),
                                         tup_overrides = tup_overrides))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop the dm015 phypermedia system.

    """

    import da.env.run
    sys.exit(da.env.run.stableflow_stop(path_cfg = _filepath_cfg()))


# -----------------------------------------------------------------------------
def _filepath_static(relpath_file):
    """
    Return the filepath to a static HTMX resource.

    """

    return _wspath('static', relpath_file)


# -----------------------------------------------------------------------------
def _filepath_cfg():
    """
    Return the filepath to the backend server stableflow configuration file.

    """

    return _wspath(f'{NAME_DEMO}.stableflow.cfg.yaml')



# -----------------------------------------------------------------------------
def _filepath_cache(id_node):
    """
    Return the filepath to the cache database.

    """

    return _wspath(f'{id_node}.cache.sqlite', is_tmp = True)


# -----------------------------------------------------------------------------
def _wspath(*args, is_tmp = False):
    """
    Return a path in the demo R&D workspace.

    """

    import da.env

    if is_tmp:
        process_area = 'a4_tmp'
    else:
        process_area = 'a3_src'

    dirpath_macro = da.env.path(process_area = process_area,
                                control_tier = 'h80_research',
                                relpath      = f't000_wtp/{NAME_DEMO}')

    return os.path.join(dirpath_macro, *args)

