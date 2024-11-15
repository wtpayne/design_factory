# -*- coding: utf-8 -*-
"""
---

title:
    "Web resource rendering."

description:
    "Web resource rendering functionality."

id:
    "af10b12b-72ef-4052-a249-3456f837de99"

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

import fl.ui.web.markup
import fl.ui.web.util


html = fl.ui.web.markup.ns_html()


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine to assemble web resources from a graph of fragments.

    data_hx_get    - Issues a GET request to the given URL
    data_hx_post   - Issues a POST request to the given URL
    data_hx_put    - Issues a PUT request to the given URL
    data_hx_patch  - Issues a PATCH request to the given URL
    data_hx_delete - Issues a DELETE request to the given URL

    data_hx_trigger - Can be


    """

    signal = None

    outputs['res']['ena']  = False
    outputs['res']['list'] = []

    while True:

        inputs = yield (outputs, signal)
        if not inputs['ctrl']['ena']:
            continue

        if not inputs['com']['ena']:
            continue

        # Index the components by id.
        #
        map_page = collections.defaultdict(dict)
        for com in inputs['com']['list']:
            map_page[com.id_page][com.id_com] = com

        map_res = fl.ui.web.util.ResMap()
        for (id_page, map_com) in map_page.items():

            
            # Add the list of component ids to 
            # the SSE topic for the page.
            #
            id_topic = id_page + '_topic'
            map_res.sse(**{id_topic: sorted(map_com.keys())})

            # Add the component html to the resource map.
            # 
            for (id_com, com) in map_com.items():
                map_res.htm(**{id_com: map_com[id_com].markup})

            # Add the page html to the resource map.
            #
            map_res.htm(**{id_page: _page(id_topic, map_com)})

        outputs['res']['ena']  = True
        outputs['res']['list'] = [dict(map_res)]


# -----------------------------------------------------------------------------
def _add_components_to_topic(map_res, id_topic, list_com):
    """
    Add the components to the SSE topic.

    """

    list_id_component = [com.id_com for com in list_com]
    map_res.sse(**{id_topic: list_id_component})


# -----------------------------------------------------------------------------
def _page(id_topic, map_com):
    """
    Add the page resource to the resource map.

    """

    page = html.document(title = 'Macro')

    with page.head:
        html.script(type  = 'text/javascript',
                    src   = 'htmx.js')
        html.script(type  = 'text/javascript',
                    src   = 'sse.js')

    with page.body:
        with html.div(data_hx_ext      = 'sse',
                      data_sse_connect = f'/{id_topic}'):
            for com in sorted(map_com.values()):
                if com.is_onpage:
                    html.raw(com.markup)

    return page.render()

     
