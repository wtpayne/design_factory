# -*- coding: utf-8 -*-
"""
---

title:
    "Phypermedia UI compoenent generation."

description:
    "Phypermedia UI compoenent generation functionality."

id:
    "cee65c85-728b-4576-bd63-c347136db697"

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


import re
import typing
import weakref

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

    is_ui_generated = False

    with UiContext() as ctx:

        while True:

            inputs = yield (outputs, signal)

            for key in outputs:
                outputs[key]['ena'] = False
                outputs[key]['list'].clear()

            if not inputs['ctrl']['ena']:
                continue

            list_msg_in = list()
            if inputs['msg']['ena']:
                list_msg_in.extend(inputs['msg']['list'])

            (list_msg_out, list_com_out) = ctx.step(list_msg_in)

            if not is_ui_generated:
                list_com_out = [com for com in _generate_ui(ctx)]
                is_ui_generated = True
 
            if list_msg_out:
                for key in outputs:
                    outputs[key]['ena']  = True
                    outputs[key]['list'].clear()
                    outputs[key]['list'].extend(list_msg_out)


# =============================================================================
class UiContext():
    """
    Pub-Sub message broker, UI component factory, and context manager.

    """

    # List of filters and subscribers.
    #
    list_subs: list[tuple[re.Pattern, list[weakref.ref['Com']]]] = list()

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Construct a Broker instance.

        """

        pass

    # -------------------------------------------------------------------------
    def __enter__(self):
        """
        Enter the context.

        """

        return self

    # -------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context.

        Clean up the pub-sub subscribers table and
        invalidate all remaining subscribers.

        """

        for (_, list_weakref_subscriber) in self.list_subs:
            set_to_delete = set()
            for weakref_subscriber in list_weakref_subscriber:
                subscriber = weakref_subscriber()
                if subscriber is not None:
                    subscriber.invalidate()
                set_to_delete.add(weakref_subscriber)
            for weakref_subscriber in set_to_delete:
                list_weakref_subscriber.remove(weakref_subscriber)

    # -------------------------------------------------------------------------
    def com(self, str_filt, *args, **kwargs) -> 'Com':
        """
        Create a new component.

        This automatically registers the component with the
        pub-sub broker.

        """

        reo_filt = re.compile(str_filt)
        com = Com(pubsub = self, reo_filt = reo_filt, *args, **kwargs)
        self.subscribe(filt = reo_filt, com = com)
        return com

    # -------------------------------------------------------------------------
    def on_component_deleted(self, com):
        """
        Callback for component deletion.

        When a component is deleted, it is removed from the
        pub-sub subscribers table (self.map_subs). We also
        handle the case where the object pointed to by the
        weakref has already been deleted (is None).

        """

        for (_, list_weakref_subscriber) in self.list_subs:
            for weakref_subscriber in list_weakref_subscriber:
                subscriber = weakref_subscriber()
                if (subscriber is com) or (subscriber is None):
                    list_weakref_subscriber.remove(weakref_subscriber)
                    break

    # -------------------------------------------------------------------------
    def step(self, list_msg_in):
        """
        Publish a message to the pub-sub broker.

        """

        list_msg_out = list()
        for (reo_filt, list_weakref_subscriber) in self.list_subs:

            list_msg_filt = list()
            for msg_in in list_msg_in:
                id_msg = msg_in['id_msg']
                if reo_filt.match(id_msg):
                    list_msg_filt.append(msg_in)

            for weakref_subscriber in list_weakref_subscriber:
                subscriber = weakref_subscriber()
                if subscriber is None:
                    continue
                list_msg_out.extend(subscriber.step(list_msg_filt))

        return list_msg_out

    # -------------------------------------------------------------------------
    def subscribe(self, filt: str | re.Pattern, com: "Com"):
        """
        Subscribe to a message from the pub-sub broker.

        """

        if isinstance(filt, str):
            reo_filt = re.compile(filt)
        elif isinstance(filt, re.Pattern):
            reo_filt = filt
        else:
            raise ValueError(f'Invalid filter type: {type(filt)}')

        weakref_subscriber = weakref.ref(com, self.on_component_deleted)
        self.map_subscriber[reo_filt].append(weakref_subscriber)


# =============================================================================
class ComData(pydantic.BaseModel):
    """
    UI component data.

    Contains markup and metadata for the component.

    """

    model_config = pydantic.ConfigDict(arbitrary_types_allowed = True)

    id_com:         str
    list_id_parent: list[str] = []    # Defines the containment hierarchy.
    list_id_page:   list[str] = []    # Used for SSE topics.
    is_valid:       bool      = True  # set to False to delete the component.
    is_dyn_sse:     bool      = False # Is dynamic using SSE.
    media_type:     str       = 'text/html'


# =============================================================================
class Com(ComData):
    """
    UI component.

    """

    broker: UiContext | None = None
    reo_filt: re.Pattern | None = None

    # -------------------------------------------------------------------------
    def __init__(self, broker, reo_filt, *args, **kwargs):
        """
        Construct a Com instance.

        """

        self.broker = broker
        self.reo_filt = reo_filt

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
def _generate_ui(ctx) -> typing.Generator[Com, None, None]:
    """
    Yield components.

    data_hx_get     - Issues a GET request to the given URL
    data_hx_post    - Issues a POST request to the given URL
    data_hx_put     - Issues a PUT request to the given URL
    data_hx_patch   - Issues a PATCH request to the given URL
    data_hx_delete  - Issues a DELETE request to the given URL
    data_hx_trigger - Can be

    """

    def coro_1(com):
        outdata = None
        while True:
            (indata) = yield (outdata)

    # TODO: Move component creation within coro?
    #       THEN ctx.add_coro(coro_1) <-- coro_1 will yield all components,
    #       and ctx will handle message routing.

    with ctx.com(filt           = 'com_1',
                 id_com         = 'com_1',
                 list_id_parent = ['app'],
                 coro           = coro_1,
                 is_dyn_sse     = True) as com_1:

        html.div('[COMPONENT 01] - *** CONINUITY ***', 
                 data_hx_trigger = 'click',
                 data_hx_target  = '#com_1',
                 data_hx_get     = '/com_2',
                 data_hx_swap    = 'outerHTML')
        yield com_1

    with ctx.com(filt           = 'com_2',
                 id_com         = 'com_2',
                 list_id_parent = [],
                 list_id_page   = ['app'],
                 is_dyn_sse     = True) as com_2:

        html.div('[COMPONENT 02] - B7',
                 data_hx_trigger = 'click',
                 data_hx_target  = '#com_2',
                 data_hx_get     = '/com_1',
                 data_hx_swap    = 'outerHTML')
        yield com_2

    with ctx.com(id_com         = 'com_3',
                 list_id_parent = ['com_1'],
                 is_dyn_sse     = True) as com_3:
        
        with html.form(id                = 'form_send',
                       data_hx_put       = '/send-message',
                       data_hx_swap      = 'none',
                       data_hx_indicator = '#loading'):

            html.input_(_class      = 'chat-input',
                        type        = 'text',
                        placeholder = 'Type a message...',
                        name        = 'message')

            with html.button(
                        id                            = 'btn_send',
                        type                          = 'submit',
                        data_hx_disable_while_request = 'true',
                        _class                        = 'chat-submit-button'):

                html.div('Send',
                         _class = 'button-text')
            
            html.div('Sending...',
                     id     = 'loading',
                     _class = 'htmx-indicator')



        # html.label('First Name')
        # html.input_(type = 'text',
        #             name = 'firstName',
        #             value = 'Joe')
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

