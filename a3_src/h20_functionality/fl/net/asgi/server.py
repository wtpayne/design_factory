# -*- coding: utf-8 -*-
"""
---

title:
    "ASGI server integration support module."

description:
    "This Python module is designed to support
    the integration of one or more embedded ASGI
    servers to serve web resources and provide
    simple HTTP APIs. The embedded ASGI server
    is based on starlette and uvicorn, and runs
    in a separate process, communicating with
    the main coroutine using multiprocessing
    queues."

id:
    "ea1c0472-71e3-465f-9478-7f0b683afe4d"

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


import asyncio
import collections
import copy
import datetime
import hashlib
import logging
import multiprocessing
import queue
import time
import uuid

import dill
import loguru
import setproctitle
import sse_starlette.sse
import starlette.applications
import starlette.background
import starlette.exceptions
import starlette.middleware
import starlette.middleware.sessions
import starlette.requests
import starlette.responses
import starlette.routing
import starlette.websockets
import uvicorn

import fl.util


_DEFAULT_DOC = ('text/html',
"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>No content</title>
  </head>
  <body>
    No content.
  </body>
</html>
""")

_ID_COOKIE_SESSION = 'xw_sid'
_ID_COOKIE_USER    = 'xw_uid'


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro(cfg):
    """
    """

    # Create the queues that we will be
    # using to communicate with the ASGI
    # server process.
    #
    # Each of these has an associated
    # feeder thread with it's own PID.
    #
    # At some point, it would be good
    # to set an appropriate process title
    # for these feeder threads, but we
    # lack an easy way of doing this
    # right now.
    #
    queue_resources  = multiprocessing.Queue()  # From system to server
    queue_requests   = multiprocessing.Queue()  # From server to system
    map_queues       = dict(queue_resources = queue_resources,
                            queue_requests  = queue_requests)
    iter_queue       = tuple(map_queues.values())
    str_name_process = 'discord-bot'
    process_server   = multiprocessing.Process(target = _asgi_server_process,
                                               args   = (cfg, map_queues),
                                               name   = str_name_process,
                                               daemon = True)
    process_server.start()
    map_hashes    = dict()
    list_from_api = list()

    while True:

        list_from_api.clear()
        while True:
            try:
                list_from_api.append(queue_requests.get(block = False))
            except queue.Empty:
                break

        (list_to_api, unix_time) = yield (list_from_api)

        accumulator = dict()
        for map_res in list_from_api:
            _remove_duplicates(map_res, map_hashes)
            accumulator.update(map_res)

            try:
                queue_resources.put(accumulator, block = False)
            except queue.Full:
                pass # TODO: LOG SOME SORT OF ERROR?

    # TODO:- Call uvicorn.stop on terminate

# -----------------------------------------------------------------------------
# def finalize(runtime, config, inputs, state, outputs):
#     """
#     Clean up resources.

#     """
#     if not state:
#         return

#     # Halt the ASGI server process
#     # before doing anything to the
#     # queues. Once this server process
#     # is stopped, nothing will be
#     # reading or writing from
#     # the queues and we can safely
#     # terminate them as well.
#     #
#     state['process_server'].terminate()

#     # For some reason joining
#     # the process server causes
#     # a broken pipe error. I'm
#     # not quite sure why.
#     #
#     # state['process_server'].join()

#     # Each multiprocessing queue has
#     # an associated feeder thread that
#     # needs to be closed and joined.
#     #
#     # The call to join_thread will block
#     # unless the queue is empty or unless
#     # the cancel_join_thread() function
#     # has been called.
#     #
#     for queue_ipc in state['iter_queue']:
#         queue_ipc.cancel_join_thread()
#         queue_ipc.close()
#         _clear(queue_ipc)
#         queue_ipc.join_thread()


# -----------------------------------------------------------------------------
def _clear(queue_ipc):
    """
    Clear all items from the specified queue.

    """
    try:
        while True:
            queue_ipc.get_nowait()
    except queue.Empty:
        pass
    except ValueError:
        pass


