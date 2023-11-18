# -*- coding: utf-8 -*-
"""
---

title:
    "File watching and reading module."

description:
    "This module contains functionality for
    watching one or more directory trees for
    changes and then outputting the path and
    content of any changed files."

id:
    "e184defe-00c2-41b8-807c-4404803eca79"

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


import collections
import functools
import hashlib
import itertools
import multiprocessing
import os
import queue
import re
import sys
import time

import watchdog.events
import watchdog.observers

# import cl.design.nonconformity


# -----------------------------------------------------------------------------
def gen_list_fileinfo(iter_dirpath_root,
                      iter_pathincl,
                      iter_pathexcl,
                      iter_direxcl,
                      iter_read_as_txt,
                      iter_read_as_bin,
                      size_batch,
                      do_output_all,
                      do_repeat_all,
                      do_output_modified,
                      do_terminate_when_done):
    """
    Yield a sequence of file information lists matching the specified criteria.

    """

    build_fileinfo = functools.partial(
                        _build_fileinfo,
                        regex_read_as_txt = _combine_regex(iter_read_as_txt),
                        regex_read_as_bin = _combine_regex(iter_read_as_bin))

    for list_filepath in _gen_list_filepath(iter_dirpath_root,
                                            iter_pathincl,
                                            iter_pathexcl,
                                            iter_direxcl,
                                            size_batch,
                                            do_output_all,
                                            do_repeat_all,
                                            do_output_modified,
                                            do_terminate_when_done):
        yield [build_fileinfo(filepath) for filepath in list_filepath]


# -----------------------------------------------------------------------------
def _build_fileinfo(filepath, regex_read_as_txt, regex_read_as_bin):
    """
    Return a file info structure that corresponds to the specified filepath.

    """

    fileinfo = dict()
    fileinfo['filepath']           = filepath
    fileinfo['list_nonconformity'] = list()
    fileinfo['metadata']           = dict()

    fileinfo = _update_with_basic_metadata(fileinfo)

    if regex_read_as_txt.match(filepath) is not None:
        fileinfo = _update_with_content_as_string(fileinfo)

    if regex_read_as_bin.match(filepath) is not None:
        fileinfo = _update_with_content_as_bytes(fileinfo)

    fileinfo = _update_metadata_with_hexdigest(fileinfo)

    return fileinfo


# -----------------------------------------------------------------------------
def _update_with_basic_metadata(fileinfo):
    """
    Update fileinfo with basic metadata

    """

    filepath = fileinfo['filepath']
    metadata = fileinfo['metadata']

    # File size in bytes.
    #
    metadata['size'] = os.path.getsize(filepath)

    # Last modified time in seconds
    # since Unix epoch. (1 Jan 1970).
    #
    metadata['last_modified'] = os.path.getmtime(filepath)

    # Creation time in seconds since
    # Unix epoch. (1 Jan 1970).
    #
    metadata['created'] = os.path.getctime(filepath)

    return fileinfo


# -----------------------------------------------------------------------------
def _update_with_content_as_string(fileinfo):
    """
    Update fileinfo with text data read from disk.

    """

    filepath     = fileinfo['filepath']
    bytes_buffer = None

    with open(filepath, 'rb') as file:

        try:
            bytes_buffer = file.read()

        except (IOError, OSError) as err:
            id_nc = 'file_not_readable'
            # id_nc = cl.design.nonconformity.nc000_file_not_readable
            nonconformity = {'reporter': __name__,
                             'id_nc':    id_nc,
                             'str_msg':  str(err),
                             'filepath': filepath,
                             'line':     None,
                             'col':      None}
            fileinfo['list_nonconformity'].append(nonconformity)

        # Break early if we couldn't read the file.
        #
        if bytes_buffer is None:
            return fileinfo

        try:
            fileinfo['text'] = bytes_buffer.decode('utf-8')

        except ValueError as err:
            id_nc = cl.design.nonconformity.nc001_file_not_decodable
            nonconformity = {'reporter': __name__,
                             'id_nc':    id_nc,
                             'str_msg':  str(err),
                             'filepath': filepath,
                             'line':     None,
                             'col':      None}
            fileinfo['list_nonconformity'].append(nonconformity)

    return fileinfo


# -----------------------------------------------------------------------------
def _update_with_content_as_bytes(fileinfo):
    """
    Update fileinfo with binary data read from disk.

    """

    with open(fileinfo['filepath'], 'rb') as file:

        try:
            fileinfo['bytes'] = file.read()

        except (IOError, OSError) as err:
            id_nc = cl.design.nonconformity.nc000_file_not_readable
            nonconformity = {'reporter': __name__,
                             'id_nc':    id_nc,
                             'str_msg':  str(err),
                             'filepath': filepath,
                             'line':     None,
                             'col':      None}
            fileinfo['list_nonconformity'].append(nonconformity)

    return fileinfo


# -----------------------------------------------------------------------------
def _update_metadata_with_hexdigest(fileinfo):
    """
    Update fileinfo metadata with hexdigest computed from file content.

    """

    if 'bytes' in fileinfo:
        byte_buffer = fileinfo['bytes']
    elif 'text' in fileinfo:
        byte_buffer = fileinfo['text'].encode('utf-8')
    else:
        byte_buffer = None

    if byte_buffer is not None:
        hasher = hashlib.sha256()
        hasher.update(byte_buffer)
        hexdigest = hasher.hexdigest()
    else:
        hexdigest = ''

    fileinfo['metadata']['hexdigest'] = hexdigest
    return fileinfo


# -----------------------------------------------------------------------------
def _combine_regex(iter_regex = None, op = '|'):
    """
    Return a regular expression compiled from an iterable of strings.

    The supplied strings are combined using the
    supplied operator and then compiled into a
    single regular expression object and
    returned.

    """

    if not iter_regex:
        return re.compile('(?!x)x')  # Will never match anything

    str_delim = '){op}('.format(op = op)
    str_inner = str_delim.join(iter_regex)
    str_regex = '({inner})'.format(inner = str_inner)
    obj_regex = re.compile(str_regex)

    return obj_regex


# -----------------------------------------------------------------------------
def _gen_list_filepath(iter_dirpath_root,
                       iter_pathincl          = None,
                       iter_pathexcl          = None,
                       iter_direxcl           = None,
                       size_batch             = 10,
                       do_output_all          = False,
                       do_repeat_all          = False,
                       do_output_modified     = False,
                       do_terminate_when_done = False):
    """
    Yield a sequence of filepath lists matching the specified criteria.

    In each batch, recently modified files are
    output first, followed by all other files.
    It is possible for duplicate filepaths to
    be output when the file changes at the same
    time as it is visited by the 'all' reader.

    The length of each yielded filepath_list
    should always be less than or equal to
    the specified size_batch parameter.

    """

    # gen_filepath_mod either yields
    # modified files or repeatedly
    # yields None if no modified
    # files are found.
    #
    gen_filepath_mod = _generate_filepath_modified(
                                        do_output_modified = do_output_modified,
                                        iter_dirpath_root  = iter_dirpath_root,
                                        iter_pathincl      = iter_pathincl,
                                        iter_pathexcl      = iter_pathexcl,
                                        iter_direxcl       = iter_direxcl)

    # gen_filepath_all yields all files,
    # modified or not. Once all matching
    # files have been yielded then it
    # either goes back to the beginning
    # and repeats the process, or starts
    # to repeatedly yield None instead,
    # depending on the value of
    # do_repeat_all.
    #
    gen_filepath_all = _generate_filepath_all(
                                        do_output_all     = do_output_all,
                                        do_repeat_all     = do_repeat_all,
                                        iter_dirpath_root = iter_dirpath_root,
                                        iter_pathincl     = iter_pathincl,
                                        iter_pathexcl     = iter_pathexcl,
                                        iter_direxcl      = iter_direxcl)

    do_terminate = False
    while True:

        if do_terminate_when_done and do_terminate:
            break

        list_filepath = list()

        # Try to fill list_filepath with as
        # many modified files as possible.
        #
        while True:

            is_full = len(list_filepath) >= size_batch
            if is_full:
                break

            try:
                filepath        = next(gen_filepath_mod)
            except StopIteration:
                is_done_for_now = True
            else:
                is_done_for_now = filepath is None

            if not is_done_for_now:
                list_filepath.append(filepath)
                continue
            else:
                # Do NOT set do_terminate as we
                # may still see changed files
                # in future.
                break

        # Try to fill any empty space
        # remaining in list_filepath
        # with as many unmodified files
        # as possible. If the unmodified
        # files are exhausted then
        # apply the termination
        # criterion.
        #
        while True:

            is_full = len(list_filepath) >= size_batch
            if is_full:
                break

            try:
                filepath = next(gen_filepath_all)
            except StopIteration:
                is_done = True
            else:
                is_done = filepath is None

            if not is_done:
                list_filepath.append(filepath)
                continue
            else:
                do_terminate = True
                break

        yield list_filepath


# -----------------------------------------------------------------------------
def _generate_filepath_all(do_output_all,
                           do_repeat_all,
                           iter_dirpath_root,
                           iter_pathincl = None,
                           iter_pathexcl = None,
                           iter_direxcl  = None):
    """
    Yield paths of matching files from the list of roots, repeating if needed.

    Continue repeatedly if configured to do so,
    otherwise fall back to yielding None forever
    after all matching files have been found and
    yielded.

    This generator has the slightly odd behaviour
    of yielding None forever as a 'final' state.

    This is done intentionally so that the
    behavior of this generator matches that of
    the _generate_filepath_modified generator
    when no modified files are found.

    This enables the calling function to use
    very similar logic for both cases,
    simplifying the otherwise very confusing
    logic in that top-level function.

    """

    if do_output_all:

        while True:
            for filepath in _generate_filepath_all_once(
                                         iter_dirpath_root = iter_dirpath_root,
                                         iter_pathincl     = iter_pathincl,
                                         iter_pathexcl     = iter_pathexcl,
                                         iter_direxcl      = iter_direxcl):
                yield filepath
            if do_repeat_all:
                continue
            else:
                break

    # Yield None forever once
    # we are done searching
    # the filesystem.
    #
    while True:
        yield None


# -----------------------------------------------------------------------------
def _generate_filepath_all_once(iter_dirpath_root,
                                iter_pathincl = None,
                                iter_pathexcl = None,
                                iter_direxcl  = None):
    """
    Yield paths of matching files from the list of roots, stopping when done.

    """

    list_generator = list()
    for dirpath_root in iter_dirpath_root:
        list_generator.append(
            _filtered_filepath_generator(dirpath_root,
                                         iter_pathincl = iter_pathincl,
                                         iter_pathexcl = iter_pathexcl,
                                         iter_direxcl  = iter_direxcl))
    return itertools.chain.from_iterable(list_generator)



# -----------------------------------------------------------------------------
def _filtered_filepath_generator(dirpath_root,
                                 iter_pathincl = None,
                                 iter_pathexcl = None,
                                 iter_direxcl  = None):

    """
    Yield each matching file in the directory tree under dirpath_src.

    """

    re_pathincl = _combine_regex(iter_regex = iter_pathincl, op = '|')
    re_pathexcl = _combine_regex(iter_regex = iter_pathexcl, op = '|')
    re_direxcl  = _combine_regex(iter_regex = iter_direxcl,  op = '|')
    os_walk     = os.walk(dirpath_root,
                          topdown     = True,
                          onerror     = None,
                          followlinks = False)

    for (dirpath, list_dirname, iter_filename) in os_walk:

        # Keep for further consideration only
        # those directories which do not match
        # the directory-exclusion regex.
        #
        list_dirname_ok = []
        for dirname in list_dirname:
            is_included = re_direxcl.match(dirname) is None
            if is_included:
                list_dirname_ok.append(dirname)
        list_dirname[:] = sorted(list_dirname_ok)

        for filename in iter_filename:
            filepath = os.path.join(dirpath, filename)

            is_excluded = re_pathexcl.match(filepath) is not None
            if is_excluded:
                continue

            is_included = re_pathincl.match(filepath) is not None
            if is_included:
                yield filepath



# -----------------------------------------------------------------------------
def _generate_filepath_modified(do_output_modified,
                                iter_dirpath_root,
                                iter_pathincl = None,
                                iter_pathexcl = None,
                                iter_direxcl  = None):
    """
    Yield filepaths of recently modified matching files.

    """

    if not do_output_modified:
        return itertools.repeat(None)

    re_pathincl = _combine_regex(iter_regex = iter_pathincl, op = '|')
    re_pathexcl = _combine_regex(iter_regex = iter_pathexcl, op = '|')
    re_direxcl  = _combine_regex(iter_regex = iter_direxcl,  op = '|')

    list_tup_observer_handler = _list_tup_observer_handler(iter_dirpath_root)

    while True:
        list_path = list()
        for (observer, handler) in list_tup_observer_handler:
            for filepath in _modified_files(handler):

                # Check to see if the modified
                # filepath is excluded (or not
                # included) according to the
                # two whole-path filters.
                #
                is_path_excluded = re_pathexcl.match(filepath) is not None
                is_path_included = re_pathincl.match(filepath) is not None
                if is_path_excluded or (not is_path_included):
                    continue

                # Check to see if any of the
                # directory names in the
                # filepath are excluded by
                # the directory-name filter.
                #
                dirpath             = os.path.dirname(filepath)
                iter_dirname        = dirpath.split(os.sep)
                is_dirname_excluded = False
                for dirname in iter_dirname:
                    is_dirname_excluded = re_direxcl.match(dirname) is not None
                    if is_dirname_excluded:
                        break
                if is_dirname_excluded:
                    continue

                list_path.append(filepath)

        if list_path:
            for filepath in sorted(list_path):
                yield filepath
        else:
            yield None


# -----------------------------------------------------------------------------
def _list_tup_observer_handler(iter_dirpath_root):
    """
    Return a list of change-observer, change-handler tuple pairs.

    """

    list_tup_observer_handler = list()
    for dirpath_root in iter_dirpath_root:
        observer  = watchdog.observers.Observer()
        handler   = EventEnqueueingHandler()
        observer.schedule(event_handler = handler,
                          path          = dirpath_root,
                          recursive     = True)
        observer.start()
        list_tup_observer_handler.append((observer, handler))
    return list_tup_observer_handler


# -----------------------------------------------------------------------------
def _modified_files(handler):
    """
    Return a list of modified files from the specified event handler.

    """

    list_filepath  = list()
    list_tup_event = handler.get()
    for tup_event in list_tup_event:

        if tup_event.is_dir:
            continue

        if tup_event.path_dst is not None:
            list_filepath.append(tup_event.path_dst)
            continue

        if tup_event.path_src is not None:
            list_filepath.append(tup_event.path_src)
            continue

    return list_filepath


# =============================================================================
TupEvent = collections.namedtuple(
                        'TupEvent', ['type', 'path_src', 'path_dst', 'is_dir'])


# =============================================================================
class EventEnqueueingHandler(watchdog.events.FileSystemEventHandler):
    """
    Enqueues watchdog filesystem events for stableflow to pick up.

    """

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Construct a EventEnqueueingHandler instance.

        """

        super(EventEnqueueingHandler, self).__init__()
        self.queue = multiprocessing.Queue()


    # -------------------------------------------------------------------------
    def on_moved(self, event):
        """
        Dispatch watchdog.events.FileMovedEvent events.

        """

        super(EventEnqueueingHandler, self).on_moved(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def on_created(self, event):
        """
        Dispatch watchdog.events.FileCreatedEvent events.

        """

        super(EventEnqueueingHandler, self).on_created(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def on_deleted(self, event):
        """
        Dispatch watchdog.events.FileDeletedEvent events.

        """

        super(EventEnqueueingHandler, self).on_deleted(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def on_modified(self, event):
        """
        Dispatch watchdog.events.FileModifiedEvent events.

        """

        super(EventEnqueueingHandler, self).on_modified(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def _enqueue(self, event):
        """
        Add the specified event to the queue.

        """

        path_src = None
        path_dst = None
        is_dir   = False

        if hasattr(event, 'src_path'):
            if event.src_path:
                path_src = event.src_path

        if hasattr(event, 'dest_path'):
            if event.dest_path:
                path_dst = event.dest_path

        if hasattr(event, 'is_directory'):
            if event.is_directory:
                is_dir = event.is_directory

        tup_event = TupEvent(type     = event.event_type,
                             path_src = path_src,
                             path_dst = path_dst,
                             is_dir   = is_dir)
        self.queue.put(tup_event, block = False)

    # -------------------------------------------------------------------------
    def get(self):
        """
        Get all events currently on the queue.

        """

        set_tup_event = set()
        while True:

            try:
                set_tup_event.add(self.queue.get(block = False))
            except queue.Empty:
                break

        list_tup_event = list(set_tup_event)

        return list_tup_event
