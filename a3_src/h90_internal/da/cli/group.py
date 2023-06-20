# -*- coding: utf-8 -*-
"""
---

title:
    "Design automation command line interface utilities module."

description:
    "The design automation command line interface
    utilities module is intended to support the
    design automation command line command module
    with utility functions and enhancements to
    the click library."

id:
    "3ffd8a9a-bb81-45cc-914d-8c63e19c95e2"

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


import click


# -----------------------------------------------------------------------------
def path():
    """
    """


# =============================================================================
class Ordered(click.Group):
    """
    A click command group enabling control over the ordering of commands.

    The help text for a click command group normally
    lists each command in arbitrary order.

    This subclass ensures that the help text for
    the corresponding click command group will
    appear in the same order in which they were
    added. I.e. the same order that they are
    defined in the source file.

    """

    # -------------------------------------------------------------------------
    def __init__(self, name = None, commands = None, **attrs):
        """
        Return an OrderedGroup instance.

        """
        super().__init__(name, commands, **attrs)

        # From Python 3.5 dict() is order preserving, so
        # we simply replace the default commands container
        # (a set) with a normal python dict.
        #
        self.commands = commands or dict()

    # -------------------------------------------------------------------------
    def list_commands(self, ctx):
        """
        Return an ordered list of the commands in the group.

        """
        return self.commands
