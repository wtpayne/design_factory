# -*- coding: utf-8 -*-
"""
Module of utilities to support various logging operations.

"""


import os
import sys

import loguru


logger = loguru.logger


# -----------------------------------------------------------------------------
def setup(cfg_host   = None,
          id_system  = 'stableflow',
          id_host    = 'localhost',
          id_process = 'main_process'):
    """
    Configure the module level logger object.

    """

    log_level   = 'WARNING'
    dirpath_log = None

    if cfg_host is not None:
        if 'log_level' in cfg_host:
            log_level   = cfg_host['log_level']
        if 'dirpath_log' in cfg_host:
            dirpath_log = cfg_host['dirpath_log']

    global logger  # pylint: disable=C0103,W0603
    logger.remove()
    logger.add(sys.stderr,
               level     = log_level,
               backtrace = False)

    if dirpath_log is not None:
        id_system    = id_system
        filename_log = '{sys}_{proc}.log'.format(sys  = id_system,
                                                 proc = id_process)
        filepath_log = os.path.join(dirpath_log, filename_log)
        logger.add(filepath_log,
                   rotation  = '100 MB',
                   level     = log_level,
                   backtrace = False)
