# -*- coding: utf-8 -*-
"""
---

title:
    "Hyperview web resource rendering."

description:
    "Web resource rendering functionality for
    the hyperview UI framework."

id:
    "915fc204-39e8-4d00-a9b6-032769b3d169"

type:
    dt004_python_stableflow_edict_component

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


import collections

import sqlitedict

import fl.ui.web.markup
import fl.ui.web.util


html = fl.ui.web.markup.ns_html()


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine to assemble web resources from a graph of fragments.

    """

    signal = None

    outputs['res']['ena']  = False
    outputs['res']['list'] = []

    map_com_cache = dict()

    while True:

        inputs = yield (outputs, signal)
        if not inputs['ctrl']['ena']:
            continue

        # Pick up any new components to render.
        #
        list_com = []
        for (key, value) in inputs.items():
            if key not in ('ctrl',) and value['ena']:
                list_com.extend(value['list'])
        if not list_com:
            continue

        # The cache enables us to generate
        # components continuously as needed.
        #
        # They get stored here so we can
        # recompute the site structure
        # when components change.
        #
        for com in list_com:
            map_com_cache[com.id_com] = com

        # The site structure is defined by
        # the parent-child (containment)
        # relationships between components.
        #
        (set_id_page,
         set_id_orphan,
         map_list_child) = _determine_site_structure(map_com_cache)
        set_id_root      = set_id_page.union(set_id_orphan)

        # Detect looping references in the
        # component containment hierarchy
        # (This is disallowed)
        #
        try:
            _detect_loop(set_id_root, map_list_child)
        except ValueError as exc:
            print('LOOP DETECTED.')
            continue

        # Generate markup for all of our
        # components.
        #
        map_res = fl.ui.web.util.ResMap()
        map_res = _render_resources(set_id_root,
                                    map_com_cache,
                                    map_list_child,
                                    map_res)

        for id_page in sorted(set_id_page):

            # Add the list of component ids to 
            # the SSE topic for the page.
            #
            id_topic = id_page + '_topic'
            map_res  = _add_sse_topic(map_res,
                                      map_list_child, 
                                      map_com_cache,
                                      id_page,
                                      id_topic)

            # Generate page markup.
            #
            content = _render_page(id_page, id_topic, map_list_child)
            map_res.htm(**{id_page: content})

        outputs['res']['ena']  = True
        outputs['res']['list'] = [dict(map_res)]


# -----------------------------------------------------------------------------
def _detect_loop(set_id_root, map_list_child):
    """
    Check for loops in the component tree.

    """

    set_id_visited = set()
    for id_root in set_id_root:
        _detect_loop_recursive(map_list_child, id_root, set_id_visited)


# -----------------------------------------------------------------------------
def _detect_loop_recursive(map_list_child, id_parent, set_id_visited):
    """
    Recursively render all the components in the specifiedtree.

    """

    for com in map_list_child[id_parent]:
        id_com = com.id_com
        if id_com in set_id_visited:
            raise ValueError(f'Loop detected: {id_parent} -> {id_com}')
        set_id_visited.add(id_com)
        _detect_loop_recursive(map_list_child, id_com, set_id_visited)


# -----------------------------------------------------------------------------
def _determine_site_structure(map_com_cache):
    """
    Return the set of page ids and the component map.

    The component map allows components to be
    looked up by the id of their parent container.

    """

    map_list_child = collections.defaultdict(list)
    set_id_com     = set()
    set_id_parent  = set()
    set_id_orphan  = set()
    for (id_com, com) in map_com_cache.items():

        if not com.is_valid:
            continue

        set_id_com.add(id_com)
        if not com.list_id_parent:
            set_id_orphan.add(id_com)
        else:
            set_id_parent.update(com.list_id_parent)
            for id_parent in com.list_id_parent:
                map_list_child[id_parent].append(com)

    set_id_page = set_id_parent.difference(set_id_com)
    return (set_id_page, set_id_orphan, map_list_child)


# -----------------------------------------------------------------------------
def _render_resources(set_id_root, map_com_cache, map_list_child, map_res):
    """
    Generate web resources for the specified component and all of its children.

    """

    for id_root in set_id_root:

        # id_root is a page.
        #
        if id_root not in map_com_cache:  
            id_page = id_root
            map_res = _render_recursive(map_list_child, id_page, map_res)

        # id_root is an orphan component.
        #
        else:
            id_com  = id_root
            com     = map_com_cache[id_com]
            map_res = _render_recursive(map_list_child, id_com, map_res)
            with com:
                for com_child in map_list_child[id_com]:
                    com.add_raw_string(com_child.render())
            map_res.add(media_type = com.media_type, **{id_com: com.render()})

    return map_res


# -----------------------------------------------------------------------------
def _render_recursive(map_list_child, id_parent, map_res):
    """
    Recursively render all the components in the specifiedtree.

    """

    try:
        for com in map_list_child[id_parent]:
            id_com  = com.id_com
            map_res = _render_recursive(map_list_child, id_com, map_res)
            with com:
                for com_child in map_list_child[id_com]:
                    com.add_raw_string(com_child.render())
            map_res.add(media_type = com.media_type, **{id_com: com.render()})
    except KeyError:
        pass
    return map_res


# -----------------------------------------------------------------------------
def _add_sse_topic(map_res, map_list_child, map_com_cache, id_page, id_topic):
    """
    Add SSE topic resources for the specified page.

    """

    set_id_com = _get_descendent_recursive(map_list_child, id_page)
    set_id_com.update(_get_orphan_components(map_com_cache, id_page))
    map_res.sse(**{id_topic: sorted(set_id_com)})
    return map_res


# -----------------------------------------------------------------------------
def _get_descendent_recursive(map_list_child, id_parent, set_id_com = None):
    """
    Recursively get the set of all descendents of the specified component.

    """

    if set_id_com is None:
        set_id_com = set()

    for com in map_list_child[id_parent]:
        id_com = com.id_com
        set_id_com.add(id_com)
        set_id_com = _get_descendent_recursive(
                                        map_list_child, id_com, set_id_com)
    return set_id_com


# -----------------------------------------------------------------------------
def _get_orphan_components(map_com_cache, id_page):
    """
    Return the set of orphan components for the specified page.

    """

    return (id_com for (id_com, com) in map_com_cache.items() 
                                            if id_page in com.list_id_page)


# -----------------------------------------------------------------------------
def _render_page(id_page, id_topic, map_list_child):
    """
    Return the page markup.

    """

    page = html.document(title = id_page)

    with page.head:
        html.script(type  = 'text/javascript',
                    src   = 'htmx.js')
        html.script(type  = 'text/javascript',
                    src   = 'sse.js')

    with page.body:
        with html.div(data_hx_ext      = 'sse',
                      data_sse_connect = f'/{id_topic}') as div:
            for com_child in map_list_child[id_page]:
                div.add_raw_string(com_child.render())

    return page.render()