# -----------------------------------------------------------------------------
def _remove_duplicates(map_res, map_hashes):
    """
    Modify map_res to remove duplicates that we have seen before.

    """
    tup_route = tuple(map_res.keys())
    for route in tup_route:

        (media_type, obj) = map_res[route]
        hash = hashlib.md5()
        hash.update(media_type.encode('utf-8'))

        if isinstance(obj, bytes):
            hash.update(obj)
        else:
            hash.update(obj.encode('utf-8'))

        digest = hash.hexdigest()

        if route in map_hashes and digest == map_hashes[route]:
            map_res.pop(route, None)
        else:
            map_hashes[route] = digest


# -----------------------------------------------------------------------------
def _asgi_server_process(cfg, map_queues):
    """
    Run the ASGI server process. (Runs until killed by a signal)

    """

    #--------------------------------------------------------------------------
    async def handle_route(request = None, *args, **kwargs):
        """
        Return a response for the specified id_resource param.

        """
        tasks = _ensure_continuously_updated()

        (id_session, id_user) = _get_cookies(request)

        if request is None:
            id_resource = 'default'
        else:
            url_path    = request.url.path.strip('/')
            id_resource = request.path_params.get('id_resource', url_path)
            tasks.add_task(_enqueue_requests,
                           request     = request,
                           id_resource = id_resource,
                           id_session  = id_session,
                           id_user     = id_user)

        (media_type, content) = _lookup_resource(id_resource)

        # SSE connection to a pub-sub topic.
        if media_type == 'topic':
            response = _get_sse_event_source_for_topic(
                                        tasks, request, id_topic = id_resource)
            return response

        # Websocket connection to a callback "resource".
        if media_type == 'socket':
            await _websocket_handler(
                            websocket = request,
                            callback  = _load_callback(media_type, content))
            return None

        # HTTP request to a callback "resource".
        if media_type == 'callback':
            callback = _load_callback(media_type, content)
            (media_type, content) = await callback(request)

        response = starlette.responses.Response(media_type = media_type,
                                                content    = content,
                                                background = tasks)
        _set_cookies(response, id_session, id_user)
        return response


    #--------------------------------------------------------------------------
    def _ensure_continuously_updated():
        """
        Update app state and ensure that background update tasks are running.

        """
        _update_and_notify()
        tasks = starlette.background.BackgroundTasks()
        tasks.add_task(_update_and_notify_background_task)
        return tasks

    #--------------------------------------------------------------------------
    def _update_and_notify():
        """
        Update resources and topics then notify listeners of changes.

        """
        (set_id_resource_changed, set_id_topic_changed) = _update_resources()
        _update_topics(set_id_topic_changed)
        _notify_listeners(set_id_resource_changed)

    #--------------------------------------------------------------------------
    def _update_resources():
        """
        Bring the resource table up to date with the latest changes.

        """
        set_id_topic_changed    = set()
        set_id_resource_changed = set()
        while True:

            # Update the resource database.
            try:
                map_resource_batch = app.state.queue_resources.get(
                                                                block = False)
                app.state.map_resources.update(map_resource_batch)
            except queue.Empty:
                break

            # Keep track of which change listeners to notify.
            set_id_resource_in_batch = set(map_resource_batch.keys())
            set_id_resource_changed |= set_id_resource_in_batch

            # Update default and keep track of which topics have changed.
            for (id_resource, resource) in map_resource_batch.items():
                if id_resource == 'default':
                    app.state.default = map_resource_batch['default']
                (type_resource, bytes_resource) = resource
                if type_resource == 'topic':
                    id_topic = id_resource
                    set_id_topic_changed.add(id_topic)

        return (set_id_resource_changed, set_id_topic_changed)

    #--------------------------------------------------------------------------
    def _update_topics(set_id_topic_changed):
        """
        Bring the topic lookups up to date with the latest changes.

        First, we determine if any active
        topics have changed. Recall that
        each id_topic is also an id_resource,
        so all we need to do is to find if
        any active topic ids are in the set
        of changed resource ids.

        Once we have the list of topics
        that have changed, we can work
        out which resources have been
        added to each topic, and which
        resources have been removed, and
        update the maps as required.

        """
        for id_topic in set_id_topic_changed:
            set_id_resource_old = app.state.map_topic_to_resource[id_topic]
            bytes_topic         = app.state.map_resources[id_topic][1]
            set_id_resource_new = set(bytes_topic.split(' '))
            for id_resource in set_id_resource_old - set_id_resource_new:
                app.state.map_resource_to_topic[id_resource].remove(id_topic)
            for id_resource in set_id_resource_new - set_id_resource_old:
                app.state.map_resource_to_topic[id_resource].add(id_topic)
            app.state.map_topic_to_resource[id_topic] = set_id_resource_new

    #--------------------------------------------------------------------------
    def _notify_listeners(set_id_resource_changed):
        """
        Notify listeners of changes to resources.

        Listeners subscribe to topics, each
        of which is a collection of resources.

        Firstly, we determine the set of
        responsive topics, given the set
        of resources that have changed.

        Them, we publish notifications to
        the relevant subscribed queues.

        """
        for id_resource in set_id_resource_changed:
            for id_topic in app.state.map_resource_to_topic[id_resource]:
                for queue_subscriber in app.state.map_topic_to_queue[id_topic]:
                    queue_subscriber.put_nowait({
                        'event': id_resource,
                        'data':  app.state.map_resources[id_resource][1]})


    #--------------------------------------------------------------------------
    async def _update_and_notify_background_task():
        """
        Continually update resource table and notify listeners of changes.

        Try to detect if another background task
        is already running by looking at when
        the state was last updated.

        """
        polling_interval   = 0.1 # seconds
        staleout_duration  = 3 * polling_interval
        staleout_time      = app.state.ts_last_update + staleout_duration
        is_stale           = time.time() > staleout_time
        is_another_running = not is_stale

        if is_another_running:
            return

        ts_last_update = app.state.ts_last_update
        while True:
            await asyncio.sleep(polling_interval)

            # If another background process is
            # running and updating the state,
            # then we don't need to be running
            # ourselves.
            #
            is_another_running = ts_last_update != app.state.ts_last_update
            if is_another_running:
                return

            ts_last_update = time.time()
            app.state.ts_last_update = ts_last_update
            _update_and_notify()

    #--------------------------------------------------------------------------
    async def _enqueue_requests(request, id_resource, id_session, id_user):
        """
        Enqueue requests from the client for the rest of the bowyer system.

        """
        headers = dict(request.headers)

        try:
            header_accept          = headers['accept']
            header_accept_encoding = headers['accept-encoding']
            header_accept_language = headers['accept-language']
            header_user_agent      = headers['user-agent']
        except KeyError:
            pass
        else:
            request_data = dict(id_resource     = str(id_resource),
                                id_session      = str(id_session),
                                id_user         = str(id_user),
                                client_ip       = request['client'][0],
                                url             = str(request.url),
                                accept          = header_accept,
                                accept_encoding = header_accept_encoding,
                                accept_language = header_accept_language,
                                user_agent      = header_user_agent)

            query_params = request.query_params
            for key in query_params.keys():
                request_data[key] = query_params.getlist(key)

            try:
                app.state.queue_requests.put(request_data, block = False)
            except queue.Full:
                pass

    #--------------------------------------------------------------------------
    def _lookup_resource(id_resource):
        """
        Return the resource corresponding to the specified id_resource.

        """
        if id_resource == 'ena':
            if app.state.default is not None:
                return app.state.default
            else:
                raise starlette.exceptions.HTTPException(
                                            status_code = 204)  # No content

        if id_resource == 'keys':
            return ('text/html', '<br>'.join(app.state.map_resources.keys()))

        try:
            return app.state.map_resources[id_resource]
        except KeyError:
            if app.state.default is not None:
                return app.state.default
            else:
                raise starlette.exceptions.HTTPException(
                                            status_code = 204)  # No content

    #--------------------------------------------------------------------------
    def _get_sse_event_source_for_topic(tasks, request, id_topic):
        """
        Return an SSE EventSourceaResponse for the specified pub sub topic.

        """
        queue_notify = asyncio.Queue()
        app.state.map_topic_to_queue[id_topic].add(queue_notify)
        response = sse_starlette.sse.EventSourceResponse(
                            # media_type = 'text/event-stream',
                            content    = _generate_change_notifications(
                                                    request, queue_notify),
                            background = tasks)
        return response

    #--------------------------------------------------------------------------
    async def _generate_change_notifications(request, queue_notify):
        """
        Yield items from the specified change notification queue.

        Until request is disconnected.

        """
        while True:

            if (await request.is_disconnected()):
                break

            try:
                item = queue_notify.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.001)
                continue
            yield item

    #--------------------------------------------------------------------------
    async def _websocket_handler(websocket, callback):
        """
        Handle websocket communications using the specified callback.

        """
        await websocket.accept()
        while True:
            message = await websocket.receive_text()
            reply   = callback(message)
            await websocket.send_text(reply)
        await websocket.close()

    #--------------------------------------------------------------------------
    def _load_callback(media_type, content):
        """
        Load the specified callback function.

        """
        return dill.loads(content)

    #--------------------------------------------------------------------------
    def _get_cookies(request):
        """
        Get cookies from the specified request.

        """
        if request is None:
            id_session = uuid.uuid4()
            id_user    = uuid.uuid4()
        else:
            map_cookie = getattr(request, 'cookies', dict())
            id_session = map_cookie.get(_ID_COOKIE_SESSION, uuid.uuid4())
            id_user    = map_cookie.get(_ID_COOKIE_USER,    uuid.uuid4())
        return (id_session, id_user)

    #--------------------------------------------------------------------------
    def _set_cookies(response, id_session, id_user):
        """
        Set cookies on the specified response.

        """
        response.set_cookie(_ID_COOKIE_SESSION, id_session,
                            max_age  = 43000,    # About 12 hours
                            secure   = False,    # TODO: FIX HTTPS
                            httponly = True,
                            samesite = 'strict')
        response.set_cookie(_ID_COOKIE_USER, id_user,
                            max_age  = 32000000, # About a year.
                            secure   = False,    # TODO: FIX HTTPS
                            httponly = True,
                            samesite = 'strict')

    # Give the ASGI process a
    # meaningful process title.
    #
    title_parent = setproctitle.getproctitle()
    title_child  = '{prefix}.asgi_server'.format(prefix = title_parent)
    setproctitle.setproctitle(title_child)

    # Configure generic routes for
    # serving resources that are
    # generated upstream elsewhere
    # in the system.
    #
    WSock = starlette.routing.WebSocketRoute
    Route = starlette.routing.Route
    verbs = ['GET', 'POST']
    list_routes = [WSock('/ws/{id_resource}', handle_route),
                   Route('/{id_resource}',    handle_route, methods = verbs),
                   Route('/',                 handle_route, methods = verbs)]

    exceptions  = {204: handle_route,
                   404: handle_route,
                   500: handle_route}

    list_middleware = [starlette.middleware.Middleware(
                              starlette.middleware.sessions.SessionMiddleware,
                              secret_key = cfg['sessionsecret'])]

    app = starlette.applications.Starlette(debug              = True,
                                           routes             = list_routes,
                                           exception_handlers = exceptions,
                                           middleware         = list_middleware)

    # Map from id_resource to id_topic
    # When a resource changes, this is
    # used to determine which queries
    # need to be notified.
    #
    app.state.map_resource_to_topic = collections.defaultdict(set)
    app.state.map_topic_to_resource = collections.defaultdict(set)
    app.state.map_topic_to_queue    = collections.defaultdict(set)

    # Map from id_resource to resource
    app.state.map_resources = dict()

    for (key, value) in map_queues.items():
        setattr(app.state, key, value)
    app.state.ts_last_update = 0.0
    app.state.default        = _DEFAULT_DOC

    host         = cfg.get('host',          '0.0.0.0')
    port         = cfg.get('port',          '8080')
    ssl_keyfile  = cfg.get('ssl_keyfile',   None)
    ssl_certfile = cfg.get('ssl_certfile',  None)
    log_level    = cfg.get('debug_level',   logging.WARNING)
    debug        = cfg.get('debug',         False)
    has_keyfile  = ssl_keyfile  is not None
    has_certfile = ssl_certfile is not None
    has_https    = has_keyfile and has_certfile

    try:
        if has_https:
            uvicorn.run(app, host         = host,
                             port         = port,
                             ssl_keyfile  = ssl_keyfile,
                             ssl_certfile = ssl_certfile,
                             log_level    = log_level)
        else:
            uvicorn.run(app, host         = host,
                             port         = port,
                             log_level    = log_level)
    except Exception as err:
        raise