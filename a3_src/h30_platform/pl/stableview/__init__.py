# -*- coding: utf-8 -*-
"""
---

title:
    "Stableview GUI platform package."

description:
    "This package provides functions for
    running user interfaces that are based
    ont the stableview platform."

id:
    "9fa93a78-fd12-44c4-9122-05b35e272340"

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


import copy
import importlib.metadata
import os.path

import appdirs
import dearpygui.dearpygui
import ruamel.yaml

import fl.rule
import fl.util
import fl.util.debug
import fl.util.io


try:
    __version__ = importlib.metadata.version('stableview')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


# -----------------------------------------------------------------------------
def main(dirpath_app, id_org, id_app, **kwargs):
    """
    Main update/event loop for the ui.

    """

    with fl.util.debug.rich_exception_printing_context(show_locals = False):

        # Initialize the various component parts of
        # the UI architecture:-
        #
        #   1. ctx.ui    - The DearPyGui API.
        #   2. ctx.app   - The application model.
        #   3. ctx.cfg   - General configuration.
        #   4. ctx.theme - Theme configuration.
        #   5. ctx.view  - The view model.
        #   6. ctx.store - Persistent data store.
        #
        # We also add rules for responding to
        # changes in the view. Rules for
        # responding to changes in the view model
        # and application model will be by their
        # nature application-specific and therefore
        # are colocated with application specific
        # design elements.
        #
        ctx     = fl.util.Bureau()
        ctx.ui  = dearpygui.dearpygui
        ctx.app = fl.util.Bureau()

        # The configuration must be loaded
        # before the theme so that the theme
        # can be set with configuration.
        #
        ctx.cfg = fl.util.Bureau()
        _load_cfg(ctx, id_app, id_org, **kwargs)

        # The theme must be loaded before
        # the view rules are triggered, as
        # the view configuration has
        # references to theme elements
        # which need to be resolved. The rules
        # are triggered on ctx.batch_finalize()
        #
        ctx.theme = fl.util.Bureau()
        _load_theme(ctx, dirpath_app, ctx.cfg.id_theme)

        # The view has the configuration for
        # most of the structure and layout of
        # UI elments.
        #
        batch = ctx.batch_init()
        filepath_cfg_view = _filepath_cfg_view(dirpath_app, ctx.cfg.id_view)
        ctx.view.from_file(filepath_cfg_view)
        ctx.view.rule(cond = fl.rule.is_leaf_at(('_fcn',)),
                      act  = _update_dearpygui_widgets)

        # The store must be loaded after view
        # so it can add UI elements to an already
        # existing structure/
        #
        ctx.store = fl.util.Bureau()
        _load_store(ctx, id_app, id_org)

        # Application coroutine
        #
        ctx.coro = fl.util.resolve(ctx.view.coro)(ctx)
        next(ctx.coro)                            # app early setup.

        ctx.ui.create_context()
        ctx.ui.configure_app(manual_callback_management = True)

        try:
            ctx.batch_finalize(batch)             # Trigger rules, create view.

            ctx.ui.setup_dearpygui()

            next(ctx.coro)                        # app late setup.

            ctx.ui.show_viewport()
            while ctx.ui.is_dearpygui_running():

                next(ctx.coro)                    # app runtime step.

                jobs = ctx.ui.get_callback_queue() # retrieves and clears queue
                ctx.ui.run_callbacks(jobs)

                ctx.ui.render_dearpygui_frame()

        finally:
            ctx.ui.destroy_context()


# -----------------------------------------------------------------------------
def _load_store(ctx, id_app, id_org):
    """
    Update ctx.store with persistent stored data.

    """

    filename = '{id}.cfg.yaml'.format(id = id_app)
    for (id_cfg, dirpath) in (
                ('site_data', appdirs.site_data_dir( id_app, id_org )),
                ('user_data', appdirs.user_data_dir( id_app, id_org ))):

        filepath_cfg = os.path.join(dirpath, filename)
        ctx.cfg['filepath_' + id_cfg] = filepath_cfg
        if os.path.isfile(filepath_cfg):
            ctx.store.from_file(filepath = filepath_cfg)


# -----------------------------------------------------------------------------
def _load_cfg(ctx, id_app, id_org, **kwargs):
    """
    Update ctx.cfg with configuration data.

    """

    ctx.cfg.dirpath_cache = appdirs.user_cache_dir( id_app, id_org )
    ctx.cfg.dirpath_log   = appdirs.user_log_dir(   id_app, id_org )

    filename = '{id}.cfg.yaml'.format(id = id_app)
    for (id_cfg, dirpath) in (
                ('site_config', appdirs.site_config_dir( id_app, id_org )),
                ('user_config', appdirs.user_config_dir( id_app, id_org ))):

        filepath_cfg = os.path.join(dirpath, filename)
        ctx.cfg['filepath_' + id_cfg] = filepath_cfg
        if os.path.isfile(filepath_cfg):
            ctx.cfg.from_file(filepath = filepath_cfg)

    ctx.cfg.from_dict(kwargs)


# -----------------------------------------------------------------------------
def _load_theme(ctx, dirpath_app, id_theme):
    """
    Update ctx.theme with theme data.

    """

    dirpath_theme      = os.path.join(dirpath_app, 'theme', id_theme)
    filename_cfg_theme = '{id}.flowforge.theme.yaml'.format(id = id_theme)
    filepath_cfg_theme = os.path.join(dirpath_theme, filename_cfg_theme)

    if not os.path.isfile(filepath_cfg_theme):
        raise RuntimeError(
                'Could not find theme configuration: ' + filepath_cfg_theme)

    (map_cfg_theme,
     map_error) = fl.util.io.load_from_filepath(filepath_cfg_theme)

    if map_error:
        msg = 'Could not load theme configuration: ' + filepath_cfg_theme
        raise RuntimeError(msg) from map_error['exception']

    # Resolve any references in the thing.
    for id_section in ('color', 'style', 'form'):
        for (key, value) in map_cfg_theme[id_section].items():
            ctx.theme[key] = fl.util.resolve(value)

    ctx.theme['icon_play']    = _load_icon(ctx, dirpath_theme, 'play')
    ctx.theme['icon_pause']   = _load_icon(ctx, dirpath_theme, 'pause')
    ctx.theme['icon_stop']    = _load_icon(ctx, dirpath_theme, 'stop')
    ctx.theme['font_primary'] = _filepath_font(dirpath_theme, 'default')


# -----------------------------------------------------------------------------
def _filepath_font(dirpath_theme, id_font):
    """
    Return the filepath to the specifiewd font.

    """

    filename_font = '{id_font}.ttf'.format(id_font = id_font)
    filepath_font = os.path.join(dirpath_theme, filename_font)

    if not os.path.isfile(filepath_font):
        raise RuntimeError('Could not find font: ' + filepath_font)

    return filepath_font


# -----------------------------------------------------------------------------
def _load_icon(ctx, dirpath_theme, id_icon, width = 16, height = 16):
    """
    Return the file path to the specified icon.

    """

    filename_png = '{id}.png'.format(id = id_icon)
    filepath_png = os.path.join(dirpath_theme, filename_png)

    if not os.path.isfile(filepath_png):
        raise RuntimeError('Could not find icon: ' + filepath_png)

    (width_png, height_png, channels, data) = ctx.ui.load_image(filepath_png)

    if not width_png == width:
        raise RuntimeError('Incorrect icon width: ' + filepath_png)

    if not height_png == height:
        raise RuntimeError('Incorrect icon height: ' + filepath_png)

    return data


# -----------------------------------------------------------------------------
def _filepath_cfg_view(dirpath_app, id_view):
    """
    Load configuration for the UI from the specified view.

    """

    filename_cfg = '{name}.stableview.cfg.yaml'.format(name = id_view)
    filepath_cfg = os.path.join(dirpath_app, id_view, filename_cfg)
    return filepath_cfg


# -----------------------------------------------------------------------------
def update_bound_values(sender, app_data, ctx):
    """
    Update bound values with app_data.

    This function is intended to be registered as
    a callback handler on various widgets in the
    view, allowing any number of bound values to
    be updated in response to user input or other
    UI events.

    We have arranged things so that the dearpygui
    tag for each widget is also the dot delimited
    string path of the corresponding item in the
    view model data structure.

    This means that we are able to easily look
    up the configured bindings for each widget
    just by using the 'sender' tag as an index
    into the context data structure.

    Similarly, the bindings themselves are just
    lists of dot-delimited bound paths that
    need to be updated with the callback
    app_Data value.

    """

    if '_bind' in ctx[sender]:
        for bound_path in ctx[sender]._bind:
            ctx[bound_path] = app_data
    return None


# -----------------------------------------------------------------------------
def _update_dearpygui_widgets(ctx, tup_cmd):
    """
    Update widgets corresponding to the specified commands.

    """

    for cmd in tup_cmd:

        if cmd.operation == 'del':
            _del_widget(ctx, cmd)

        if cmd.operation == 'add':
            _add_widget(ctx, cmd)

        if cmd.operation == 'edit':
            print('EDIT')
            print(cmd)


# -----------------------------------------------------------------------------
def _del_widget(ctx, cmd):
    """
    Delete the widget being referenced by the specified command.

    """

    tup_path = cmd.path[:-1]
    tag      = '.'.join(tup_path)
    ctx.ui.delete_item(tag)


# -------------------------------------------------------------------------
def widget(cfg, fcn, *args, **kwargs):
    """
    Add the specfied widget to the view.

    """

    cfg._fcn = fcn

    if args:
        cfg.args = list()
        for item in args:
            cfg._args.append(item)

    if kwargs:
        for (key, value) in kwargs.items():
            cfg._kwargs[key] = value

    return cfg


# -----------------------------------------------------------------------------
def _add_widget(ctx, cmd):
    """
    Add the widget being referenced by the specified command.

    """

    tup_path = cmd.path[:-1]
    cfg_item = ctx[tup_path]

    (name_fcn, args, kwargs, bindings, misc) = _get_widget_params(cfg_item)

    fcn = getattr(ctx.ui, name_fcn)

    # Resolve functions (and sometimes also
    # constants) from specification strings
    # to their actual (e.g. callable) values.
    #
    for key in tuple(kwargs.keys()):  # Keys change, so iterate over a copy.

        # value = kwargs[key]
        # if isinstance(value, str):
        #     prefix = '_ref::'
        #     if value.startswith(prefix):
        #         kwargs[key] = ctx[value[len(prefix):]]

        kwargs[key] = fl.util.resolve(value = kwargs[key], ctx = ctx)

        if key.endswith('callback'):
            kwargs['user_data'] = ctx

    # Handle nodes where the associated
    # DearPyGui function does not expect
    # either a tag parameter or a parent
    # parameter.
    #
    tup_no_tag = ('create_viewport',
                  'bind_item_font',
                  'bind_theme',
                  'bind_item_handler_registry')
    if name_fcn in tup_no_tag:
        fcn(**kwargs)
        return
    tag_item      = '.'.join(tup_path)
    kwargs['tag'] = tag_item

    # Handle functions known to have
    # no parent parameter.
    #
    tup_no_parent = ('add_file_dialog',
                     'add_font_registry',
                     'add_handler_registry',
                     'add_item_handler_registry',
                     'add_texture_registry',
                     'add_theme',
                     'add_window')
    if name_fcn in tup_no_parent:
        fcn(**kwargs)
        if 'set_primary_window' in misc and misc['set_primary_window']:
            ctx.ui.set_primary_window(tag_item, True)
        return
    tag_parent       = '.'.join(tup_path[:-1])
    kwargs['parent'] = tag_parent

    # Handle all other functions.
    #
    if args:
        fcn(*args, **kwargs)
    else:
        fcn(**kwargs)


# -----------------------------------------------------------------------------
def _get_widget_params(cfg_item):
    """
    Return widget parameters from the specified config.

    """

    name_fcn = ''
    args     = tuple()
    kwargs   = dict()
    bindings = dict()
    misc     = dict()

    if '_fcn' in cfg_item:
        name_fcn = cfg_item._fcn

    if '_args' in cfg_item:
        args = cfg_item._args

    if '_kwargs' in cfg_item:
        kwargs = cfg_item._kwargs.to_dict()

    if '_bindings' in cfg_item:
        bindings = cfg_item._bindings.to_dict()

    if '_misc' in cfg_item:
        misc = cfg_item._misc.to_dict()

    return (name_fcn, args, kwargs, bindings, misc)
