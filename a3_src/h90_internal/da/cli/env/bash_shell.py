# -*- coding: utf-8 -*-
"""
---

title:
    "Interactive bash shell command module."

description:
    "This module provides an interactive bash
    shell in a terminal emulator."

id:
    "35f6c22d-bea1-4415-b0c5-9635e1f43e68"

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

...
"""


import os
import os.path


# -----------------------------------------------------------------------------
def run():
    """
    Run an interactive bash shell in a pseudoterminal.

    """
    import prompt_toolkit.application
    import prompt_toolkit.layout
    import ptterm

    # -----------------------------------------------------------------------------
    def _done():
        """
        Exit the application when the terminal emulator is done.

        """
        application.exit()

    # -----------------------------------------------------------------------------
    def _before_exec():
        """
        Setup environment variables.

        """
        pass

    relfilepath_self = __file__ if __file__ else argv[0]
    filepath_self    = os.path.realpath(relfilepath_self)
    dirpath_self     = os.path.dirname(filepath_self)
    filename_init    = 'bash_init.sh'
    filepath_init    = os.path.join(dirpath_self, filename_init)
    command          = ["/usr/bin/env", "bash", "--init-file", filepath_init]
    terminal         = ptterm.Terminal(command          = command,
                                       done_callback    = _done,
                                       before_exec_func = _before_exec)
    app_layout       = prompt_toolkit.layout.Layout(container = terminal)
    application      = prompt_toolkit.application.Application(
                                                    layout      = app_layout,
                                                    full_screen = True)
    application.run()
