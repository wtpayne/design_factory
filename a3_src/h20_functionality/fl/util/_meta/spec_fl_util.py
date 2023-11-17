# -*- coding: utf-8 -*-
"""
Functional specification for fl.util

"""


import textwrap
import time
import warnings

import pytest


# =============================================================================
class SpecifyFlUtil:
    """
    Spec for the fl.util module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        fl.util can be imported with no errors.

        """

        import fl.util


# =============================================================================
class SpecifyFlUtilBureau:
    """
    Spec for the fl.util.Bureau class.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_instantiated(self):
        """
        fl.util.Bureau can be instantiated with no errors.

        """

        import fl.util

        soi = fl.util.Bureau()

        assert isinstance(soi, fl.util.Bureau)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_use_integer_keys(self):
        """
        fl.util.Bureau can use integer keys.

        """

        import fl.util

        soi      = fl.util.Bureau()
        key      = 10203040
        value    = 1234
        soi[key] = value

        assert soi[key] == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_use_string_keys(self):
        """
        fl.util.Bureau can use string keys.

        """

        import fl.util

        soi          = fl.util.Bureau()
        value        = 1234
        soi['field'] = value

        assert soi['field'] == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_store_integer_values(self):
        """
        fl.util.Bureau can store and retrieve integer values.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value     = 1234
        soi.field = value

        assert soi.field == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_store_floating_point_values(self):
        """
        fl.util.Bureau can store and retrieve floating point values.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value     = 1.234
        soi.field = value

        assert soi.field == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_store_string_values(self):
        """
        fl.util.Bureau can store and retrieve string values.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value     = 'test_value'
        soi.field = value

        assert soi.field == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_store_arrays_of_integer_values(self):
        """
        fl.util.Bureau can store and retrieve arrays of integer values.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value     = [1, 2, 3, 4]
        soi.field = value

        assert soi.field == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_store_tuples_of_integer_values(self):
        """
        fl.util.Bureau can store and retrieve tuples of integer values.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value     = (1, 2, 3, 4)
        soi.field = value

        assert soi.field == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_store_sets_of_integer_values(self):
        """
        fl.util.Bureau can store and retrieve sets of integer values.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value     = {1, 2, 3, 4}
        soi.field = value

        assert soi.field == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_store_nested_structures(self):
        """
        fl.util.Bureau can store and retrieve arrays of integer values.

        """

        import fl.util

        soi         = fl.util.Bureau()
        soi.field_1 = 1234
        soi.field_2 = 1.234
        soi.field_3 = 'onetwothreefour'
        soi.field_4 = [1, 2, 3, 4]
        soi.field_5 = (1, 2, 3, 4)
        soi.field_6 = {1, 2, 3, 4}

        assert soi.field_1 == 1234
        assert soi.field_2 == 1.234
        assert soi.field_3 == 'onetwothreefour'
        assert soi.field_4 == [1, 2, 3, 4]
        assert soi.field_5 == (1, 2, 3, 4)
        assert soi.field_6 == {1, 2, 3, 4}

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_serialised_to_a_string(self):
        """
        fl.util.Bureau can be serialised to a string.

        """

        import fl.util

        soi       = fl.util.Bureau()
        soi.field = b'value'

        assert str(soi) == "{'field': b'value'}"

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_fields_on_demand(self):
        """
        fl.util.Bureau creates nested bureaus as fields on demand.

        """

        import fl.util

        soi    = fl.util.Bureau()
        nested = soi['field1']['field2']['field3']

        assert isinstance(nested, fl.util.Bureau)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_write_to_nested_bureaus_as_fields_on_demand(self):
        """
        fl.util.Bureau creates nested bureaus for writing on demand.

        """

        import fl.util

        soi    = fl.util.Bureau()
        value  = 100
        soi['field1']['field2']['field3'] = value

        assert soi['field1']['field2']['field3'] == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_attributes(self):
        """
        fl.util.Bureau creates nested bureaus as attributes on demand.

        """

        import fl.util

        soi                      = fl.util.Bureau()
        value                    = 100
        soi.field1.field2.field3 = value

        assert soi['field1']['field2']['field3'] == value
        assert soi.field1.field2.field3          == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_a_string_path(self):
        """
        fl.util.Bureau creates nested bureaus as a string path on demand.

        """

        import fl.util

        soi                         = fl.util.Bureau()
        value                       = 100
        soi['field1.field2.field3'] = value

        assert soi['field1']['field2']['field3'] == value
        assert soi['field1.field2.field3']       == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_an_iterable_path(self):
        """
        fl.util.Bureau creates nested bureaus as a path on demand.

        """

        import fl.util

        soi                               = fl.util.Bureau()
        value                             = 100
        soi[('field1','field2','field3')] = value

        assert soi['field1']['field2']['field3'] == value
        assert soi[('field1','field2','field3')] == value


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_a_pathform_attribute(self):
        """
        fl.util.Bureau creates nested bureaus as a pathform attrib on demand.

        """

        import fl.util

        soi                      = fl.util.Bureau(_path_delimiter = '_')
        value                    = 100
        soi.field1_field2_field3 = value

        assert soi['field1']['field2']['field3'] == value
        assert soi.field1_field2_field3          == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_support_undo(self):
        """
        fl.util.Bureau fields can support undoable mutations.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value_1   = 100
        value_2   = 200
        soi.field = value_1
        assert soi.field == value_1
        soi.field = value_2
        assert soi.field == value_2
        soi.undo()
        assert soi.field == value_1
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_support_redo(self):
        """
        fl.util.Bureau fields can support undoable and redoable mutations.

        """

        import fl.util

        soi       = fl.util.Bureau()
        value_1   = 100
        value_2   = 200
        soi.field = value_1
        assert soi.field == value_1
        soi.field = value_2
        assert soi.field == value_2
        soi.undo()
        assert soi.field == value_1
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None
        soi.redo()
        assert soi.field == value_1
        soi.redo()
        assert soi.field == value_2

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_trigger_rules(self):
        """
        Editing fl.util.Bureau fields can trigger rules.

        """

        value_written = None
        path_written  = None

        # ---------------------------------------------------------------------
        def _test_action(data, tup_cmd):
            """
            Test action.

            """

            nonlocal value_written
            nonlocal path_written

            value_written = tup_cmd[0].value_new
            path_written  = tup_cmd[0].path

        import fl.rule
        import fl.util

        soi   = fl.util.Bureau()
        key   = 'field_1'
        value = 100
        soi.rule(cond = fl.rule.always(),
                 act  = _test_action)

        with soi.batch_context():
            soi[key] = value

        assert value_written == value
        assert path_written  == (key,)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_trigger_rules_on_nested_fields(self):
        """
        Editing fl.util.Bureau fields will trigger relevant rules.

        """

        value_written = None
        path_written  = None

        # ---------------------------------------------------------------------
        def _test_action(data, tup_cmd):
            """
            Test action.

            """

            nonlocal value_written
            nonlocal path_written

            value_written = tup_cmd[0].value_new
            path_written  = tup_cmd[0].path

        import fl.rule
        import fl.util

        soi    = fl.util.Bureau()
        value1 = 100
        value2 = 200
        soi.rule(cond = fl.rule.is_root_in(('field_1','field_2')),
                 act  = _test_action)

        with soi.batch_context():
            soi.field_1.field_2 = value1
            soi.field3          = value2

        assert value_written == value1
        assert path_written  == ('field_1', 'field_2')

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_trigger_rules_if_nested_field_is_changed(self):
        """
        fl.util.Bureau rules are triggered if a nested field is changed.

        """

        value_written = None
        path_written  = None

        # ---------------------------------------------------------------------
        def _test_action(data, tup_cmd):
            """
            Test action.

            """

            nonlocal value_written
            nonlocal path_written

            value_written = tup_cmd[0].value_new
            path_written  = tup_cmd[0].path

        import fl.rule
        import fl.util

        soi = fl.util.Bureau()
        soi.rule(cond = fl.rule.is_root_in(('field_1',)),
                 act  = _test_action)

        with soi.batch_context():
            soi.field_1.field_2 = 100

        assert value_written == 100
        assert path_written  == ('field_1', 'field_2')

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_represent_a_flat_structure_as_a_key_value_tuple(self):
        """
        fl.util.Bureau containers can be represented as key-value tuples.

        """

        import fl.util

        soi   = fl.util.Bureau()
        soi.a = 100
        soi.b = 200
        soi.c = 300
        soi.d = 400

        assert soi.to_tuple() == ((('a',), 100),
                                  (('b',), 200),
                                  (('c',), 300),
                                  (('d',), 400))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_represent_a_nested_structure_as_a_key_value_tuple(self):
        """
        fl.util.Bureau containers can be represented as key-value tuples.

        """

        import fl.util

        soi     = fl.util.Bureau()
        soi.a.c = 100
        soi.a.d = 200
        soi.b.e = 300
        soi.b.f = 400

        assert soi.to_tuple() == ((('a', 'c'), 100),
                                  (('a', 'd'), 200),
                                  (('b', 'e'), 300),
                                  (('b', 'f'), 400))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_represent_structures_with_lists_as_a_key_value_tuple(self):
        """
        fl.util.Bureau containers can be represented as key-value tuples.

        """

        import fl.util

        soi     = fl.util.Bureau()
        soi.a.c = 1234
        soi.a.d = 5678
        soi.b.e = [10, 20, 30, 40]
        soi.b.f = (50, 60, 70, 80)

        assert soi.to_tuple() == ((('a','c'), 1234),
                                  (('a','d'), 5678),
                                  (('b','e'), [10, 20, 30, 40]),
                                  (('b','f'), (50, 60, 70, 80)))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_key_value_tuple(self):
        """
        fl.util.Bureau containers can be updated using key-value tuples.

        """

        import fl.util

        soi = fl.util.Bureau()
        soi.from_tuple(((('a', 'c'), 100),
                        (('a', 'd'), 200),
                        (('b', 'e'), 300),
                        (('b', 'f'), 400)))

        assert soi.a.c == 100
        assert soi.a.d == 200
        assert soi.b.e == 300
        assert soi.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_tuple_rooted_key_value_tuple(self):
        """
        fl.util.Bureau containers can be partly updated using key-value tuples.

        """

        import fl.util

        soi = fl.util.Bureau()
        soi.from_tuple(path_root = ('root', 'path'),
                       tup_kv    = ((('a', 'c'), 100),
                                    (('a', 'd'), 200),
                                    (('b', 'e'), 300),
                                    (('b', 'f'), 400)))

        assert soi.root.path.a.c == 100
        assert soi.root.path.a.d == 200
        assert soi.root.path.b.e == 300
        assert soi.root.path.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_string_rooted_key_value_tuple(self):
        """
        fl.util.Bureau containers can be partly updated using key-value tuples.

        """

        import fl.util

        soi = fl.util.Bureau()
        soi.from_tuple(path_root = 'root.path',
                       tup_kv    = ((('a', 'c'), 100),
                                    (('a', 'd'), 200),
                                    (('b', 'e'), 300),
                                    (('b', 'f'), 400)))

        assert soi.root.path.a.c == 100
        assert soi.root.path.a.d == 200
        assert soi.root.path.b.e == 300
        assert soi.root.path.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_represented_as_a_nested_dict(self):
        """
        fl.util.Bureau containers can be represented as a nested dict.

        """

        import fl.util

        soi     = fl.util.Bureau()
        soi.a.c = 100
        soi.a.d = 200
        soi.b.e = 300
        soi.b.f = 400

        assert soi.to_dict()   == {'a': {'c': 100, 'd': 200},
                                   'b': {'e': 300, 'f': 400}}
        assert soi.a.to_dict() == {'c': 100, 'd': 200}
        assert soi.b.to_dict() == {'e': 300, 'f': 400}

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_nested_dict(self):
        """
        fl.util.Bureau containers can be updated from a nested dict.

        """

        import fl.util

        soi = fl.util.Bureau()
        soi.from_dict({'a': {'c': 100, 'd': 200},
                       'b': {'e': 300, 'f': 400}})

        assert soi.a.c == 100
        assert soi.a.d == 200
        assert soi.b.e == 300
        assert soi.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_tuple_rooted_nested_dict(self):
        """
        fl.util.Bureau containers can be updated from a nested dict.

        """

        import fl.util

        soi = fl.util.Bureau()
        soi.from_dict(path_root = ('root', 'path'),
                      map_item  = {'a': {'c': 100, 'd': 200},
                                   'b': {'e': 300, 'f': 400}})

        assert soi.root.path.a.c == 100
        assert soi.root.path.a.d == 200
        assert soi.root.path.b.e == 300
        assert soi.root.path.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_string_rooted_nested_dict(self):
        """
        fl.util.Bureau containers can be updated from a nested dict.

        """

        import fl.util

        soi = fl.util.Bureau()
        soi.from_dict(path_root = 'rootpath',
                      map_item  = {'a': {'c': 100, 'd': 200},
                                   'b': {'e': 300, 'f': 400}})

        assert soi.rootpath.a.c == 100
        assert soi.rootpath.a.d == 200
        assert soi.rootpath.b.e == 300
        assert soi.rootpath.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_allows_batching_updates_via_context_manager(self, monkeypatch):
        """
        fl.util.Bureau containers provide a batched-updates context manager.

        Test that 'Bureau' objects provide a
        context manager for batch updates.

        This test creates a 'Bureau' instance and
        uses a 'batch_context' to perform a series
        of operations including adding, deleting,
        editing, undoing, and redoing actions.

        Mocking is used to override the 'time'
        function for consistency in the batch's
        timestamp.

        The test asserts that the final batch,
        once transformed into a tuple of tuples,
        matches the expected sequence of operations
        and values.

        """

        import fl.util

        soi = fl.util.Bureau()

        # ---------------------------------------------------------------------
        ts = '1234.5678'
        def _mock_time():
            """
            Mock for time.time()

            """
            return ts

        with monkeypatch.context() as patch:

            patch.setattr(time, 'time', _mock_time)

            with soi.batch_context() as batch:

                soi.a.c = 100
                soi.a.d = 200
                soi.b.e = 300
                del soi.a
                soi.b.f = 400
                soi.b.f = 500
                soi.undo()
                soi.redo()

        tup_tup_batch = tuple(tuple(item) for item in batch)

        import pprint
        pprint.pprint(tup_tup_batch)

        assert tup_tup_batch == (('add',  0, ts, ('a', 'c'), 100,  None ),
                                 ('add',  1, ts, ('a', 'd'), 200,  None ),
                                 ('add',  2, ts, ('b', 'e'), 300,  None ),
                                 ('del',  3, ts, ('a', 'c'), None, 100  ),
                                 ('del',  4, ts, ('a', 'd'), None, 200  ),
                                 ('add',  5, ts, ('b', 'f'), 400,  None ),
                                 ('edit', 6, ts, ('b', 'f'), 500,  400  ),
                                 ('undo', 7, ts, ('b', 'f'), 400,  500  ),
                                 ('redo', 8, ts, ('b', 'f'), 500,  400  ))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_updates_data_from_batched_commands(self):
        """
        fl.util.Bureau containers can be updated with batches of commands.

        Test that 'Bureau' objects can update
        their data from a batch record consisting
        of multiple commands.

        This test creates a 'Bureau' instance and
        a batch of commands including 'edit',
        'undo' and 'redo' operations. The batch
        is used to update the 'Bureau' instance
        using the 'from_batch' method. The test
        concludes by asserting that the final
        values of the 'Bureau' object match the
        expected results after batch updates.

        """

        import fl.util

        batch = (('edit', 0, 0.0, ('a', 'c'), 100, None ),
                 ('edit', 1, 0.0, ('a', 'd'), 200, None ),
                 ('edit', 2, 0.0, ('b', 'e'), 300, None ),
                 ('edit', 3, 0.0, ('b', 'f'), 400, None ),
                 ('edit', 4, 0.0, ('b', 'f'), 500, 400  ),
                 ('undo', 5, 0.0, ('b', 'f'), 400, 500  ),
                 ('redo', 6, 0.0, ('b', 'f'), 500, 400  ))

        soi = fl.util.Bureau()
        soi.from_batch(batch)

        assert soi.a.c == 100
        assert soi.a.d == 200
        assert soi.b.e == 300
        assert soi.b.f == 500


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_synchronizes_data_between_bureaus_using_batch_context(self):
        """
        fl.util.Bureau containers can be kept in synch with another bureau.

        Test the ability of 'Bureau' objects to
        sync their data with another 'Bureau'
        instance using batch_context.

        This test operates by creating two 'Bureau'
        instances, soi_01 and soi_02. Initially,
        data is added to soi_01 within a batch_context,
        and then this batch is used to sync soi_02
        with soi_01. Equality of soi_01 and soi_02
        is then asserted.

        The process is repeated in reverse, adding
        different data to soi_02 and syncing it to
        soi_01 and finally checking equality of
        both 'Bureau' instances again.

        """

        import fl.util

        soi_01 = fl.util.Bureau()
        soi_02 = fl.util.Bureau()

        with soi_01.batch_context() as batch_01:
            soi_01.a.c = 10
            soi_01.a.d = 20
            soi_01.b.e = 30
            soi_01.b.f = 50

        soi_02.from_batch(batch_01)

        assert soi_02 == soi_01

        with soi_02.batch_context() as batch_02:
            soi_02.a.c = 600
            soi_02.a.d = 700
            soi_02.b.e = 800
            soi_02.b.f = 900

        soi_01.from_batch(batch_02)

        assert soi_01 == soi_02
