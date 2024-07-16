# -*- coding: utf-8 -*-
"""
----

title:
    "Track logic module."

description:
    "This module contains track logic for
    the harmonica bot."

id:
    "2ad7c8fb-49f7-4f2a-b200-99568e35eccc"

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


import asyncio
import collections
import logging
import os
import os.path
import pprint
import sqlite3
import typing

import dill
import pydantic
import sqlitedict

import t000_wtp.harmonica as harmonica


# =============================================================================
class Table():
    """
    Track table

    """

    _proxy_bot: typing.Any
    _db:        typing.Union[None, sqlitedict.SqliteDict] = None
    _map_track: dict = {}
    _map_queue: dict = {}

    # -------------------------------------------------------------------------
    def __init__(self, proxy_bot):
        """
        Return an instance of the track table.

        """

        self._proxy_bot   = proxy_bot
        dirpath_self      = os.path.dirname(os.path.realpath(__file__))
        dirpath_parent    = os.path.join(dirpath_self, '..')
        filename_db       = 'track.db'
        filepath_default  = os.path.join(dirpath_parent, filename_db)
        filepath_db_track = os.getenv('HARMONICA_FILEPATH_DB_TRACK',
                                      default = filepath_default)
        self._db          = sqlitedict.SqliteDict(filepath_db_track,
                                                  encode = dill.dumps,
                                                  decode = dill.loads)

    # -------------------------------------------------------------------------
    def close(self, do_commit = False):
        """
        Close DB connections and prevent class from being used again.

        """

        if self._db is None:
            return

        if self._db.conn is None:
            self._db = None
            return

        has_commit_error = False
        try:
            if do_commit:
                self._db.commit()
        except sqlite3.Error as err:
            has_commit_error = True
            logging.error(err)
            raise
        finally:
            try:
                self._db.close()
            except sqlite3.Error as err:
                logging.error(err)
                if not has_commit_error:
                    raise
            finally:
                self._db = None

    # -------------------------------------------------------------------------
    def load(self, update, context):
        """
        Load a track from the database.

        """

        id_chat  = update.effective_chat.id
        id_track = f'tg.{id_chat}'

        try:
            return self._map_track[id_track]
        except KeyError:
            pass

        try:
            state = self._db[id_track]
        except KeyError:
            state = State()

        queue = asyncio.Queue()
        coro  = self._proxy_bot.app.create_task(
                                        self._coro(queue = queue,
                                                   chat  = self.chat))


        return Track(queue   = queue,
                     coro    = coro,
                     update  = update,
                     context = context,
                     state   = state)


# =============================================================================
class Track():
    """
    Track class.

    """

    bot:     typing.Any
    update:  typing.Any
    context: typing.Any
    state:   typing.Any


    # -------------------------------------------------------------------------
    def __init__(self, bot, update, context, state):
        """
        Return a Track instance.

        """

        self.bot     = bot
        self.update  = update
        self.context = context
        self.state   = state


    # -------------------------------------------------------------------------
    def commit(self):
        """
        """

        # self._track_table.db.commit()
        pass


# =============================================================================
class State():
    """
    Track state class.

    """

    pass


