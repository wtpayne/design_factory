# -*- coding: utf-8 -*-
"""
Test utiltiy functions.

"""


import collections
import contextlib
import inspect
import os
import os.path
import sys

import pl.stableflow.cli.command
import pl.stableflow.util.serialization

import click.testing
import dill
import zmq


TEST_PORT = 5556


# -----------------------------------------------------------------------------
def env(filepath):
    """
    Return an environment dict with the specified filepath on PYTHONPATH.

    """

    relpath    = filepath if filepath else sys.argv[0]
    dirpath    = os.path.dirname(os.path.realpath(relpath))
    pythonpath = os.environ.get('PYTHONPATH', '')
    env        = {'PYTHONPATH': os.pathsep.join([pythonpath, dirpath])}
    return env


# -----------------------------------------------------------------------------
def simple_pipeline(repr, iface, is_closed_loop, **kwargs):
    """
    Return test configuration for a simple pipeline to run on localhost.

    """

    cfg = {
        'system': {
            'id_system': 'stableflow_system_test'
        },
        'host': {
            'localhost': {
                'hostname':       '127.0.0.1',
                'acct_run':       'stableflow',
                'acct_provision': 'stableflow'
            }
        },
        'process': {},
        'node': {},
        'edge': [],
        'requirement': {
            'some_requirement': {
                'how_to_install'
            }
        },
        'data': {
            'python_dict': 'py_dict'
        }
    }

    list_name_node = list()

    for name_process, cfg_process in kwargs.items():
        cfg['process'][name_process] = {'host': 'localhost'}

        for (name_node, function) in cfg_process.items():

            if repr == 'py_dill':
                packer = dill.dumps
            elif repr == 'py_src':
                packer = inspect.getsource
            else:
                raise RuntimeError(
                            'Unrecognized representation: "{repr}"'.format(
                                                                repr = repr))
            if iface == 'step':
                spec_functionality = {
                        'reset':  packer(_noop_reset),
                        'step':   packer(function) }
            elif iface == 'coro':
                spec_functionality = {
                        'coro':   packer(function) }
            else:
                raise RuntimeError(
                            'Unrecognized interface: "{iface}"'.format(
                                                                iface = iface))

            list_name_node.append(name_node)
            cfg['node'][name_node] = {
                'process':       name_process,
                'state_type':    'python_dict',
                'functionality':  {
                    'requirement':  'some_requirement',
                    repr:           spec_functionality
                }
            }

    # Generate edges in a pipeline.
    for (name_src, name_dst) in _sliding_window(list_name_node, len_window = 2):
        cfg['edge'].append({
                'owner': name_src,
                'data':  'python_dict',
                'src':   name_src + '.outputs.output',
                'dst':   name_dst + '.inputs.input'
            })

    # Complete the feedback loop
    if is_closed_loop:
        name_src = list_name_node[-1]
        name_dst = list_name_node[0]
        cfg['edge'].append({
                'owner': name_src,
                'data':  'python_dict',
                'src':   name_src + '.outputs.output',
                'dst':   name_dst + '.inputs.input'
            })

    return cfg


# -----------------------------------------------------------------------------
def _sliding_window(iterable, len_window):
    """
    Yield pairs drawn consecutively from the specified iterable.

    """

    iterator_obj = iter(iterable)
    initial_pair = (next(iterator_obj, None) for _ in range(len_window))
    window       = collections.deque(initial_pair, maxlen = len_window)

    yield window

    for item in iterator_obj:
        window.append(item)
        yield window


# -----------------------------------------------------------------------------
def _noop_reset(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Default noop reset function.

    """

    pass


# -----------------------------------------------------------------------------
def run(cfg, expected_output, is_local = False, env = None):
    """
    Run the specified system config.

    Look for the specified outputs on the
    specified ports.

    """

    # if 'VIRTUAL_ENV' in os.environ:
    #     cfg['host']['localhost']['dirpath_venv'] = os.environ['VIRTUAL_ENV']

    with _reply_sockets_context(iter_port = expected_output.keys()) as sock:

        arg_local = '--local' if is_local else '--no-local'
        str_cfg   = pl.stableflow.util.serialization.serialize(cfg)
        args      = ['system', 'start', arg_local, '--cfg', str_cfg]
        runner    = click.testing.CliRunner(env = env)
        response  = runner.invoke(pl.stableflow.cli.command.grp_main, args)

        assert response.output    == '', 'Unexpected output: "{txt}"'.format(
                                                    txt = response.output)
        assert response.exit_code == 0, 'Unexpected exit code: "{id}"'.format(
                                                    id = response.exit_code)

        for key, expected_msg in expected_output.items():
            received_msg = sock[key].recv().decode('utf-8')
            assert received_msg == expected_msg, \
                   'Unexpected message: {msg}'.format(msg = received_msg)


# -----------------------------------------------------------------------------
def send(message, port = TEST_PORT):
    """
    Send the specified message on the specified port.

    """

    with _request_socket_context(port) as sock:
        sock.send(message.encode('utf-8'))


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _request_socket_context(port):
    """
    Yield a request socket context for the specified port.

    """

    context = zmq.Context()
    socket  = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:{port}'.format(port = port))

    yield socket

    socket.close()
    context.term()


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _reply_sockets_context(iter_port):
    """
    Yield a dictionary with a reply socket context for each specified port.

    """

    context    = zmq.Context()
    map_socket = dict()
    for port in iter_port:
        map_socket[port] = context.socket(zmq.REP)
        # map_socket[port].setsockopt(zmq.LINGER, 0)
        map_socket[port].bind('tcp://*:{port}'.format(port = port))

    yield map_socket

    for socket in map_socket.values():
        socket.close()
    context.term()
