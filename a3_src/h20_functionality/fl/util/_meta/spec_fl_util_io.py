# -*- coding: utf-8 -*-
"""
Functional specification for fl.util.io

"""


import textwrap
import time
import warnings

import pytest


# =============================================================================
class SpecifyFlUtilIo:
    """
    Spec for the fl.util.io module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        fl.util.io can be imported with no errors.

        """
        import fl.util.io


# =============================================================================
class SpecifyFlUtilIoSerialize:
    """
    Spec for the fl.util.io.serialize function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_pickle(self):
        """
        fl.util.io.serialize can serialize a dict to pickle

        """
        import fl.util
        map_input = dict(a = 1, b = 2)
        (bytes_output, map_error) = fl.util.io.serialize(map_input, 'pickle')

        assert map_error is None
        assert bytes_output == b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02u.'


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_xml(self):
        """
        fl.util.io.serialize can serialize a dict to xml

        """
        import fl.util
        map_input  = dict(a = dict(b = 1, c = 2, d = 3))
        (str_output, map_error) = fl.util.io.serialize(map_input, 'xml')

        assert map_error is None
        assert str_output == textwrap.dedent(
                                        """
                                        <?xml version="1.0" encoding="utf-8"?>
                                        <a>
                                          <b>1</b>
                                          <c>2</c>
                                          <d>3</d>
                                        </a>
                                        """).strip()

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_json(self):
        """
        fl.util.io.serialize can serialize a dict to json

        """
        import fl.util
        map_input  = dict(a = dict(b = 1, c = 2, d = 3))
        (str_output, map_error) = fl.util.io.serialize(map_input, 'json')

        assert str_output == textwrap.dedent(
                                        """
                                        {
                                          "a": {
                                            "b": 1,
                                            "c": 2,
                                            "d": 3
                                          }
                                        }
                                        """).strip()

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_toml(self):
        """
        fl.util.io.serialize can serialize a dict to toml

        """
        import fl.util
        map_input  = dict(a = dict(b = 1, c = 2, d = 3))
        (str_output, map_error) = fl.util.io.serialize(map_input, 'toml')

        assert str_output == textwrap.dedent(
                                        """
                                        [a]
                                        b = 1
                                        c = 2
                                        d = 3
                                        """).strip()

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_yaml(self):
        """
        fl.util.io.serialize can serialize a dict to yaml

        """
        import fl.util
        map_input  = dict(a_key = dict(a_long_key = 1, short = 2, tiny = 3))
        (str_output, map_error) = fl.util.io.serialize(map_input, 'yaml')

        assert str_output == textwrap.dedent(
                                        """
                                        a_key:
                                          a_long_key: 1
                                          short: 2
                                          tiny: 3
                                        """).strip()


# =============================================================================
class SpecifyFlUtilIoDeserialize:
    """
    Spec for the fl.util.io.deserialize function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_pickle(self):
        """
        fl.util.io.deserialize can deserialize a dict from pickle bytes.

        Please note that XML does not inherently
        distinguish between different datatypes,
        and treats everything as text. This means
        that unless an application-specific type
        annotation mechanism is used, then all
        type information will be lost when using
        xml.

        """
        import fl.util
        bytes_input = b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02u.'
        (map_output, map_error) = fl.util.io.deserialize(bytes_input, 'pickle')
        assert map_error is None
        assert map_output == dict(a = 1, b = 2)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_xml(self):
        """
        fl.util.io.deserialize can deserialize a dict from xml

        Please note that XML does not inherently
        distinguish between different datatypes,
        and treats everything as text. This means
        that unless an application-specific type
        annotation mechanism is used, then all
        type information will be lost when using
        xml.

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                <?xml version="1.0" encoding="utf-8"?>
                                <root>
                                  <a>1</a>
                                  <b>2.0</b>
                                  <c>Some string</c>
                                  <d>
                                    <e>345</e>
                                  </d>
                                </root>
                                """).strip()
        (map_output, map_error) = fl.util.io.deserialize(str_input, 'xml')
        assert map_error is None
        assert map_output == dict(a = 1,
                                  b = 2.0,
                                  c = 'Some string',
                                  d = dict(e = 345))


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_json(self):
        """
        fl.util.io.deserialize can deserialize a dict from json

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                {
                                  "a": 1,
                                  "b": 2.0,
                                  "c": "Some string",
                                  "d": {
                                    "e": 345
                                  }
                                }
                                """).strip()
        (map_output, map_error) = fl.util.io.deserialize(str_input, 'json')
        assert map_error is None
        assert map_output == dict(a = 1,
                                  b = 2.0,
                                  c = 'Some string',
                                  d = dict(e = 345))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_toml(self):
        """
        fl.util.io.deserialize can deserialize a dict from toml

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                [a]
                                b = 1
                                c = 2
                                d = 3
                                """).strip()
        (map_output, map_error) = fl.util.io.deserialize(str_input, 'toml')
        assert map_error is None
        assert map_output == dict(a = dict(b = 1, c = 2, d = 3))


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_yaml(self):
        """
        fl.util.io.deserialize can deserialize a dict from yaml

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                a: 1
                                b: 2.0
                                c: "Some string"
                                d:
                                  e: 345
                                """).strip()
        (map_output, map_error) = fl.util.io.deserialize(str_input, 'yaml')
        assert map_error is None
        assert map_output == dict(a = 1,
                                  b = 2.0,
                                  c = 'Some string',
                                  d = dict(e = 345))
