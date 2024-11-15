# -*- coding: utf-8 -*-
"""
---

title:
    "Macro UI compoenent generation."

description:
    "Macro UI compoenent generation functionality."

id:
    "81c6f602-ca54-46b0-8ed0-ad911d1bd286"

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


import typing

import pydantic

import fl.ui.web.markup
import fl.ui.web.util


html = fl.ui.web.markup.ns_html()
svg  = fl.ui.web.markup.ns_svg()


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine to generate UI components.

    """

    signal = None

    for key in outputs:
        outputs[key]['ena']  = False
        outputs[key]['list'] = list()

    while True:

        inputs = yield (outputs, signal)
        if not inputs['ctrl']['ena']:
            continue

        list_component = [component for component in _gencom()]
        if not list_component:
            continue

        for key in outputs:
            outputs[key]['ena']  = True
            outputs[key]['list'].clear()
            outputs[key]['list'].extend(list_component)


# =============================================================================
class ComData(pydantic.BaseModel):
    """
    UI component data.

    Contains markup and metadata for the component.

    """

    id_com:         str
    list_id_parent: list[str] = []
    is_valid:       bool      = True   # set to False to delete the component.
    is_dyn_sse:     bool      = False  # Is dynamic using SSE.
    media_type:     str       = 'text/html'


# =============================================================================
class Com(ComData):
    """
    UI component.

    """

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Construct a Com instance.

        """

        # Separate out kwargs for ComData
        # and kwargs for the html.div tag.
        #
        set_key_super = set(ComData.model_fields.keys())
        kwargs_super  = {k:v for k,v in kwargs.items() if k in set_key_super}
        super().__init__(**kwargs_super)

        for key in kwargs_super.keys():
            del kwargs[key]
        if 'id' in kwargs:
            raise RuntimeError('invalid kwarg "id" in Com ctor.')

        if self.is_dyn_sse:
            kwargs['data_sse_swap'] = f'{self.id_com}'
            kwargs['data_hx_swap']  = 'outerHTML'

        match self.media_type:
            case 'text/html':
                self._tag = html.div(*args, **kwargs, id = self.id_com)
            case _:
                raise ValueError(f'invalid media_type: {self.media_type}')

    # -------------------------------------------------------------------------
    def __enter__(self):
        """
        Enter the tag scope context.

        """

        self._tag.__enter__()
        return self

    # -------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the tag scope context.

        """

        self._tag.__exit__(exc_type, exc_value, traceback)

    # -------------------------------------------------------------------------
    def __lt__(self, other):
        """
        Less than comparison using id_com as the sort key.

        """

        return self.id_com < other.id_com

    # -------------------------------------------------------------------------
    def render(self) -> str:
        """
        Render the component.

        """

        return self._tag.render()
    
    # -------------------------------------------------------------------------
    def add_raw_string(self, str_content: str) -> None:
        """
        Add a raw string to the component.

        """

        return self._tag.add_raw_string(str_content)

    # -------------------------------------------------------------------------
    def model_dump(self):
        """
        Dump the component data as a dictionary.

        """

        return super().model_dump()


# -----------------------------------------------------------------------------
def _gencom() -> typing.Generator[Com, None, None]:
    """
    Yield components.

    data_hx_get     - Issues a GET request to the given URL
    data_hx_post    - Issues a POST request to the given URL
    data_hx_put     - Issues a PUT request to the given URL
    data_hx_patch   - Issues a PATCH request to the given URL
    data_hx_delete  - Issues a DELETE request to the given URL
    data_hx_trigger - Can be

    """

    with Com(id_com         = 'com_1',
             list_id_parent = ['app'],
             is_dyn_sse     = True) as com_1:

        html.div('[COMPONENT 01] - A', 
                 data_hx_trigger = 'click',
                 data_hx_target  = '#com_1',
                 data_hx_get     = '/com_2',
                 data_hx_swap    = 'outerHTML')
        yield com_1

    with Com(id_com         = 'com_2',
             list_id_parent = [],
             is_dyn_sse     = True) as com_2:

        html.div('[COMPONENT 02] - B',
                 data_hx_trigger = 'click',
                 data_hx_target  = '#com_2',
                 data_hx_get     = '/com_1',
                 data_hx_swap    = 'outerHTML')
        yield com_2

    with Com(id_com         = 'com_3',
             list_id_parent = ['com_2'],
             is_dyn_sse     = True) as com_3:

        html.div('[COMPONENT 03] - C')
        yield com_3

        # circle_small = svg.svg(width = '100', height = '100')
        # with circle_small:
        #     svg.circle(cx              = '50',
        #                cy              = '50',
        #                r               = '20',
        #                stroke          = 'black',
        #                stroke_width    = '5',
        #                fill            = 'white')

        # circle1 = svg.svg(width = '100', height = '100')
        # with circle1:
        #     svg.circle(cx              = '50',
        #                cy              = '50',
        #                r               = '40',
        #                stroke          = 'black',
        #                stroke_width    = '4',
        #                fill            = 'red',
        #                data_hx_get     = '/circle2',
        #                data_hx_trigger = 'click')

        # circle2 = svg.svg(width = '100', height = '100')
        # with circle2:
        #     svg.circle(cx              = '50',
        #                cy              = '50',
        #                r               = '40',
        #                stroke          = 'black',
        #                stroke_width    = '4',
        #                fill            = 'blue',
        #                data_hx_get     = '/circle1',
        #                data_hx_trigger = 'click',
        #                data_hx_on      = "htmx:beforeRequest: console.log('Circle clicked!')")
        # print('')

