# -*- coding: utf-8 -*-
"""
---

title:
    "Metric logging support module."

description:
    "This Python module is designed to support
    metric logging."

id:
    "42e44473-3350-4b6c-94f2-d6cc99469062"

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


import appdirs
import logging
import os.path
import sqlite3

import fl.util



# -----------------------------------------------------------------------------
@fl.util.coroutine
def writer(id_system, dirpath_log = None):
    """
    Coroutine for writing metric log items to a persistent store.

    """

    # Create a directory for the metric log file.
    # If the dirpath is not provided, then we use
    # the appdirs library to generate a platform
    # the appdirs library to generate a platform
    # system specific default path. On Unix
    # platforms this will be:
    #
    #   ~/.local/share/{id_system}/
    #
    if dirpath_log is None:
        dirpath_log = appdirs.user_data_dir(appname = id_system)

    # Create the directory where the event logs
    # are going to be stored. If we cannot create
    # the directory then we consider that to
    # be a critical (nonrecoverable) error, so
    # we signal the system to shut down by
    # raising an exception.
    #
    try:
        os.makedirs(dirpath_log, exist_ok = True)
    except OSerror as err:
        raise RuntimeError(
            'Critical error creating directory "{dirpath}": {err}'.format(
                                                        dirpath = dirpath_log,
                                                        err     = err))

    filename_log = 'log_metric.db'
    filepath_log = os.path.join(dirpath_log, filename_log)
    connection   = sqlite3.connect(filepath_log)
    cursor       = connection.cursor()

    cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS
                    log_metric (created TIMESTAMP,
                                id      TEXT,
                                value   REAL);
                """)

    cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS
                    log_metric_created_idx
                ON
                    log_metric (created);
                """)

    connection.commit()

    while True:

        (event) = yield (None)

        cursor.execute(
                    """
                    INSERT INTO log_metric (created,
                                            id,
                                            value)
                    VALUES (?, ?, ?)
                    """,
                    (event['created'],
                     event['id'],
                     event['value']))

        connection.commit()
