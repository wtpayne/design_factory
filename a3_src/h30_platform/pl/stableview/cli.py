#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---

title:
    "Stableview GUI platform command line interface."

description:
    "This script is used to launch a stableview
    user interface."

id:
    "fac2efd1-a12f-4726-8a19-3410c306dfd1"

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


import click

import pl.stableview


# -----------------------------------------------------------------------------
@click.command()
@click.version_option(version = pl.stableview.__version__)
@click.argument(
    'path_cfg',
    required = False,
    default  = None,
    type     = click.STRING,
    nargs    = -1)
def main(path_cfg):
    """
    Run the main view of the configured GUI.

    """

    pl.stableview.main(path_cfg, 'main')


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.argv.pop(0)
    main(prog_name = sys.argv[0])
