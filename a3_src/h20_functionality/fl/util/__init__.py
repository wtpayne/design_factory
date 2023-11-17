# -*- coding: utf-8 -*-
"""
---

title:
    "Utility package."

description:
    "This package contains various bits of
    general purpose utility functionality."

id:
    "b34331cb-926d-4efa-aa88-0797b7067ed3"

type:
    dt002_python_package

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
import collections.abc
import contextlib
import hashlib
import importlib
import pprint
import time

import fl.util.alg
import fl.util.io


# Command used by Bureau and BureauEngine to mutate state.
#
Command = collections.namedtuple(
    typename    = 'Command',
    field_names = ('operation', 'idx', 'time_utc', 'path', 'value_new', 'value_old'),
    defaults    = ('edit',      0,     0.0,        '',     None,        None))


# Rule used by Bureau and BureauEngine to filter and modify commands.
#
Rule = collections.namedtuple(
    typename    = 'Rule',
    field_names = ('cond', 'act'))


# =============================================================================
class Bureau(collections.abc.MutableMapping):
    """
    Custom dictionary class intended to help manage application state.

    """

    # Instance private attributes
    # are given special handling
    # so they don't get treated
    # as regular keys.
    #
    _bureau_attributes = ('_bureau_attributes',
                          '_bureau_data',
                          '_bureau_engine',
                          '_bureau_path',
                          '_bureau_path_delimiter')

    # -------------------------------------------------------------------------
    def __init__(self,
                 filepath        = None,
                 _engine         = None,
                 _path           = None,
                 _path_delimiter = '.'):
        """
        Returns a new Bureau instance.

        The Bureau class defines a container
        that conforms to the standard library
        dictionary interface and whose instances
        are intended to be used as nodes in a
        larger tree structured hierarchical data
        store.

        The Bureau class supports both dict-like
        and attribute-like field access. Keys
        can be both atomic keys, dot-delimited
        string paths, or tuple paths. When keys
        are path-like in form, they are used to
        access data structures which are nested
        under the current instance.

        Each overall tree maintains unitary
        edit/undo histories and supports simple
        undo and redo functionality.

        Each tree also maintains unitary rule
        tables and supports rule registration
        for responding to changes.

        """

        # The path delimiter (normally '.'') is
        # used to delimit string paths.
        #
        self._bureau_path_delimiter = _path_delimiter

        # The path is the path to the current
        # node in the tree. This is stored
        # internally as a tuple of strings.
        #
        if _path is None:
            self._bureau_path = tuple()
        else:
            self._bureau_path = _path

        # The engine handles undo/redo and
        # callbacks. There is a single engine
        # for each tree. All nodes in the tree
        # have a reference to it.
        #
        if _engine is None:
            self._bureau_engine = BureauEngine(bureau = self)
        else:
            self._bureau_engine = _engine

        # Bureau data is the underlying datastore
        # for this node in the overall tree.
        #
        self._bureau_data = dict()
        if filepath is not None:
            with self.batch_context():
                self.from_file(filepath  = filepath,
                               str_format = None,
                               path_root  = self._bureau_path)

    # -------------------------------------------------------------------------
    def __getstate__(self):
        """
        Return a dictionary that represents the Bureau instance state.

        """
        return {
            '_bureau_path_delimiter': self._bureau_path_delimiter,
            '_bureau_path':           self._bureau_path,
            '_bureau_engine':         self._bureau_engine,
            '_bureau_data':           self._bureau_data,
        }

    # -------------------------------------------------------------------------
    def __setstate__(self, state):
        """
        Update the Bureau instance state to match the provided dictionary.

        """

        self._bureau_path_delimiter = state['_bureau_path_delimiter']
        self._bureau_path           = state['_bureau_path']
        self._bureau_engine         = state['_bureau_engine']
        self._bureau_data           = state['_bureau_data']

    # -------------------------------------------------------------------------
    def _str_path(self):
        """
        Return a delimited string representation of the path.

        """

        return self._bureau_path_delimiter.join(self._bureau_path)


    # -------------------------------------------------------------------------
    def reset_engine(self, path = None, engine = None):
        """
        Disconnect this Bureau from it's engine and replace with a new one.

        We need to do this, for example, when
        separating a subtree from the main
        tree.

        """

        if engine is None:
            self._bureau_engine = BureauEngine(bureau = self)
        else:
            self._bureau_engine = engine

        if path is None:
            self._bureau_path = tuple()
        else:
            self._bureau_path = path

    # -------------------------------------------------------------------------
    def to_tuple(self):
        """
        Return a representation of self as a key-value tuple.

        Note that recursive structures and non-
        traversable data types are NOT supported.

        """

        return tuple(fl.util.alg.walk(obj            = self,
                                      gen_leaf       = True,
                                      gen_path       = True,
                                      gen_obj        = True,
                                      use_fat_leaves = True))

    # -------------------------------------------------------------------------
    def from_tuple(self, tup_kv, path_root = tuple()):
        """
        Update Bureau from a key-value tuple.

        """

        if path_root:
            tup_path_root = tuple(_iter_path(
                                        path  = path_root,
                                        delim = self._bureau_path_delimiter))
        else:
            tup_path_root = self._bureau_path

        for (tup_path, value) in tup_kv:
            self._bureau_engine.set_item(path      = tup_path_root + tup_path,
                                         value_new = value)

    # -------------------------------------------------------------------------
    def to_dict(self):
        """
        Return a representation of self as a nested dict.

        This function converts the current Bureau
        instance into a nested dictionary
        representation.

        This method traverses the object using
        the `walk` utility function (via the
        to_tuple method), which generates length
        two tuples where the first element is a
        path indicating a location in the Bureau
        and the second element is the value at
        that path location.

        For each path-value pair, this method
        creates nested dictionaries within the
        output dictionary according to the path,
        and sets the innermost dictionary's value
        according to the value.

        The resulting dictionary has the same
        nested structure as the original object,
        and can be used for purposes like
        serialization.

        :returns:   A nested dictionary representation of the object. The
                    keys in the dictionary correspond to the paths in the
                    object, and the values in the dictionary correspond
                    to the values in the object.

        """

        return tup_path_val_to_dict(tup_path_val = self.to_tuple())

    # -------------------------------------------------------------------------
    def from_dict(self, map_item, path_root = tuple()):
        """
        Load Bureau from a nested dict.

        """

        return self.from_tuple(path_root = path_root,
                               tup_kv    = fl.util.alg.walk(
                                                    obj            = map_item,
                                                    gen_leaf       = True,
                                                    gen_path       = True,
                                                    gen_obj        = True,
                                                    use_fat_leaves = True))

    # -------------------------------------------------------------------------
    def from_file(self, filepath, str_format = None, path_root = tuple()):
        """
        Load data into the Bureau from the specified file.

        """

        (map_data, map_error) = fl.util.io.load_from_filepath(
                                                    filepath   = filepath,
                                                    str_format = str_format)
        if map_error is None:
            self.from_dict(path_root = path_root,
                           map_item  = map_data)

    # -------------------------------------------------------------------------
    def to_file(self, filepath, str_format = None):
        """
        Save data from the Bureau to the specified file.

        """

        fl.util.io.save_to_filepath(self.to_dict(), filepath, str_format)

    # -------------------------------------------------------------------------
    def pprint(self):
        """
        Pretty print the bureau.

        """

        pprint.pprint(self.to_dict())

    # -------------------------------------------------------------------------
    def __contains__(self, item):
        """
        Return true if item is in self, false otherwise.

        """

        return self._bureau_data.__contains__(item)

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Gets the value for the specified key.

        """

        return self._bureau_engine.get_item(path = self._tup_full_path(key))

    # -------------------------------------------------------------------------
    def __setitem__(self, key, value):
        """
        Sets a key-value pair.

        """

        self._bureau_engine.set_item(path      = self._tup_full_path(key),
                                     value_new = value)

        return None

    # -------------------------------------------------------------------------
    def __delattr__(self, key):
        """
        Delete the specified key.

        """

        self._bureau_engine.del_item(path = self._tup_full_path(key))

        return None

    # -------------------------------------------------------------------------
    def __delitem__(self, key):
        """
        Delete the specified key.

        """

        self._bureau_engine.del_item(path = self._tup_full_path(key))

        return None

    # -------------------------------------------------------------------------
    def __iter__(self):
        """
        Return an iterator over elements in the Bureau.

        """

        return self._bureau_data.__iter__()

    # -------------------------------------------------------------------------
    def __len__(self):
        """
        Return the number of elements in the Bureau.

        """

        return self._bureau_data.__len__()

    # -------------------------------------------------------------------------
    def __setattr__(self, key, value):
        """
        Sets a key-value pair.

        """

        if key in Bureau._bureau_attributes:
            super().__setattr__(key, value)
        else:
            self.__setitem__(key, value)

        return None

    # -------------------------------------------------------------------------
    def __getattr__(self, key):
        """
        Gets the value for the specified key.

        """

        return self.__getitem__(key)

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Return a string representation of the Bureau.

        """

        list_kv = list()
        for (key, value) in self._bureau_data.items():

            if isinstance(key, str):
                key = repr(key)
            else:
                key = str(key)

            if isinstance(value, str):
                value = repr(value)
            else:
                value = str(value)

            list_kv.append('{k}: {v}'.format(k = key, v = value))

        return '{' + ', '.join(list_kv) + '}'

    # -------------------------------------------------------------------------
    def undo(self):
        """
        Undo the last edit in the bureau engine edit history.

        """

        return self._bureau_engine.undo()

    # -------------------------------------------------------------------------
    def redo(self):
        """
        Redo the last undo in the bureau engine undo history.

        """

        return self._bureau_engine.redo()

    # -------------------------------------------------------------------------
    def rule(self,
             rule     = None,
             cond     = None,
             act      = None,
             tup_path = None):
        """
        Add a rule to the bureau engine.

        """

        if tup_path is None:
            tup_path = self._bureau_path

        return self._bureau_engine.rule(rule     = rule,
                                        cond     = cond,
                                        act      = act,
                                        tup_path = tup_path)

    # -------------------------------------------------------------------------
    def _tup_full_path(self, key):
        """
        Return the full path to the specified key as a tuple.

        """

        iter_branch = _iter_path(key, self._bureau_path_delimiter)

        return self._bureau_path + tuple(iter_branch)

    # -------------------------------------------------------------------------
    @contextlib.contextmanager
    def batch_context(self):
        """
        Context manager for processing updates as a batch.

        """

        batch = self.batch_init()

        try:

            yield batch

        except Exception as err:

            raise # We might want to rollback changes here if there is a need.

        finally:

            self.batch_finalize(batch)

    # -------------------------------------------------------------------------
    def batch_init(self):
        """
        Initialize the batch.

        """

        self._bureau_engine._journal.clear()
        self._bureau_engine._do_keep_journal = True
        batch = list()
        return batch

    # -------------------------------------------------------------------------
    def batch_finalize(self, batch):
        """
        Finalize the batch.

        """

        self._bureau_engine._do_keep_journal = False
        batch[:] = self._bureau_engine._journal

        self._bureau_engine._invoke_rules(batch)

        self._bureau_engine._journal.clear()

    # -------------------------------------------------------------------------
    def from_batch(self, batch):
        """
        Update the Bureau using the specified journal segment.

        """

        for tup_cmd in batch:
            cmd = Command._make(tup_cmd)
            self._bureau_engine.set_item(path      = cmd.path,
                                         value_new = cmd.value_new,
                                         operation = cmd.operation)

# =============================================================================
class BureauEngine():
    """
    An engine to help run a tree of Bureau objects.

    """

    # -------------------------------------------------------------------------
    def __init__(self, bureau):
        """
        Returns a new BureauEngine instance.

        """

        self._bureau          = bureau
        self._do_keep_journal = False
        self._journal         = list()
        self._cmd_counter     = 0
        self._hist_edit       = list()
        self._hist_undo       = list()
        self._list_rule       = list()

    # -------------------------------------------------------------------------
    def __getstate__(self):
        """
        Return a dictionary that represents the BureauEngine instance state.

        """

        return {
            '_bureau':          self._bureau,
            '_do_keep_journal': self._do_keep_journal,
            '_journal':         self._journal,
            '_cmd_counter':     self._cmd_counter,
            '_hist_edit':       self._hist_edit,
            '_hist_undo':       self._hist_undo,
            '_list_rule':       self._list_rule
        }

    # -------------------------------------------------------------------------
    def __setstate__(self, state):
        """
        Update the BureauEngine instance state to match the provided dict.

        """

        self._bureau          = state['_bureau']
        self._do_keep_journal = state['_do_keep_journal']
        self._journal         = state['_journal']
        self._cmd_counter     = state['_cmd_counter']
        self._hist_edit       = state['_hist_edit']
        self._hist_undo       = state['_hist_undo']
        self._list_rule       = state['_list_rule']

    # -------------------------------------------------------------------------
    def get_item(self, path):
        """
        Getter implementation.

        """

        # Resolve path.
        #
        cursor      = self._bureau._bureau_data
        path_cursor = tuple()
        for name in _iter_path(path, self._bureau._bureau_path_delimiter):
            path_cursor = path_cursor + (name,)
            cursor      = self._ensure_exists(path_cursor, cursor, name)

        # Invalid path raise KeyError.
        #
        if cursor is self._bureau._bureau_data:
            raise KeyError(repr(path))

        return cursor

    # -------------------------------------------------------------------------
    def del_item(self, path):
        """
        Deleter implementation.

        """

        self.set_item(path = path, value_new = None, operation = 'del')

        return None

    # -------------------------------------------------------------------------
    def set_item(self, path, value_new, operation = None):
        """
        Setter implementation.

        """

        self._hist_edit.append(
                    self._do_update_and_bookkeeping(
                                    Command(operation = operation,
                                            path      = path,
                                            value_new = value_new,
                                            value_old = None)))
        return None

    # -------------------------------------------------------------------------
    def undo(self):
        """
        Get the last edit, reverse it, and store in the undo history.

        """

        if not self._hist_edit:
            return None

        cmd_edit = self._hist_edit.pop()
        self._hist_undo.append(
                    self._do_update_and_bookkeeping(
                                    Command(operation = 'undo',
                                            path      = cmd_edit.path,
                                            value_new = cmd_edit.value_old,
                                            value_old = cmd_edit.value_new)))
        return None

    # -------------------------------------------------------------------------
    def redo(self):
        """
        Get the last undo, reverse it, and store in the edit history.

        """

        if not self._hist_undo:
            return None

        cmd_undo = self._hist_undo.pop()
        self._hist_edit.append(
                    self._do_update_and_bookkeeping(
                                    Command(operation = 'redo',
                                            path      = cmd_undo.path,
                                            value_new = cmd_undo.value_old,
                                            value_old = cmd_undo.value_new)))
        return None

    # -------------------------------------------------------------------------
    def _do_update_and_bookkeeping(self, cmd):
        """
        Update the bureau state and return the completed command.

        The Command named tuple that is returned
        has mostly the same values as the command
        specified by the caller, but with any
        missing values filled in. This will
        include the old value where it isn't
        known beforehand, and the operation name
        when we don't know if we are making an
        'edit' to an existing field or an 'add'
        of a new field.

        This procedure also performs book-keeping
        tasks such as updating the journal and the
        command counter.

        If the command specified by the caller
        affects more than one leaf of the bureau
        tree, then the journal is updated with
        one command for each leaf that is changed.

        This is done so that leaf-specific rules
        will be triggered as expected.

        We call these leaf-specific commands
        'auxiliary' commands, and we call the
        command from which they are derived
        the 'principal' command.

        """

        is_delete = cmd.operation == 'del'
        value_new = cmd.value_new
        value_old = self._do_update(cmd.path, value_new, is_delete)

        # Connect any newly added Bureau subtrees
        # to the engine, and disconnect any newly
        # removed subtrees from the engine.
        #
        # This is to prevent removed subtrees
        # from affecting the original and vice
        # versa.
        #
        if isinstance(value_new, Bureau):
            value_new.reset_engine(path   = cmd.path,
                                   engine = self)

        if isinstance(value_old, Bureau):
            value_old.reset_engine(path   = None,
                                   engine = None)

        # Work out if we are adding a new
        # value or modifying an existing
        # value.
        #
        operation = cmd.operation
        if operation is None:
            if value_old is None:
                operation = 'add'
            else:
                operation = 'edit'

        # If we're not keeping a journal, then
        # we don't need to worry about non-atomic
        # additions and removals. We also
        # don't need to keep track of the command
        # counter or timestamp.
        #
        if not self._do_keep_journal:
            return Command(operation = operation,
                           idx       = None,
                           time_utc  = None,
                           path      = cmd.path,
                           value_new = value_new,
                           value_old = value_old)

        # If both the old and the new values are
        # leaf nodes, then it is an atomic change
        # and we can just journal the principal
        # command as-is.
        #
        time_utc    = time.time()
        is_leaf_new = fl.util.alg.is_leaf(value_new, use_fat_leaves = False)
        is_leaf_old = fl.util.alg.is_leaf(value_old, use_fat_leaves = False)

        is_leaf_replaces_leaf     =      is_leaf_new  and      is_leaf_old
        is_leaf_replaces_branch   =      is_leaf_new  and (not is_leaf_old)
        is_branch_replaces_leaf   = (not is_leaf_new) and      is_leaf_old
        is_branch_replaces_branch = (not is_leaf_new) and (not is_leaf_old)

        if is_leaf_replaces_leaf:

            self._cmd_counter += 1
            idx_cmd            = self._cmd_counter - 1
            cmd_principal      = Command(operation = operation,
                                         idx       = idx_cmd,
                                         time_utc  = time_utc,
                                         path      = cmd.path,
                                         value_new = value_new,
                                         value_old = value_old)
            self._journal.append(cmd_principal)

        elif is_leaf_replaces_branch:

            for (relpath, leaf_old) in fl.util.alg.walk(
                                                    obj         = value_old,
                                                    gen_leaf    = True,
                                                    gen_nonleaf = False,
                                                    gen_path    = True,
                                                    gen_obj     = True):
                self._cmd_counter += 1
                idx_cmd = self._cmd_counter - 1
                self._journal.append(Command(operation = operation,
                                             idx       = idx_cmd,
                                             time_utc  = time_utc,
                                             path      = cmd.path + relpath,
                                             value_new = value_new,
                                             value_old = leaf_old))

        elif is_branch_replaces_leaf:

            # TODO: HANDLE LISTS AND DICTS SEPARATELY
            #       PRESERVE LIST TYPES

            if isinstance(value_new, (tuple, list)):
                pass

            for (relpath, leaf_new) in fl.util.alg.walk(
                                                    obj         = value_new,
                                                    gen_leaf    = True,
                                                    gen_nonleaf = False,
                                                    gen_path    = True,
                                                    gen_obj     = True):
                self._cmd_counter += 1
                idx_cmd = self._cmd_counter - 1
                self._journal.append(Command(operation = operation,
                                             idx       = idx_cmd,
                                             time_utc  = time_utc,
                                             path      = cmd.path + relpath,
                                             value_new = leaf_new,
                                             value_old = value_old))

        elif is_branch_replaces_branch:

            # TODO: HANDLE LISTS AND DICTS SEPARATELY
            #       PRESERVE LIST TYPES

            for (relpath, leaf_old) in fl.util.alg.walk(
                                                    obj         = value_old,
                                                    gen_leaf    = True,
                                                    gen_nonleaf = False,
                                                    gen_path    = True,
                                                    gen_obj     = True):
                self._cmd_counter += 1
                idx_cmd = self._cmd_counter - 1
                self._journal.append(Command(operation = operation,
                                             idx       = idx_cmd,
                                             time_utc  = time_utc,
                                             path      = cmd.path + relpath,
                                             value_new = None,
                                             value_old = leaf_old))

            for (relpath, leaf_new) in fl.util.alg.walk(
                                                    obj         = value_new,
                                                    gen_leaf    = True,
                                                    gen_nonleaf = False,
                                                    gen_path    = True,
                                                    gen_obj     = True):
                self._cmd_counter += 1
                idx_cmd = self._cmd_counter - 1
                self._journal.append(Command(operation = operation,
                                             idx       = idx_cmd,
                                             time_utc  = time_utc,
                                             path      = cmd.path + relpath,
                                             value_new = leaf_new,
                                             value_old = None))

        return Command(operation = operation,
                       idx       = None,
                       time_utc  = None,
                       path      = cmd.path,
                       value_new = value_new,
                       value_old = value_old)

    # -------------------------------------------------------------------------
    def _iter_subtree_leaves(self, path):
        """
        Yield of the existing leaf items under the specified path.

        """

        for (relpath, value) in fl.util.alg.walk(
                                            obj         = self._item_at(path),
                                            gen_leaf    = True,
                                            gen_nonleaf = False,
                                            gen_path    = True,
                                            gen_obj     = True):
            yield (path_cursor + relpath, value)

    # -------------------------------------------------------------------------
    def _item_at(self, path, do_create_missing = False):
        """
        Return a reference to the item at the specified path.

        """

        cursor      = self._bureau._bureau_data
        path_cursor = tuple()
        for name in _iter_path(path, self._bureau._bureau_path_delimiter):
            path_cursor = path_cursor + (name,)
            (get_item, set_item, del_item) = _accessor_functions(cursor)
            cursor = get_item(name)
        return cursor

    # -------------------------------------------------------------------------
    def _do_update(self, tup_path, value_new, is_delete):
        """
        Sets a new value in the specified bureau and returns the old value.

        This function implements the functionality
        of setting a new value at a specified path
        in the data structure.

        This method updates the value at the
        specified path in the bureau's data
        structure with a new value.

        The old value at the specified path is
        returned. If there is no old value (the
        path was not previously in the data
        structure), then None is returned.

        :param tup_path:    A tuple representing the path in the bureau's
                            data structure where the new value is to be set.
                            Each item in the tuple is a key in the data
                            structure, and the sequence of keys represents
                            the path to  the value.

        :param value_new:   The new value to be set at the specified path
                            in the bureau's data structure.

        :returns:           The old value at the specified path, or None
                            if there was no old value.

        :raises KeyError:   If the specified path is not valid (it is an
                            empty tuple).

        :note:              The method uses the _ensure_exists method to
                            get or create the bureau at each step along the
                            specified path. It uses the _accessor_functions
                            function to get the getter and setter methods
                            for the bureau's data structure.

        """

        # Resolve path-like keys.
        #
        cursor      = self._bureau._bureau_data
        path_cursor = tuple()
        for name in tup_path[:-1]:
            path_cursor += (name,)
            cursor      = self._ensure_exists(path_cursor, cursor, name)

        # Invalid keys raise KeyError.
        #
        try:
            name = tup_path[-1]
        except IndexError:
            raise KeyError(repr(tup_path))

        # Resolve the final element of a path-like
        # key (or the whole key if it is atomic).
        #
        path_cursor += (name,)

        # Avoid recursion and get the old value.
        #
        (get_item, set_item, del_item) = _accessor_functions(cursor)
        is_new_name = name not in cursor

        if is_new_name:

            if not is_delete:
                set_item(name, value_new)
            return None

        else:  # Name already exists

            value_old = get_item(name)
            if is_delete:
                del_item(name)
            else:
                if not (value_old is value_new):
                    set_item(name, value_new)
            return value_old

    # -------------------------------------------------------------------------
    def _ensure_exists(self, tup_path_cursor, cursor, name):
        """
        Return the named item in cursor, or create as a Bureau if not present.

        This function tries to return a named
        item in a given cursor. If the item does
        not exist, it creates a new Bureau object
        and assigns it to the specified name in
        the cursor.

        The function uses the _accessor_functions
        function to get the getter and setter
        methods for the current cursor, and uses
        these methods to get and set items in the
        cursor.

        """

        (get_item, set_item, del_item) = _accessor_functions(cursor)
        try:
            cursor = get_item(name)
        except KeyError:
            bureau_new = Bureau(_engine = self,
                                _path   = tup_path_cursor)
            set_item(name, bureau_new)
            cursor = bureau_new

        return cursor

    # -------------------------------------------------------------------------
    def rule(self,
             rule     = None,
             cond     = None,
             act      = None,
             tup_path = None):
        """
        Add a rule.

        """

        has_rule      = rule      is not None
        has_condition = cond      is not None
        has_action    = act       is not None
        has_tup_path  = tup_path  is not None

        if has_rule:

            if (has_condition) or (has_action):
                raise ValueError((
                    'If a rule is specified, then'
                    'no additional condition or'
                    'action may be specified.'))

        else:

            if (not has_condition) or (not has_action):
                raise ValueError((
                    'If no rule is specified, then'
                    'a condition and an action must'
                    'be specified instead.'))

            # Ensure condition wrapped in tuple
            if callable(cond):
                cond = (cond,)

            rule = Rule(cond = cond,
                        act  = act)

        # Add an indicator function to the rule's
        # conditions to select only commands that
        # affect the specified path.
        #
        if has_tup_path:
            rule = Rule(cond = (fl.rule.is_root_in(tup_path),) + rule.cond,
                        act  = rule.act)

        self._list_rule.append(rule)

        return None

    # -------------------------------------------------------------------------
    def _invoke_rules(self, batch):
        """
        Invoke rules for the specified batch of commands.

        """

        list_cmd = list()
        for rule in self._list_rule:

            # If one or more commands in the
            # batch meet all of the current
            # rule's conditions, then the rule's
            # action is invoked.
            #
            list_cmd.clear()
            list_cmd[:] = batch

            for indicator in rule.cond:
                if not list_cmd:
                    break
                list_cmd[:] = (cmd for cmd in list_cmd if indicator(cmd = cmd))

            if not list_cmd:
                continue

            rule.act(self._bureau, list_cmd)

        return None


# -------------------------------------------------------------------------
def tup_path_val_to_dict(tup_path_val):
    """
    Return a representation of tup_path_val as a nested dict.

    This function converts the specified
    tuple of path-value pairs into a nested
    dictionary representation.

    The paths are sorted by their length as
    a (probably unnecessary) sanity check
    to ensure that parent dictionaries are
    created before their children.

    For each path-value pair, this method
    creates nested dictionaries within the
    output dictionary according to the path,
    and sets the innermost dictionary's value
    according to the value.

    The resulting dictionary has the same
    nested structure as the original object,
    and can be used for purposes like
    serialization.

    :returns:   A nested dictionary representation of the object. The
                keys in the dictionary correspond to the paths in the
                object, and the values in the dictionary correspond
                to the values in the object.

    """

    tup_path_val = sorted(tup_path_val, key = lambda item: len(item[0]))

    set_path_referent_as_list = _set_path_referent_as_list(tup_path_val)

    # Go through each leaf path-value pair
    # in tup_path_val, creating internal
    # nodes in the tree as required.
    #
    output = dict()
    for (tup_path, value) in tup_path_val:

        # Go through path from root to leaf.
        #
        cursor         = output
        tup_path_accum = tuple()
        for (idx, name) in enumerate(tup_path[:-1]):
            tup_path_accum = tup_path_accum + (name,)
            do_use_list    = tup_path_accum in set_path_referent_as_list
            if do_use_list:
                ctor = list
            else:
                ctor = dict

            # Create nodes in the tree as
            # required. If the current node
            # is a dictionary, then it is
            # easy enough to add either
            # a list or a dict in the named
            # slot as required.
            #
            if isinstance(cursor, dict):
                if (name not in cursor):
                    cursor[name] = ctor()

            # If on the other hand, the
            # current node is a list, then
            # we need to be careful to
            # extend the list to the required
            # size before adding values.
            #
            else:

                # Extend the list as needed.
                #
                idx      = int(name)
                len_list = len(cursor)
                if idx >= len_list:
                    len_needed = (idx + 1)  # Because 0-based
                    shortfall  = len_needed - len_list
                    cursor    += [None] * shortfall

                # Add either a list or a
                # dict to the index as
                # required.
                #
                if cursor[idx] is None:
                    cursor[name] = ctor()

            cursor = cursor[name]

        name = tup_path[-1]
        if isinstance(cursor, dict):
            cursor[name] = value
        else:
            idx      = int(name)
            len_list = len(cursor)
            if idx >= len_list:
                len_needed = idx + 1  # Because 0-based
                shortfall  = len_needed - len_list
                cursor    += [None] * shortfall
            cursor[name] = value

    return output


# -----------------------------------------------------------------------------
def _set_path_referent_as_list(tup_path_val):
    """
    Return the set of paths whose referents can be represented as lists.

    If the referent of a path has one or
    more non-integer keys, then it must
    be represented by a mapping of some sort
    such as a 'dict'.

    On the other hand, if the referent of
    a path has nothing but integer keys,
    then we can use a (possibly sparse)
    ordered collection such as a 'list' or
    a 'tuple' instead of a mapping.

    TODO: Give some thought as to whether
          we actually want to use a list
          if the integer indices are very
          sparsely distributed.

    """

    set_path_maybe_list = set()
    set_path_never_list = set()

    for (tup_path, _) in tup_path_val:

        for (idx, name) in enumerate(tup_path):

            is_integer_key = True
            try:
                _ = int(name)
            except ValueError:
                is_integer_key = False

            if is_integer_key:
                set_path_maybe_list.add(tup_path[0:idx])
            else:
                set_path_never_list.add(tup_path[0:idx])

    set_path_referent_as_list = set_path_maybe_list - set_path_never_list

    return set_path_referent_as_list


# -----------------------------------------------------------------------------
def _accessor_functions(item):
    """
    Return getter and setter methods for the specified object.

    This function returns the getter and setter
    methods for a specified object. If the object
    is an instance of Bureau, it uses the getter
    and setter methods of the _bureau_data
    attribute.

    If the object is not an instance of Bureau,
    it uses the built-in getter and setter
    methods.

    """

    if isinstance(item, Bureau):

        get_item = item._bureau_data.__getitem__
        set_item = item._bureau_data.__setitem__
        del_item = item._bureau_data.__delitem__

    else:

        get_item = item.__getitem__
        set_item = item.__setitem__
        del_item = item.__delitem__

    return (get_item, set_item, del_item)


# -----------------------------------------------------------------------------
def _iter_path(path, delim):
    """
    Yield each item in path.

    This function returns a generator that yields
    each item in a given path. The path can be a
    string, an iterable, or an atomic (non-string,
    non-iterable) value.

    If the path is a string, it is split by a
    specified delimiter, and each item is yielded.

    If the item can be converted to an integer,
    it is yielded as an integer; otherwise, it
    is yielded as a string.

    If the path is an iterable (but not a string),
    each item in the iterable is yielded.

    If the path is an atomic value (neither a
    string nor an iterable), it is yielded as is.

    """

    # If the path is a string, split by the
    # delimiter and yield each item in turn.
    #
    try:
        for item in path.split(delim):
            try:
                yield int(item)  # Support for indices into lists.
            except ValueError:
                yield item

    # If the path is not a string (it doesn't
    # have the split method), it treats it as
    # an iterable.
    #
    except AttributeError:
        try:
            for item in path:
                yield item

        # If the path is not an iterable either,
        # it treats it as an atomic value and
        # yields it as-is.
        #
        except TypeError:
            yield path


# =============================================================================
class DotDict(dict):
    """
    Custom dictionary with dot notation attribute access.

    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# -----------------------------------------------------------------------------
