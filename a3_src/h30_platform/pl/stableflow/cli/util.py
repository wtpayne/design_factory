# -*- coding: utf-8 -*-
"""
Module of utility functions related to the stableflow command line interface.

"""


import click


# =============================================================================
class OrderedGroup(click.Group):
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
