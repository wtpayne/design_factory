# -*- coding: utf-8 -*-
"""
---

title:
    "Interactive design index browser command module."

description:
    "This module provides an interactive design
    index browser textual user interface."

id:
    "c334ab74-e2b4-45ea-a4d0-569b3ff97df9"

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
import dataclasses
import os
import os.path
import sys

import pycozo.client
import rich.pretty
import rich.syntax
import rich.traceback
import textual
import textual.app
import textual.binding
import textual.color
import textual.containers
import textual.reactive
import textual.widgets

import cl.design.index.db.trace as trace


# =============================================================================
@dataclasses.dataclass
class Theme:
    """
    Theme dataclass

    """
    background: textual.color.Color
    foreground: textual.color.Color


_THEME = Theme(background = 'black',
               foreground = 'green')


# -----------------------------------------------------------------------------
def run():
    """
    Run the interactive design index browser.

    """
    dirpath_src  = _dirpath_src()
    dirname_src  = os.path.basename(dirpath_src)
    filepath_db  = os.path.join(_dirpath_tmp(), 'main/design_index.db')
    db           = trace.DataBase(filepath_db = filepath_db)
    design_index = {
        'src':     DesignIndexDict(db, dirpath_src, dirname_src, ''),
        'reports': DesignIndexDict(db, 'reports',   'reports',   '') }
    app = Browser(label_tree_root = 'ws00_pri',
                  map_data_tree   = design_index)
    app.run()
    return 0


# =============================================================================
class Browser(textual.app.App):
    """
    Textual design index browser app.

    """
    _nav             = None
    _content         = None
    _label_tree_root = ''
    _map_data_tree   = dict()  # Dict-like backing datastore for the tree.
    _set_id_expanded = set()   # Set of items whose children are expanded.

    # -------------------------------------------------------------------------
    def __init__(self, label_tree_root, map_data_tree):
        """
        Create a Browser app class.

        """
        self._label_tree_root = label_tree_root
        self._map_data_tree   = map_data_tree
        super().__init__()

    # -------------------------------------------------------------------------
    def on_mount(self) -> None:
        """
        Ensure the navigation tree has focus once the app is mounted.

        """
        self._nav.focus()

    # -------------------------------------------------------------------------
    def compose(self) -> textual.app.ComposeResult:
        """
        Yield all initial user interface widgets.

        """
        self._nav     = NavTree(id    = 'nav_tree',
                                label = self._label_tree_root,
                                data  = self._map_data_tree)
        self._content = ContentDisplay(
                                id     = 'content_pane',
                                expand = True)
        yield self._nav
        yield self._content

    # -------------------------------------------------------------------------
    def _update_content(self, event):
        """
        Update the content pane with the specified event.

        """
        try:
            metadata = event.node.data.metadata
            if isinstance(metadata, str):
                self._content.update(metadata)
            else:
                self._content.update(rich.pretty.Pretty(metadata))
        except AttributeError:
            self._content.update("")
            pass

    # -------------------------------------------------------------------------
    def on_tree_node_selected(
                        self,
                        event: textual.widgets.Tree.NodeSelected) -> None:
        """
        Display the content.

        """
        self._update_content(event)

    # -------------------------------------------------------------------------
    def on_tree_node_expanded(
                        self,
                        event: textual.widgets.Tree.NodeSelected) -> None:
        """
        Load the children of a tree node when the parent node is expanded.

        """
        event.stop()

        self._update_content(event)

        # Ignore nodes that are
        # already in the cache.
        #
        id_data = id(event.node.data)
        if id_data not in self._set_id_expanded:
            self._set_id_expanded.add(id_data)

            # Add child nodes in the same
            # order as they are returned
            # from the .items() call.
            #
            # Child nodes may either be
            # expanding 'interior' nodes, or
            # non-expanding 'leaf' nodes.
            #
            for (id_node, node) in event.node.data.items():
                try:
                    _ = node.items()

                # Add non-expanding 'leaf' node.
                #
                except AttributeError:
                    event.node.add(id_node,
                                   data         = None,
                                   expand       = False,
                                   allow_expand = False)

                # Add expanding 'interior' node.
                #
                else:
                    event.node.add(node.label,
                                   data         = node,
                                   expand       = False,
                                   allow_expand = True)


# =============================================================================
class NavTree(textual.widgets.Tree):
    """
    Navigation tree widget.

    """
    Binding  = textual.binding.Binding
    BINDINGS = [
        Binding('space', 'select_cursor', 'Select', show = False),
        Binding('right', 'select_cursor', 'Select', show = False),
        Binding('left',  'select_cursor', 'Select', show = False)
    ]

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Contstruct a new navigation tree widget.

        """
        super().__init__(*args, **kwargs)

        self.styles.background = _THEME.background
        self.styles.color      = _THEME.foreground
        self.styles.min_height = '80vh'
        self.styles.width      = '100%'


# =============================================================================
class ContentDisplay(textual.widgets.Static):
    """
    Content display widget.

    """

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Contstruct a new content display widget.

        """
        super().__init__(*args, **kwargs)

        self.styles.background = _THEME.background
        self.styles.color      = _THEME.foreground
        self.styles.width      = '100%'
        self.styles.dock       = 'bottom'
        self.styles.padding    = (1, 1)


# =============================================================================
class DesignIndexDict(collections.UserDict):
    """
    Read only dictionary backed by the design index.

    """

    # -------------------------------------------------------------------------
    def __init__(self, db, id_node, label_node, metadata, *args, **kwargs):
        """
        Return a DesignIndexDict instance.

        """
        super().__init__(*args, **kwargs)

        self.label    = label_node
        self.metadata = metadata

        for trace in db.iter_trace(id_from = id_node):

            (rel_type, id_dst, label_src, label_dst, metadata_dst) = trace
            self.data[id_dst] = DesignIndexDict(db         = db,
                                                id_node    = id_dst,
                                                label_node = label_dst,
                                                metadata   = metadata_dst)


# -----------------------------------------------------------------------------
def _dirpath_self():
    """
    Return the directory path to the current module.

    """
    return os.path.dirname(os.path.realpath(__file__))


# -----------------------------------------------------------------------------
def _dirpath_workspace():
    """
    Return the path of the workspace filesystem root directory.

    """
    return os.path.normpath(os.path.join(_dirpath_self(), '../../../../..'))


# -----------------------------------------------------------------------------
def _dirpath_src():
    """
    Return the path of the workspace filesystem source directory.

    """
    return os.path.normpath(os.path.join(_dirpath_workspace(), 'a3_src'))


# -----------------------------------------------------------------------------
def _dirpath_tmp():
    """
    Return the path of the workspace filesystem temporary directory.

    """
    return os.path.normpath(os.path.join(_dirpath_workspace(), 'a4_tmp'))
