# -*- coding: utf-8 -*-
"""
Functional specification for the pl.stableflow.util.serialization module.

"""


# =============================================================================
class SpecifySerialize:
    """
    Spec for the serialize function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_python_unicode_string(self):
        """
        Serialize returns a python string.

        """
        import pl.stableflow.util.serialization  # pylint: disable=C0415

        original = {'a': 1, 'b': 2, 'c': 3}
        encoded = pl.stableflow.util.serialization.serialize(original)
        assert isinstance(encoded, str)

    # -------------------------------------------------------------------------
    def it_returns_a_base64_encoded_string(self):
        """
        Serialize returns a python string encoded as base64.

        """
        import re                         # pylint: disable=C0415
        import pl.stableflow.util.serialization  # pylint: disable=C0415

        original = {'a': 1, 'b': 2, 'c': 3}
        encoded = pl.stableflow.util.serialization.serialize(original)
        assert re.match(pattern = '^[-A-Za-z0-9+/]*={0,3}$',
                        string  = encoded) is not None

    # -------------------------------------------------------------------------
    def it_returns_a_compressed_string_when_the_input_has_redundant_info(self):
        """
        Serialize compresses data.

        """
        import pl.stableflow.util.serialization  # pylint: disable=C0415

        original = {
            'a_key_with_redundant_information_01': 1,
            'a_key_with_redundant_information_02': 2,
            'a_key_with_redundant_information_03': 3,
        }
        encoded = pl.stableflow.util.serialization.serialize(original)
        assert len(encoded) < len(repr(original))


# =============================================================================
class SpecifyDeserialize:
    """
    Spec for the deserialize function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_python_dict(self):
        """
        Deserialize returns a python dict.

        """
        import pl.stableflow.util.serialization  # pylint: disable=C0415

        encoded = 'eNpLtFIw5EqyUjDiSrZSMOYCABljAuk='
        decoded = pl.stableflow.util.serialization.deserialize(encoded)
        assert isinstance(decoded, dict)

    # -------------------------------------------------------------------------
    def it_does_lossless_round_tripping(self):
        """
        Serialize and deserialize can do a lossless round trip.

        """
        import pl.stableflow.util.serialization  # pylint: disable=C0415

        original = {'a': 1, 'b': 2, 'c': 3}
        encoded = pl.stableflow.util.serialization.serialize(original)
        decoded = pl.stableflow.util.serialization.deserialize(encoded)
        assert decoded == original
