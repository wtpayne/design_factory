# -*- coding: utf-8 -*-
"""
---

title:
    "HTML markup generator module."

description:
    "This Python module is designed to
    generate HTML markup."

id:
    "d40ca4ec-48e3-4091-ad85-abacd25ad1f4"

type:
    dt002_python_package

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

...
"""

"""
Markup generator library.

"""


import types

import dominate
import dominate.dom_tag
import dominate.tags
import dominate.svg
import dominate.util


html_tag = dominate.tags.html_tag  # Export html_tag class


# -----------------------------------------------------------------------------
def ns_html() -> types.SimpleNamespace:
    """
    Return a namespace containing html tag classes.

    """

    ns_tag = types.SimpleNamespace()
    for (key, value) in _iter_dom_tag(module     = dominate.tags,
                                      tup_ignore = ('dom_tag', 'html_tag')):
        setattr(ns_tag, key, value)

    ns_tag.document = dominate.document
    ns_tag.raw      = dominate.util.raw
    return ns_tag


# -----------------------------------------------------------------------------
def ns_svg() -> types.SimpleNamespace:
    """
    Return a namespace containing svg tag classes.

    """

    ns_tag = types.SimpleNamespace()
    for (key, value) in _iter_dom_tag(
                            module     = dominate.svg,
                            tup_ignore = ('dom_tag', 'html_tag', 'svg_tag')):
        setattr(ns_tag, key, value)
    return ns_tag


# -----------------------------------------------------------------------------
def _iter_dom_tag(module, tup_ignore):
    """
    Yield name_class, type_class for each dom_tag in the specified module.

    """
    for (key, value) in module.__dict__.items():
        if (     isinstance(value, type)
             and issubclass(value, dominate.dom_tag.dom_tag)
             and (key not in tup_ignore)):
            yield (key, value)


# -----------------------------------------------------------------------------
def _monkeypatch_dominate(dom_tag):
    """
    Monkeypatch the dom_tag class with a new clean_pair function.

    """
    # Prevent monkey patching twice.
    if hasattr(dom_tag, '_clean_pair_orig'):
        return

    # Keep a reference to the old clean_pair function.
    setattr(dom_tag, '_clean_pair_orig', dom_tag.clean_pair)

    # -------------------------------------------------------------------------
    def _clean_pair_patch(cls, attribute, value):
        """
        Return a clean attribute value pair.

        This is used to patch the dom_tag clean_pair
        function to add syntactic sugar for helping
        with class-based frameworks like tailwind.

        """
        (attribute, value) = cls._clean_pair_orig(attribute, value)
        if attribute in ('class', 'data-script'):
            if isinstance(value, tuple) or isinstance(value, list):
                value = ' '.join(value)
        return (attribute, value)

    # Patch in the new function.
    dom_tag.clean_pair = classmethod(_clean_pair_patch)


_monkeypatch_dominate(dom_tag = dominate.dom_tag.dom_tag)