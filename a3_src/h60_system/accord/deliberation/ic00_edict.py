# -*- coding: utf-8 -*-
"""
---

title:
    "Discord deliberation component."

description:
    "Controls the deliberation."

id:
    "04fff1bb-ea23-4dc7-a49e-ee3d49415eac"

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
import uuid

import fl.util
import key

import fl.net.discord.bot

# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Transcript aggregation coroutine.

    """
    transcript       = collections.defaultdict(list)
    map_str_question = collections.defaultdict(str)
    map_set_id_user  = collections.defaultdict(set)
    map_name_user    = dict()

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Keep transcript of messages posted
        # in each channel.
        #
        if inputs['msg']['ena']:
            timestamp = inputs['msg']['ts']
            for msg in inputs['msg']['list']:
                transcript[msg['name_channel']].append((timestamp, msg))

        list_request = list()  # To the LLM.
        list_msg     = list()  # To discord.

        if inputs['cmd']['ena']:
            timestamp = inputs['cmd']['ts']
            for cmd in inputs['cmd']['list']:

                if (     cmd['type']         == 'command'
                     and cmd['name_command'] == 'ask'):

                    list_msg.extend(_init_deliberation(
                                        cmd              = cmd,
                                        map_str_question = map_str_question))

                elif (     cmd['type'] == 'interaction'
                       and cmd['id_btn'].startswith('btn_join_')):

                    list_msg.extend(_join_deliberation(
                                        cmd              = cmd,
                                        map_str_question = map_str_question,
                                        map_set_id_user  = map_set_id_user,
                                        map_name_user    = map_name_user))

                elif (     cmd['type']         == 'command'
                       and cmd['name_command'] == 'summary'):

                    list_request.append(_summarize(
                                        cmd              = cmd,
                                        map_str_question = map_str_question,
                                        transcript       = transcript,
                                        map_set_id_user  = map_set_id_user))

                else:
                    raise RuntimeError(
                            'Command type not recognized: {type}'.format(
                                                        type = cmd['type']))

        if list_msg:
            outputs['msg']['ena'] = True
            outputs['msg']['ts'].update(timestamp)
            outputs['msg']['list'][:] = list_msg

        if list_request:
            outputs['request']['ena'] = True
            outputs['request']['ts'].update(timestamp)
            outputs['request']['list'][:] = list_request


# -----------------------------------------------------------------------------
def _init_deliberation(cmd, map_str_question):
    """
    Initiate a deliberation and yield a join button.

    """
    try:
        id_channel                   = cmd['id_channel']
        str_question                 = ' '.join(cmd['args'])
        map_str_question[id_channel] = str_question
    except KeyError:
        return
    else:
        yield dict(
            type       = 'msg',
            id_channel = cmd['id_channel'],
            content    = 'Join deliberation.',
            button     =  fl.net.discord.bot.ButtonData(
                                label  = 'Join',
                                id_btn = 'btn_join_{uid}'.format(
                                                uid = uuid.uuid4().hex[:16])))


# -----------------------------------------------------------------------------
def _join_deliberation(cmd,
                       map_str_question,
                       map_set_id_user,
                       map_name_user):
    """
    Yield all required join messages.

    """
    id_user    = cmd['id_user']
    id_channel = cmd['id_channel']

    if id_user in map_set_id_user[id_channel]:
        return

    map_set_id_user[id_channel].add(id_user)

    yield dict(type       = 'dm',
               id_user    = id_user,
               content    = map_str_question[id_channel])

    yield dict(type       = 'msg',
               id_channel = id_channel,
               content    = '{user} joined the deliberation.'.format(
                                                    user = cmd['name_user']))


# -----------------------------------------------------------------------------
def _summarize(cmd,
               map_str_question,
               transcript,
               map_set_id_user):
    """
    Yield a summary request for the LLM.

    """
    id_channel     = cmd['id_channel']
    set_id_user    = map_set_id_user[id_channel]
    list_id_user   = list(sorted(set_id_user))
    str_transcript = ''
    for (name_channel, list_tup_msg) in transcript.items():

        is_dm = str(name_channel) == 'None'
        if is_dm:
            for (timestamp, msg) in list_tup_msg:
                is_in_discussion = msg['id_author'] in set_id_user
                if is_in_discussion:
                    str_transcript += '\n {name}: "{txt}"'.format(
                                            name = msg['name_author'],
                                            txt  = msg['content'])

        str_transcript += '\n'
    str_transcript += '\n'

    str_prompt = """Please provide a summary for the given transcript.

    The question given to the participants was:

    {str_question}

    Make sure that the summary highlights the main different points of view
    that have been expressed and the main arguments that have been put forward
    and suggests potential consensus solutions.

    {str_transcript}

    """.format(str_question   = map_str_question[id_channel],
               str_transcript = str_transcript)

    request = {
        'state':       dict(id_channel   = id_channel,
                            list_id_user = list_id_user),
        'model':       'gpt-3.5-turbo',
        'messages':    [{
            'role':    'system',
            'content': str_prompt}]}

    return request