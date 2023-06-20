# -*- coding: utf-8 -*-
"""
---

title:
    "Rules package."

description:
    "This package contains various rules."

id:
    "cc3e3e2f-a740-4ff5-bec6-9217b9624b37"

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


# -----------------------------------------------------------------------------
def always():
    """
    Return an always-true indicator function.

    """

    def _indicator(cmd):
        """
        Return True.

        """
        return True
    return _indicator


# -----------------------------------------------------------------------------
def never():
    """
    Return a never-true indicator function.

    """

    def _indicator(cmd):
        """
        Return False.

        """
        return False
    return _indicator


# -----------------------------------------------------------------------------
def is_not(fcn):
    """
    Return indicator that negates the specified indicator.

    """

    def _indicator(cmd):
        """
        Return the negation of the specified indicator.

        """
        return not fcn(cmd)
    return _indicator


# -----------------------------------------------------------------------------
def is_root_in(tup_path_root):
    """
    Return indicator that checks cmd.path is rooted in the specified location.

    """

    def _indicator(cmd):
        """
        Return True iff cmd.path is rooted in the specified location.

        """
        return cmd.path[:len(tup_path_root)] == tup_path_root
    return _indicator


# -----------------------------------------------------------------------------
def is_leaf_at(tup_path_leaf):
    """
    Return indicator that checks cmd.path leafed at the specified location.

    """

    def _indicator(cmd):
        """
        Return True iff cmd.path is leafed at the specified location.

        """
        return cmd.path[-len(tup_path_leaf):] == tup_path_leaf
    return _indicator


# -----------------------------------------------------------------------------
def is_operation(operation):
    """
    Return indicator that checks cmd.operation.

    """

    def _indicator(cmd):
        """
        Return True iff cmd.path is leafed at the specified location.

        """
        return cmd.operation == operation
    return _indicator