def coroutine(fun):
    """
    This module provides the 'coroutine' decorator for priming coroutines.

    A coroutine in Python is a function containing
    the 'yield' statement, and can be used to handle
    asynchronous tasks elegantly.

    However, before a coroutine can start responding
    to 'send()' or '__next__()' calls, it must be
    'primed' to advance its execution to the first
    'yield' expression. This module's 'coroutine'
    decorator provides a way to automatically prime
    coroutines upon their creation.

    Functions:

        coroutine (fun: Callable) -> Callable :

                A decorator function that primes a coroutine by automatically
                advancing its execution to the first 'yield' statement.

    Example:

        @coroutine
        def my_coroutine():
            while True:
                received = yield
                # process received value

    """

    def primed(*args, **kwargs):
        """
        Wrapper for coroutines that 'primes' it by sending the first message.

        """

        coro = fun(*args, **kwargs)
        coro.send(None)
        return coro

    return primed


# -----------------------------------------------------------------------------
def resolve(value, ctx = None):
    """
    Resolves a string to its actual value.

    The function handles strings starting with
    '_spec::' or '_ref::', interpreting them as
    module specifications and context references
    respectively. For '_spec::', it imports the
    module and fetches the attribute, while for
    '_ref::', it fetches the attribute from the
    provided context.

    If the value is not a string, or does not
    start with the recognized prefixes, it is
    returned as is.

    The function performs a maximum of
    'count_indir_max' iterations of resolution,
    raising a RuntimeError if this limit is
    exceeded.

    Parameters:

        value (str or Any):     The value to be resolved. Could be string
                                (with specific prefixes) or any other data
                                type.

        ctx (dict, optional):   Context in which the '_ref::' prefixed values
                                should be resolved.

    Returns:

        Any:                    The resolved value, which could be any
                                data type.

    Raises:

        RuntimeError:   If the maximum limit of resolution levels
                        ('count_indir_max') is exceeded.

    """

    prefix_spec     = '_spec::'
    prefix_ref      = '_ref::'
    count_indir_max = 10


    for _ in range(count_indir_max):

        if not fl.util.alg.is_string(value):
            return value

        if value.startswith(prefix_spec):
            value = from_spec(value[len(prefix_spec):])
        elif value.startswith(prefix_ref):
            value = ctx[value[len(prefix_ref):]]
        else:
            return value

    raise RuntimeError('Maximum number of levels of indirection exceeded.')


# -----------------------------------------------------------------------------
def from_spec(str_spec):
    """
    Imports a module and fetches a specified attribute from it.

    The function receives a string in the format
    'module.attribute', and returns the value of
    the attribute from the specified module. It
    uses the Python built-in 'importlib' to
    dynamically import the module.

    Parameters:

        str_spec (str):     The string specifying the module and the
                            attribute, in the format 'module.attribute'.

    Returns:

        Any:                The attribute fetched from the specified
                            module.

    Raises:

        ImportError:        If the module specified in 'str_spec'
                            cannot be imported.

        AttributeError:     If the attribute specified in 'str_spec'
                            does not exist in the module.

    """

    (name_module, name_attrib) = str_spec.rsplit('.', 1)
    return getattr(importlib.import_module(name_module), name_attrib)


# -----------------------------------------------------------------------------
def strhash(string, length = 8):
    """
    Return a short hexadecimal hash code for the specified string.

    """

    sha256 = hashlib.sha256()
    sha256.update(string.encode('utf-8'))
    return sha256.hexdigest()[:length]