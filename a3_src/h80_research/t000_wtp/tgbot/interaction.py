# -*- coding: utf-8 -*-
"""
---

title:
    "Telegram bot interaction context module."

description:
    "This module contains a class based context
    manager to help manage the life cycle of
    individual interactions with a Telegram bot
    implemented using the python-telegram-bot
    library."

id:
    "42e685b9-8891-42b2-859c-827ca283122e"

type:
    dt003_python_module

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


"""


import http
import logging
import os
import pprint
import typing
import urllib.parse

import pydantic
import requests

import t000_wtp.tgbot.logutil as tgbot_logutil
import t000_wtp.tgbot.runtime as tgbot_runtime


URL_CHATSERVER = 'https://chatserver.paideia.ai'

# id_chat -> coroutine
map_chat = {}


# -----------------------------------------------------------------------------
async def _chat(fcn_telegram,
                fcn_new_conv,
                fcn_reply):
    """
    Chat coroutine.

    This synchronous coroutine is responsible for
    defining the chat lifecycle from initiation
    through to conclusion.

    All dependencies are injected so that the
    chat logic can be tested in isolation.

    """

    # Conversation initiation.
    #
    state = yield
    while state.str_topic == '':
        await fcn_telegram('What topic do you want to discuss?')
        state = yield
        state.str_topic = state.str_message_last

    await fcn_telegram(await fcn_new_conv(state.str_topic))

    # Carry out the conversation.
    #
    while True:

        state = yield
        logging.info(pprint.pformat(state.dict(), indent=4))
        message = await fcn_reply(state.str_message_last)
        if message:
            await fcn_telegram(message)


# =============================================================================
class InteractionState(pydantic.BaseModel):
    """
    Bot interaction state.

    """

    version:          int  = 1
    id_conversation:  str  = ''
    id_message_last:  str  = ''
    str_message_last: str  = ''
    str_topic:        str  = ''


# =============================================================================
class Context():
    """
    Interaction context for a telegram bot.

    This context will be exited when the
    current interaction with the bot is
    complete.

    An interaction consists of zero or one
    inputs from the user and zero or more
    responses from the bot. In other words
    any action taken by or to the bot.

    """

    id_chat: int
    bot:     tgbot_runtime.Context
    update:  typing.Any
    context: typing.Any
    state:   InteractionState

    # -------------------------------------------------------------------------
    def __init__(self,
                 bot:     tgbot_runtime.Context,
                 update:  typing.Any,
                 context: typing.Any):
        """
        Return an instance of BotInteractionContext.

        Gets called at the start of each interaction.

        """

        self.id_chat = update.effective_chat.id

        try:
            self.state   = InteractionState(**bot.db[self.id_chat])
        except KeyError:
            self.state   = InteractionState()
        finally:
            self.bot     = bot
            self.update  = update
            self.context = context

    # -------------------------------------------------------------------------
    def __enter__(self):
        """
        Enter the interaction context for the telegram bot.

        """

        return self

    # -------------------------------------------------------------------------
    def __exit__(self, type_exc, value_exc, tb_exc):
        """
        Exit the interaction context for the telegram bot.

        Make sure that relevant state is saved in the db.

        """

        self.bot.db[self.id_chat] = self.state.dict()
        self.bot.db.commit()

    # -------------------------------------------------------------------------
    @tgbot_logutil.trace
    async def reset(self, str_topic = ''):
        """
        Reset the interaction state.

        """

        logging.info('Reset/restart chat.')
        self.state.str_topic         = str_topic
        self.state.str_message_last  = ''
        map_chat[self.id_chat]       = _chat(fcn_telegram = self.telegram,
                                             fcn_new_conv = self._new_conv,
                                             fcn_reply    = self._reply)
        await map_chat[self.id_chat].asend(None)  # Prime the generator
        await map_chat[self.id_chat].asend(self.state)

    # -------------------------------------------------------------------------
    @tgbot_logutil.trace
    async def step(self):
        """
        Single step the logic coroutine, creating it if necessary.

        """

        self.state.str_message_last = self.update.message.text
        try:
            await map_chat[self.id_chat].asend(self.state)
        except KeyError:
            logging.warning(
                ('Possible server restart? '
                 'Recreating chat coroutine from saved state.'))
            map_chat[self.id_chat] = _chat(fcn_telegram = self.telegram,
                                           fcn_new_conv = self._new_conv,
                                           fcn_reply    = self._reply)
            await map_chat[self.id_chat].asend(None)  # Prime the generator
            await map_chat[self.id_chat].asend(self.state)

    # -------------------------------------------------------------------------
    @tgbot_logutil.trace
    async def telegram(self, str_text):
        """
        Utility function to send a message to the user via telegram.

        """

        await self.context.bot.send_message(chat_id = self.id_chat,
                                            text    = str_text)

    # -------------------------------------------------------------------------
    async def _new_conv(self, topic):
        """
        Utility function to create a new conversation on the chatserver.

        """

        response = requests.post(**self._post_params('new'),
                                 json = { 'name':    'dfs_v1',
                                          'request': { 'topic': topic }})
        if response.status_code != http.HTTPStatus.OK:
            return self._error_message(response)

        payload = response.json()
        self.state.id_conversation = payload['conversation_id']
        self.state.id_message_last = payload['message_id']
        return payload['message']

    # -------------------------------------------------------------------------
    async def _reply(self, reply):
        """
        Utility function to add a reply to a conversation on the chatserver.

        """

        id_conversation = self.state.id_conversation
        id_message_last = self.state.id_message_last
        response = requests.post(**self._post_params('reply'),
                                 json = { 'conversation_id': id_conversation,
                                          'message_id':      id_message_last,
                                          'message':         reply })
        if response.status_code != http.HTTPStatus.OK:
            return self._error_message(response)

        payload = response.json()
        self.state.id_message_last = payload['id']
        return payload['message']

    # -------------------------------------------------------------------------
    def _post_params(self, endpoint):
        """
        Return standard requests.post parameters.

        """

        uuid_bearer = os.getenv("UUID_BEARER_CHATSERVER")
        return { 'url':     urllib.parse.urljoin(URL_CHATSERVER, endpoint),
                 'headers': { 'accept':        'application/json',
                              'Content-Type':  'application/json',
                              'Authorization': f'Bearer {uuid_bearer}'},
                 'timeout': 10 }

    # -------------------------------------------------------------------------
    def _error_message(self, response):
        """
        Log an error and return a suitable user-facing error message.

        """

        logging.error('Error: %s - %s', response.status_code, response.text)
        is_not_found = response.status_code == http.HTTPStatus.NOT_FOUND  # 404
        if is_not_found:
            return ('We have encountered an error. '
                    'Please restart the conversation.')
        return f'Internal error: {response.status_code}'
