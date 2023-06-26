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
users_joined_array = []

# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Transcript aggregation coroutine.

    """
    global users_joined_array
    transcript = collections.defaultdict(list)
    map_user   = collections.defaultdict(list)

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

        list_request = list()
        list_msg     = list()

        if inputs['cmd']['ena']:
            timestamp = inputs['cmd']['ts']
            for cmd in inputs['cmd']['list']:
                type_cmd = cmd['type']

                if (type_cmd == 'interaction'):
                    id_btn = cmd['id_btn']

                    if id_btn.startswith('btn_join_'):
                        join_messages = _create_join_message(cmd, map_user)
                        for msg in join_messages:
                            list_msg.append(msg)

                elif type_cmd == 'command':
                    id_cmd = cmd['name_command']

                    if id_cmd == 'create':
                        list_msg.append(_create_join_button(cmd))

                    if id_cmd == 'question':
                        question = ' '.join(cmd['args'])
                        send_list = (_create_question_messages(question))
                        for recipient in send_list:
                            list_msg.append(recipient)

                    if id_cmd == 'summarize':
                        list_request.append(_create_summary_request(
                                                            cmd, transcript))

                else:
                    raise RuntimeError(
                            'Command type not recognized: {type}'.format(
                                                            type = type_cmd))
                

        if list_msg:
            outputs['msg']['ena'] = True
            outputs['msg']['ts'].update(timestamp)
            outputs['msg']['list'][:] = list_msg

        if list_request:
            outputs['request']['ena'] = True
            outputs['request']['ts'].update(timestamp)
            outputs['request']['list'][:] = list_request

# -----------------------------------------------------------------------------


def _create_join_message(cmd, map_user):
    """
    """
    global users_joined_array

    join_messages_array = []

    id_user = cmd['id_user']
    user_name = cmd['id_name']
    channel_id = cmd['id_channel']
    
    if id_user in users_joined_array:
        return
    
    users_joined_array.append(id_user)

    join_messages_array.append(dict(
        type    = 'dm',
        id_user = id_user,
        content = 'You have joined the deliberation.')) 
            
    join_messages_array.append(dict(
        type       = 'msg',
        id_channel = channel_id,
        content    = '{user_name_} has joined the deliberation.'.format(user_name_ = user_name)))
            
    for user in users_joined_array:
        if user != id_user:
            join_messages_array.append(dict(
                type    = 'dm',
                id_user = user,
                content = 'User {user_name_} has joined the deliberation.'.format(user_name_ = user_name)))

    return join_messages_array


# -----------------------------------------------------------------------------
def _create_join_button(cmd):
    """
    Return a message that contains a join button.

    """
    str_uid = uuid.uuid4().hex[:16]
    id_btn  = 'btn_join_{uid}'.format(uid = str_uid)

    return dict(
        type       = 'msg',
        id_channel = cmd['id_channel'],
        content    = 'Join deliberation: {uid}'.format(uid = str_uid),
        button     =  fl.net.discord.bot.ButtonData(label  = 'Join',
                                                    id_btn = id_btn))


# -----------------------------------------------------------------------------
def _create_question_messages(delib_question):
    """
    Return a list of messages that contain the question to each user that has joined the deliberation.
    """

    send_questions_dict_array = list()
    if delib_question is None:
        raise Exception("Delib question is not provided")

    if len(users_joined_array) == 0:
        raise Exception("Users joined array is empty")

    for user_id in users_joined_array:
        send_questions_dict_array.append(dict(
            type       = 'dm',
            id_user    = user_id,
            content    = delib_question))
        
    return send_questions_dict_array

# -----------------------------------------------------------------------------
def _create_summary_request(cmd, transcript):
    """
    """
    str_transcript = ''

    for (name_channel, list_tup_msg) in transcript.items():

        str_transcript += '\n Channel {name}:\n'.format(
                                        name = name_channel)

        for (timestamp, msg) in list_tup_msg:
            str_transcript += '\n {name}: "{txt}"'.format(
                                    name = msg['name_author'],
                                    txt  = msg['content'])

        str_transcript += '\n'

    str_transcript += '\n'

    str_prompt = """Please provide a summary for the given transcript.

    Make sure that the summary highlights the main different points of view
    that have been expressed and the main arguments that have been put forward
    and suggests potential consensus solutions.

    {str_transcript}

    """.format(str_transcript = str_transcript)

    request = {
        'model':       'gpt-3.5-turbo',
        'messages':    [{
            'role':    'system',
            'content': str_prompt}]}

    return request