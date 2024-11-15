# -*- coding: utf-8 -*-
"""
---

title:
    "Web utility functions."

description:
    "Web utility functions."

id:
    "78f1e1fe-9f03-47bf-9cfe-2aa955c138fe"

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


import base64
import collections
import os
import sys
import uuid

import dominate


# -----------------------------------------------------------------------------
def urlsafe_uid(prefix = 'r', num_chars = None):
    """
    Return a new unique url-safe (base16 encoded) GUID.

    """

    uid = prefix + base64.b32encode(uuid.uuid4().bytes).decode('utf-8')
    if num_chars is not None:
        uid = uid[:num_chars]
    return uid.lower()


# =============================================================================
class ResMap(collections.abc.MutableMapping):
    """
    Class representing a mapping of id_resource to (media_type, content) pairs.

    """

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the ResourceMap class.

        """

        self._map = dict()

    # -------------------------------------------------------------------------
    def htm(self, default = None, **kwargs):
        """
        Add a set of HTML resources.

        """

        self.add(media_type = 'text/html',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def css(self, default = None, **kwargs):
        """
        Add a set of CSS resources.

        """

        map_routes = dict()
        for (key, value) in kwargs.items():
            if isinstance(value, dict):
                map_routes[key] = str(CSS(value))
            else:
                map_routes[key] = value

        self.add(media_type = 'text/css',
                 default    = default,
                 **map_routes)

    # -------------------------------------------------------------------------
    def js(self, default = None, **kwargs):
        """
        Add a set of Javascript resources.

        """

        self.add(media_type = 'text/javascript',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def json(self, default = None, **kwargs):
        """
        Add a set of JSON resources.

        """

        self.add(media_type = 'application/json',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def svg(self, default = None, **kwargs):
        """
        Add a set of SVG resources.

        """

        self.add(media_type = 'text/svg',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def bmp(self, default = None, **kwargs):
        """
        Add a set of MS windows, OS/2 bitmap image resources.

        """

        self.add(media_type = 'image/bmp',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def dib(self, default = None, **kwargs):
        """
        Add a set of device independent bitmap image resources.

        """

        self.add(media_type = 'image/dib',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def jpeg(self, default = None, **kwargs):
        """
        Add a set of JPEG image resources.

        """

        self.add(media_type = 'image/jpeg',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def jpeg2k(self, default = None, **kwargs):
        """
        Add a set of JPEG 2000 image resources.

        """

        self.add(media_type = 'image/jpm',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def png(self, default = None, **kwargs):
        """
        Add a set of portable network graphics format image resources.

        """

        self.add(media_type = 'image/png',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def webp(self, default = None, **kwargs):
        """
        Add a set of WebP image resources.

        """

        self.add(media_type = 'image/webp',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def pbm(self, default = None, **kwargs):
        """
        Add a set of portable bit map image resources.

        """

        self.add(media_type = 'image/x-ortable-bitmap',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def tiff(self, default = None, **kwargs):
        """
        Add a set of tagged image file format image resources.

        """

        self.add(media_type = 'image/tiff',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def hdr(self, default = None, **kwargs):
        """
        Add a set of HDR image resources.

        """

        self.add(media_type = 'image/vnd.radiance',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def woff(self, default = None, **kwargs):
        """
        Add a set of woff font resources.

        """

        self.add(media_type = 'font/woff',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def woff2(self, default = None, **kwargs):
        """
        Add a set of woff2 font resources.

        """

        self.add(media_type = 'font/woff2',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def ttf(self, default = None, **kwargs):
        """
        Add a set of ttf font resources.

        """

        self.add(media_type = 'application/octet-stream',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def callback(self, default = None, **kwargs):
        """
        Add a set of asynchronous callbacks that return resources.

        """

        self.add(media_type = 'callback',
                 default    = default,
                 **kwargs)

    # -------------------------------------------------------------------------
    def topic(self, default = None, **kwargs):
        """
        Add an SSE topic.

        """

        self.sse(default, **kwargs)

    # -------------------------------------------------------------------------
    def sse(self, default = None, **kwargs):
        """
        Add an SSE topic.

        """

        map_routes = dict()
        for (key, value) in kwargs.items():
            map_routes[key] = ' '.join(value)

        self.add(media_type = 'topic',
                 default    = default,
                 **map_routes)

    # -------------------------------------------------------------------------
    def add(self, media_type, default = None, **kwargs):
        """
        Add a set of routes with the specified media_type.

        """

        if default is not None and 'default' not in kwargs:
            kwargs['default'] = default

        for (route, obj) in kwargs.items():
            self._map[route] = (media_type, obj)

            # Mark alternate routes as 'used' so
            # that they don't get added to any
            # open dominate context managers.
            #
            if route != default and isinstance(obj, dominate.dom_tag.dom_tag):
                thread_hash = dominate.dom_tag._get_thread_context()
                ctx         = obj._with_contexts[thread_hash]
                if ctx and ctx[-1]:
                    ctx[-1].used.add(obj)

    # -------------------------------------------------------------------------
    def __iter__(self):
        """
        Yield (key, content) for each route in the map.

        """
        for (route, (media_type, obj)) in self._map.items():

            if isinstance(obj, dominate.dom_tag.dom_tag):
                obj = obj.render()

            yield (route, (media_type, obj))


    # -------------------------------------------------------------------------
    def __bool__(self):
        """
        Return true iff there are items in the map.

        """
        return len(self._map) > 0


    # -------------------------------------------------------------------------
    def keys(self):
        """
        Return all the route keys in the map.

        """
        return self._map.keys()

    # -------------------------------------------------------------------------
    def __len__(self):
        """
        Return the number of routes in the map.

        """
        return len(self._map)

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Return the content corresponding to the specified route key.

        """
        (media_type, obj) = self._map[key]
        if isinstance(obj, dominate.dom_tag.dom_tag):
            obj = obj.render()
        return (media_type, obj)

    # -------------------------------------------------------------------------
    def __setitem__(self, key, value):
        """
        Set the content corresponding to the specified route key.

        """
        self._map[key] = value

    # -------------------------------------------------------------------------
    def __delitem__(self, key):
        """
        Delete the content corresponding to the specified route key.

        """
        del self._map[key]


    # -------------------------------------------------------------------------
    def update(self, other):
        """
        Update the ResMap from the specified other ResMap

        """
        self._map.update(other._map)


# -----------------------------------------------------------------------------
def cla(*args):
    """
    Return a dict suitable for setting tailwind classes.

    """
    return {'_class': ' '.join(args)}


# =============================================================================
class CSS():
    """
    CSS rendering class.

    """

    # -------------------------------------------------------------------------
    def __init__(self, map_ruleset = None):
        """
        Return an instantiated css.Renderer object.

        """
        self._list_rules = []
        if map_ruleset is not None:
            self.add(map_ruleset)

    # -------------------------------------------------------------------------
    def add(self, map_ruleset):
        """
        Add a collection of rulesets to the css.

        """
        for (selector, declaration) in map_ruleset.items():
            self.add_ruleset(selector, declaration)

    # -------------------------------------------------------------------------
    def add_ruleset(self, selector, declaration):
        """
        Add a ruleset to the css.

        """
        self._list_rules.append((selector, declaration))

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Render the CSS document.

        """
        text = ''
        for rule in self._list_rules:

            (selector, declaration) = rule

            text += '{selector} {{\n'.format(selector = selector)

            # Align values using max-property-name-length.
            len_max = 0
            for prop in declaration.keys():
                len_prop = len(prop)
                if len_prop > len_max:
                    len_max = len_prop
            len_max = max(20, len_max)

            for (prop, value) in declaration.items():
                fmt       = '{indent}{prop}:{align}{value};\n'
                indent    = ' ' * 2
                len_delta = len_max - len(prop)
                len_align = len_delta + 2
                align     = ' ' * len_align
                text     += fmt.format(indent = indent,
                                       prop   = prop,
                                       align  = align,
                                       value  = value)
            text += '}\n\n'

        return text


# -----------------------------------------------------------------------------
def _load_txt(relpath_file):
    """
    Return the content of the specified text file.

    """
    return _load_static(relpath_file, is_binary = False)


# -----------------------------------------------------------------------------
def _load_bin(relpath_file):
    """
    Return the content of the specified binary file.

    """
    return _load_static(relpath_file, is_binary = True)


# -----------------------------------------------------------------------------
def _load_static(relpath_file, is_binary = False):
    """
    Return the content of the specified file.

    """
    relpath_self   = __file__ if __file__ else sys.argv[0]
    dirpath_self   = os.path.dirname(os.path.realpath(relpath_self))
    dirpath_static = os.path.join(dirpath_self, 'static')
    filepath       = os.path.join(dirpath_static, relpath_file)

    if is_binary:
        flags = 'rb'
    else:
        flags = 'r'

    with open(filepath, flags) as file:
        return file.read()


