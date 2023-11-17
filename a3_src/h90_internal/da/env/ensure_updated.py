#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---

title:
    "Virtual environment update script."

description:
    "This script is used to create and update
    virtual environments of various types."

id:
    "0a877789-1627-4a93-bb0b-e43ee1dbec6e"

type:
    dt001_python_script

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


import sys

import da.env


# -----------------------------------------------------------------------------
def main():
    """
    Ensure the specified environment is up to date with the latest envspec.

    """

    da.env.do_ensure_updated(dirpath_root = sys.argv[1],
                             id_env       = sys.argv[2])


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
