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
import fl.util.edict
import key

import fl.net.discord.bot


NOTHING     = tuple()
PREFIX_JOIN = 'join_'


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Transcript aggregation coroutine.

    """

    # Setup system state
    #
    #   state['session'] is a map from id_session -> info_session
    #   state['user']    is a map from id_user    -> info_user
    #   state['prompt']  is a map from id_prompt  -> str_prompt
    #
    #   info_session is { 'admin':        id_admin,
    #                     'id_channel':   id_channel,
    #                     'ts_tick_last': timestamp,   # time of last tick
    #                     'ts_act_last':  timestamp,   # time of last action
    #                     'ts_summ_last': timestamp,   # time of last summary
    #                     'topic':        str_topic,
    #                     'participant':  set(id_user),
    #                     'contributor':  set(id_user),
    #                      }
    #   info_user    is { 'name':       name_user,
    #                     'session':    id_session,
    #                     'transcript': list(content) }
    #
    state = dict(session = dict(),
                 user    = dict(),
                 prompt  = dict())
    state['prompt'].update(cfg.get('prompt', dict()))

    # Main loop.
    #
    signal = fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        if not inputs['ctrl']['ena']:
            continue
        timestamp = inputs['ctrl']['ts']

        tick_interval_secs = 5
        list_msg_in = list(_gen_msg_tick(state, timestamp, tick_interval_secs))
        if inputs['discord']['ena']:
            list_msg_in.extend(inputs['discord']['list'])
        if inputs['openai']['ena']:
            list_msg_in.extend(inputs['openai']['list'])

        list_to_discord = list()
        list_to_openai  = list()
        for msg in list_msg_in:
            (part_discord, part_openai) = _update(state, timestamp, msg)
            list_to_discord += part_discord
            list_to_openai  += part_openai

        if list_to_discord:
            outputs['discord']['ena'] = True
            outputs['discord']['ts'].update(timestamp)
            outputs['discord']['list'][:] = list_to_discord

        if list_to_openai:
            outputs['openai']['ena'] = True
            outputs['openai']['ts'].update(timestamp)
            outputs['openai']['list'][:] = list_to_openai


# -----------------------------------------------------------------------------
def _gen_msg_tick(state, timestamp, tick_interval_secs):
    """
    Yield all due tick messages.

    """

    MS_PER_SECOND      = 1000
    US_PER_MS          = 1000
    US_PER_SECOND      = MS_PER_SECOND * US_PER_MS
    TICK_INTERVAL_US   = tick_interval_secs * US_PER_SECOND
    ts_rel_us          = timestamp['ts_rel_us']

    for (id_session, info_session) in state['session'].items():

        ts_tick_last = info_session.get('ts_tick_last', 0)
        ts_delta_us  = ts_rel_us - ts_tick_last
        is_tick_due  = ts_delta_us > TICK_INTERVAL_US

        if is_tick_due:
            state['session'][id_session]['ts_tick_last'] = ts_rel_us
            yield dict(type       = 'timer_tick',
                       id_session = id_session,
                       ts_tick    = ts_rel_us)


# -----------------------------------------------------------------------------
def _update(state, timestamp, msg):
    """
    Return an update corresponding to the specified msg.

    """

    discord = list()
    openai  = list()

    str_type      = msg['type']
    is_appcmd     = str_type in { 'appcmd_dm', 'appcmd_guild' }
    is_msgcmd     = str_type in { 'msgcmd_dm', 'msgcmd_guild' }
    is_btn        = str_type in { 'btn',                      }
    is_dm         = str_type in { 'msg_dm',    'edit_dm'      }
    is_guild      = str_type in { 'msg_guild', 'edit_guild'   }
    is_result     = str_type in { 'openai_result',            }
    is_timer_tick = str_type in { 'timer_tick',               }

    if (is_appcmd and msg['name_command'] == 'ask'):
        discord += _on_cmd_ask(state, timestamp, msg)

    if (is_btn    and msg['id_btn'].startswith(PREFIX_JOIN)):
        discord += _on_btn_join(state, timestamp, msg)

    if (is_dm     and msg['id_author'] in state['user']):
        discord += _on_msg_dm(state, timestamp, msg)

    if (is_timer_tick):
        openai  += _on_timer_tick(state, timestamp, msg)

    if (is_result and msg['state']['id_prompt'] == 'summary'):
        discord += _on_llm_summary(state, msg)

    if (is_appcmd and msg['name_command'] == 'dbg_transcript_show'):
        discord += _on_cmd_dbg_transcript_show(state, msg)

    if (is_appcmd and msg['name_command'] == 'dbg_prompt_show'):
        discord += _on_cmd_dbg_prompt_show(state, msg)

    if (is_appcmd and msg['name_command'] == 'dbg_prompt_set'):
        discord += _on_cmd_dbg_prompt_set(state, msg)

    return (discord, openai)


# -----------------------------------------------------------------------------
def _on_cmd_ask(state, timestamp, msg):
    """
    Respond to an ask command.

    """

    # Create a new session in the state.
    #
    id_user      = msg['id_user']
    id_channel   = msg.get('id_channel', None)
    ts_rel_now   = timestamp['ts_rel_us']
    str_topic    = ' '.join(msg['args'])
    id_session   = uuid.uuid4().hex[:6]
    state['session'][id_session] = dict(
                                    admin        = id_user,
                                    id_channel   = id_channel, # Maybe None
                                    ts_tick_last = ts_rel_now,
                                    ts_act_last  = ts_rel_now,
                                    ts_summ_last = 0,
                                    topic        = str_topic,
                                    participant  = set(),  # set(id_user)
                                    contributor  = set())  # set(id_user)

    # Configure a join button for the session.
    #
    str_invite = 'Join deliberation #{id}'.format(id = id_session)
    cfg_button = fl.net.discord.bot.ButtonData(
                                    label  = 'Join',
                                    id_btn = _id_btn(PREFIX_JOIN, id_session))

    # Enqueue a message with the session join button.
    #
    msg_type = msg['type']
    if msg_type == 'appcmd_dm':
        yield dict(type    = 'msg_dm',
                   id_user = id_user,
                   content = str_invite,
                   button  = cfg_button)
    if msg_type == 'appcmd_guild':
        yield dict(type       = 'msg_guild',
                   id_channel = id_channel,
                   content    = str_invite,
                   button     = cfg_button)


# -----------------------------------------------------------------------------
def _on_btn_join(state, timestamp, msg):
    """
    On "Join" button press.

    """

    # Remove the user from any previous session.
    #
    id_user = msg['id_user']
    if id_user in state['user']:
        id_session_prev   = state['user'][id_user]['session']
        info_session_prev = state['session'][id_session_prev]

        try:
            info_session_prev['participant'].remove(id_user)
        except KeyError:
            pass

        try:
            info_session_prev['contributor'].remove(id_user)
        except KeyError:
            pass

    # Add the user to the current session.
    #
    id_session      = msg['id_btn'][len(PREFIX_JOIN):]
    info_session    = state['session'][id_session]
    set_participant = info_session['participant']
    set_participant.add(id_user)

    # Create a new transcript for the user.
    #
    name_user = msg['name_user']
    state['user'][id_user] = dict(name       = name_user,
                                  session    = id_session,
                                  transcript = list())

    # Update last-action timestamp.
    #
    ts_rel_now = timestamp['ts_rel_us']
    state['session'][id_session]['ts_act_last'] = ts_rel_now

    # Send a message to the admin.
    #
    yield dict(type    = 'msg_dm',
               id_user = info_session['admin'],
               content = '{name} joined session {session} ' \
                         'as participant #{num}.'.format(
                                                name    = name_user,
                                                num     = len(set_participant),
                                                session = id_session))

    # Send the topic and a 'Submit' button to the user.
    #
    yield dict(type    = 'msg_dm',
               id_user = id_user,
               content = info_session['topic'])


# -----------------------------------------------------------------------------
def _on_msg_dm(state, timestamp, msg):
    """
    On message recieved.

    """

    # Update transcript.
    #
    id_user = msg['id_author']
    state['user'][id_user]['transcript'].append(msg['content'])

    # Update last-action timestamp.
    #
    info_user  = state['user'][id_user]
    id_session = info_user['session']
    ts_rel_now = timestamp['ts_rel_us']
    state['session'][id_session]['ts_act_last'] = ts_rel_now

    return NOTHING


# -----------------------------------------------------------------------------
def _on_timer_tick(state, timestamp, msg):
    """
    Request a new summary.

    """

    SUMMARY_WAIT_SECS = 20
    MS_PER_SECOND     = 1000
    US_PER_MS         = 1000
    US_PER_SECOND     = MS_PER_SECOND * US_PER_MS
    SUMMARY_WAIT_US   = SUMMARY_WAIT_SECS * US_PER_SECOND
    ts_rel_now        = timestamp['ts_rel_us']

    for (id_session, info_session) in state['session'].items():
        ts_tick_last_us     = info_session['ts_tick_last']
        ts_act_last_us      = info_session['ts_act_last']
        ts_summ_last_us     = info_session['ts_summ_last']
        is_summ_most_recent = ts_summ_last_us > ts_act_last_us
        is_up_to_date       = is_summ_most_recent
        if is_up_to_date:
            continue

        ts_delta_us    = ts_tick_last_us - ts_act_last_us
        is_summary_due = ts_delta_us >= SUMMARY_WAIT_US
        if not is_summary_due:
            print('SUMMARY IS NOT YET DUE')
            continue

        # Get all transcripts associated with the session.
        #
        has_transcript = False
        str_transcript = ''
        for (id_user, state_user) in state['user'].items():
            if state_user['session'] == id_session:
                str_transcript += '\n\nA user in the session wrote: \n'
                for item in state_user['transcript']:
                    has_transcript = True
                    str_transcript += ' - {item}\n'.format(item = item)

        if not has_transcript:
            continue

        # Update the last-summary timestamp.
        #
        state['session'][id_session]['ts_summ_last'] = ts_rel_now
        print('PRODUCING SUMMARY FOR SESSION: ' + str(id_session))

        id_prompt  = 'summary'
        str_prompt = state['prompt'][id_prompt].format(
                        str_topic      = state['session'][id_session]['topic'],
                        str_transcript = str_transcript)

        yield dict(state    = dict(id_prompt  = id_prompt,
                                   id_session = id_session),
                   model    = 'gpt-3.5-turbo',
                   messages = [{'role': 'system', 'content': str_prompt}])


# -----------------------------------------------------------------------------
def _on_llm_summary(state, msg):
    """
    Forward LLM summary information to session participants.

    This function is triggered when we recieve
    a resposne message with summary information
    back from the language model.

    """

    str_summary = msg['response']['choices'][0]['message']['content']
    id_session  = msg['state']['id_session']

    # Send the summary to the channel
    # in which the question was asked.
    #
    id_channel  = state['session'][id_session].get('id_channel', None)
    if id_channel is not None:
        yield dict(type       = 'msg_guild',
                   id_channel = id_channel,
                   content    = str_summary)

    # Send the summary to each user
    # in the session.
    #
    for (id_user, state_user) in state['user'].items():
        if state_user['session'] == id_session:
            yield dict(type       = 'msg_dm',
                       id_user    = id_user,
                       content    = str_summary)


# -----------------------------------------------------------------------------
def _on_cmd_dbg_transcript_show(state, msg):
    """
    Respond to a dbg_transcript_show command.

    """

    for (id_user, state_user) in state['user'].items():

        if msg['type'] == 'appcmd_dm':
            yield dict(type    = 'msg_dm',
                       id_user = msg['id_user'],
                       content = '{id_user}: "{transcript}"'.format(
                                    id_user    = id_user,
                                    transcript = state_user['transcript'] ))

        if msg['type'] == 'appcmd_guild':
            yield dict(type       = 'msg_guild',
                       id_channel = msg['id_channel'],
                       content    = '{id_user}: "{transcript}"'.format(
                                    id_user    = id_user,
                                    transcript = state_user['transcript'] ))

# -----------------------------------------------------------------------------
def _on_cmd_dbg_prompt_show(state, msg):
    """
    Respond to a dbg_prompt_show command.

    """

    for (id_prompt, str_prompt) in state['prompt'].items():

        if msg['type'] == 'appcmd_dm':
            yield dict(type    = 'msg_dm',
                       id_user = msg['id_user'],
                       content = id_prompt.upper())
            yield dict(type    = 'msg_dm',
                       id_user = msg['id_user'],
                       content = str_prompt)

        if msg['type'] == 'appcmd_guild':
            yield dict(type       = 'msg_guild',
                       id_channel = msg['id_channel'],
                       content    = id_prompt.upper())
            yield dict(type       = 'msg_guild',
                       id_channel = msg['id_channel'],
                       content    = str_prompt)



# -----------------------------------------------------------------------------
def _on_cmd_dbg_prompt_set(state, msg):
    """
    Respond to a dbg_prompt_set command.

    """

    state['prompt'][msg['args'][0]] = msg['args'][1]
    return NOTHING


# -----------------------------------------------------------------------------
def _id_btn(prefix, id_session):
    """
    """
    id_button = '{prefix}{id_session}'.format(prefix     = prefix,
                                              id_session = id_session)
    return id_button
