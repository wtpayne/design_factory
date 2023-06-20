# -*- coding: utf-8 -*-
"""
Functional specification for cl.util.persistence.ic00_edict


"""


import os
import shutil
import unittest.mock

import dill
import pytest


# =============================================================================
class SpecifyClUtilPersistenceIc00_edict:
    """
    Spec for the cl.util.persistence.ic00_edict module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_cl_util_persistence_ic00_edict(self):
        """
        The module can be imported.

        """
        import cl.util.persistence.ic00_edict


# =============================================================================
class SpecifyClUtilPersistenceIc00_edictCoro:
    """
    Spec for the cl.util.persistence.ic00_edict.coro coroutine.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_should_persist_and_load_data_successfully_on_a_valid_run(self,
                                                                    tmp_path):
        """
        The coroutine functions correctly when conditions are nominal.

        This is the simplest test case where all
        conditions are ideal. It will ensure that
        the component works as expected under
        normal conditions.

        The correct directory path is provided,
        the necessary read/write permissions are
        available, and the data to be persisted is
        pickleable.

        """

        import cl.util.persistence.ic00_edict

        # Setup.
        #
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        runtime = {'id':         {'id_system': 'test_system'}}
        cfg     = {'dirpath':    test_dir}
        inputs  = {'ctrl':       {'ena':   True,
                                  'ts':    {},
                                  'list':  []},
                   'test_data':  {'ena':   True,
                                  'ts':    {},
                                  'list':  ['test_value']}}
        state   = {}
        outputs = {'test_data':  {'ena':   False,
                                  'ts':    {},
                                  'list':  []}}

        # Run test
        #
        coroutine = cl.util.persistence.ic00_edict.coro(runtime,
                                                        cfg,
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = coroutine.send(None)
        assert signal is None

        (outputs, signal) = coroutine.send(inputs)
        assert signal is None

        # Check that data was persisted
        #
        persisted_file = os.path.join(test_dir, 'test_data.bin')
        assert os.path.exists(persisted_file)

        # Reload the coroutine and check that it loads the saved state
        #
        coroutine = cl.util.persistence.ic00_edict.coro(runtime,
                                                        cfg,
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = coroutine.send(None)
        assert signal is None

        (outputs, signal) = coroutine.send(inputs)
        assert signal is None

        assert outputs['test_data']['ena'] == True
        assert outputs['test_data']['list'] == ['test_value']

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_should_create_directory_if_not_already_exists(self,
                                                         tmp_path):
        """
        The coroutine creates a save directory if it doesnt already exist.

        This test ensures that the component
        works as expected when the directory
        specified in the configuration does not
        exist. It should automatically create
        the directory.

        """

        import cl.util.persistence.ic00_edict

        # Setup.
        #
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        runtime = {'id':         {'id_system': 'test_system'}}
        cfg     = {'dirpath':    test_dir}
        inputs  = {'ctrl':       {'ena':   True,
                                  'ts':    {},
                                  'list':  []},
                   'test_data':  {'ena':   True,
                                  'ts':    {},
                                  'list':  ['test_value']}}
        state   = {}
        outputs = {'test_data':  {'ena':   False,
                                  'ts':    {},
                                  'list':  []}}

        # Run test
        #
        coroutine = cl.util.persistence.ic00_edict.coro(runtime,
                                                        cfg,
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = coroutine.send(None)
        assert signal is None

        (outputs, signal) = coroutine.send(inputs)
        assert signal is None

        # Check that directory was created
        #
        assert os.path.isdir(test_dir)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_should_handle_file_loading_error_gracefully(self,
                                                       tmp_path,
                                                       monkeypatch):
        """
        The coroutine handles file loading errors gracefully.

        This test ensures that the component
        handles file loading errors gracefully.
        A typical scenario could be a corrupted
        or improperly formatted persisted file.

        """

        import cl.util.persistence.ic00_edict

        # Setup.
        #
        test_dir = tmp_path / "subfolder"
        test_dir.mkdir()

        runtime = {'id':        {'id_system': 'test_system'}}
        cfg     = {'dirpath':   str(test_dir)}
        inputs  = {'ctrl':      {'ena': True,
                                 'ts': {},
                                 'list': []},
                   'test_data': {'ena': True,
                                 'ts': {},
                                 'list': ['test_value']}}
        state   = {}
        outputs = {'test_data': {'ena': False,
                                 'ts': {},
                                 'list': []},
                   'log':       {'ena': False,
                                 'ts': {},
                                 'list': []}}

        # Save the state initially to create a
        # persisted file.
        #
        coroutine = cl.util.persistence.ic00_edict.coro(runtime,
                                                        cfg,
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = coroutine.send(None)
        assert signal is None

        (outputs, signal) = coroutine.send(inputs)
        assert signal is None

        # Now let's mock dill.load to raise an
        # UnpicklingError.
        #
        monkeypatch.setattr(
                dill, 'load', unittest.mock.Mock(
                                        side_effect = dill.UnpicklingError))

        # Reload the coroutine. It should handle
        # the UnpicklingError gracefully.
        #
        coroutine = cl.util.persistence.ic00_edict.coro(runtime,
                                                        cfg,
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = coroutine.send(None)
        assert signal is None

        (outputs, signal) = coroutine.send(inputs)
        assert signal is None

        # It should not output the corrupted data.
        #
        assert outputs['test_data']['ena']  == False
        assert outputs['test_data']['ts']   == {}
        assert outputs['test_data']['list'] == []

        # It should log an error message.
        #
        assert outputs['log']['ena'] == True
        assert 'Error unpickling data' in ' '.join(outputs['log']['list'])

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_should_handle_unpickleable_data_error_gracefully(self,
                                                            tmp_path,
                                                            monkeypatch):
        """
        Test for Unpickleable Data:

        This test case involves attempting to
        persist data that cannot be pickled. The
        component should be able to handle the
        dill.PicklingError exception properly.

        """

        import cl.util.persistence.ic00_edict

        # Setup.
        #
        test_dir = tmp_path / "subfolder"
        test_dir.mkdir()

        def generator_function():
            yield 1

        unpicklable_generator = generator_function()

        runtime = {'id':        {'id_system': 'test_system'}}
        cfg     = {'dirpath':   str(test_dir)}
        inputs  = {'ctrl':      {'ena': True,
                                 'ts': {},
                                 'list': []},
                   'test_data': {'ena': True,
                                 'ts': {},
                                 'list': [unpicklable_generator]}}
        state   = {}
        outputs = {'test_data': {'ena': False,
                                 'ts': {},
                                 'list': []},
                   'log':       {'ena': False,
                                 'ts': {},
                                 'list': []}}

        # Run coroutine. It should handle the
        # dill.PicklingError gracefully.
        #
        coroutine = cl.util.persistence.ic00_edict.coro(runtime,
                                                        cfg,
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = coroutine.send(None)
        assert signal is None

        (outputs, signal) = coroutine.send(inputs)
        assert signal is None

        # Check that data was persisted
        #
        persisted_file = os.path.join(test_dir, 'test_data.bin')
        assert os.path.exists(persisted_file)

        # Reload the coroutine and check that it
        # loads the saved state.
        #
        coroutine = cl.util.persistence.ic00_edict.coro(runtime,
                                                        cfg,
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = coroutine.send(None)
        assert signal is None

        (outputs, signal) = coroutine.send(inputs)
        assert signal is None

        # It should not output the unpickleable
        # data.
        #
        assert outputs['test_data']['ena']  == False
        assert outputs['test_data']['ts']   == {}
        assert outputs['test_data']['list'] == []

        # It should log an error message.
        #
        assert outputs['log']['ena'] == True
        assert 'Error pickling data' in ' '.join(outputs['log']['list'])
