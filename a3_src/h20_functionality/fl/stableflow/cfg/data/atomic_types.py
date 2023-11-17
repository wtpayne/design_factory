# -*- coding: utf-8 -*-
"""
Module defining how atomic data types are named and handled.

"""

import collections

import numpy


# -----------------------------------------------------------------------------
def as_dict():
    """
    Return a lookup table of information about atomic data types as a dict.

    Each entry in the table is a list of TypeInfo
    named tuples. Each TypeInfo instance contains
    the information that is needed to allocate,
    serialize and deserialize the corresponding
    atomic (fundamnetal) data type in each
    of the supported programming languages.

    The table is indexed using a string.

    Xact is intended to be used to manage and
    distribute compute bound workloads, and to
    support interoperability between Python and
    C.

    We use Numpy as a lingua franca to communicate
    between compute nodes, as Numpy data types can
    be used from both languages and are already
    familiar to many developers of quantitative
    Python applications.

    """

    map_typeinfo = dict()
    for typeinfo in _as_tuple():
        map_typeinfo[typeinfo.id] = dict(typeinfo._asdict())
    return map_typeinfo


# -----------------------------------------------------------------------------
def _as_tuple():
    """
    Return the lookup table as a tuple of named tuples.

    Each TypeInfo data structure describes how to
    map between data types in different languages.

    """

    TypeInfo = collections.namedtuple('TypeInfo',
                    ['id',     # type id.
                     'py_eq',  # True if python type is binary-compatible.
                     'c_eq',   # True if c type is binary-compatible.
                     'align',  # True if can be aligned.
                     'py',     # python type.
                     'np',     # numpy type.
                     'c'])     # c type.

    # pylint: disable=C0301
    return tuple(TypeInfo._make(tup) for tup in (
        ('py_bytearray', True,  False, True,  bytearray, None,             None,             ),   # noqa
        ('py_bool',      True,  False, True,  bool,      None,             None,             ),   # noqa
        ('py_str',       True,  False, True,  str,       None,             None,             ),   # noqa
        ('py_bytes',     True,  False, True,  bytes,     None,             None,             ),   # noqa
        ('py_dict',      True,  False, True,  dict,      None,             None,             ),   # noqa
        ('py_list',      True,  False, True,  list,      None,             None,             ),   # noqa
        ('py_set',       True,  False, True,  set,       None,             None,             ),   # noqa
        ('bool_',        True,  False, False, bool,      numpy.bool_,      None,             ),   # noqa
        ('byte',         False, True,  True,  int,       numpy.byte,       'char',           ),   # noqa
        ('short',        False, True,  True,  int,       numpy.short,      'short',          ),   # noqa
        ('intc',         False, True,  True,  int,       numpy.intc,       'int',            ),   # noqa
        ('int',          False, True,  False, int,       numpy.int_,       'int',            ),   # noqa
        ('int_',         False, True,  False, int,       numpy.int_,       'long',           ),   # noqa
        ('longlong',     False, True,  True,  int,       numpy.longlong,   'long long',      ),   # noqa
        ('intp',         False, True,  True,  int,       numpy.intp,       'void *',         ),   # noqa
        ('int8',         False, True,  True,  int,       numpy.int8,       'int8_t',         ),   # noqa
        ('int16',        False, True,  True,  int,       numpy.int16,      'int16_t',        ),   # noqa
        ('int32',        False, True,  True,  int,       numpy.int32,      'int32_t',        ),   # noqa
        ('int64',        False, True,  True,  int,       numpy.int64,      'int64_t',        ),   # noqa
        ('ubyte',        False, True,  True,  int,       numpy.ubyte,      'unsigned char',  ),   # noqa
        ('ushort',       False, True,  True,  int,       numpy.ushort,     'unsigned short', ),   # noqa
        ('uintc',        False, True,  True,  int,       numpy.uintc,      'unsigned int',   ),   # noqa
        ('uint',         True,  False, True,  int,       numpy.uint,       None,             ),   # noqa
        ('ulonglong',    False, True,  True,  int,       numpy.ulonglong,  'long long',      ),   # noqa
        ('uintp',        False, True,  True,  int,       numpy.uintp,      'void *',         ),   # noqa
        ('uint8',        False, True,  True,  int,       numpy.uint8,      'uint8_t',        ),   # noqa
        ('uint16',       False, True,  True,  int,       numpy.uint16,     'uint16_t',       ),   # noqa
        ('uint32',       False, True,  True,  int,       numpy.uint32,     'uint32_t',       ),   # noqa
        ('uint64',       False, True,  True,  int,       numpy.uint64,     'uint64_t',       ),   # noqa
        ('half',         False, False, True,  float,     numpy.half,       None,             ),   # noqa
        ('single',       False, True,  True,  float,     numpy.single,     'float',          ),   # noqa
        ('double',       False, True,  True,  float,     numpy.double,     'double',         ),   # noqa
        ('float_',       True,  False, False, float,     numpy.float_,     None,             ),   # noqa
        ('longfloat',    False, True,  True,  float,     numpy.longfloat,  'long float',     ),   # noqa
        ('float16',      False, False, True,  float,     numpy.float16,    None,             ),   # noqa
        ('float32',      False, False, True,  float,     numpy.float32,    None,             ),   # noqa
        ('float64',      False, False, True,  float,     numpy.float64,    None,             ),   # noqa
        ('csingle',      False, False, True,  float,     numpy.csingle,    None,             ),   # noqa
        ('complex_',     True,  False, False, complex,   numpy.complex_,   None,             ),   # noqa
        ('clongfloat',   False, False, True,  complex,   numpy.clongfloat, None,             ),   # noqa
        ('complex64',    False, False, True,  complex,   numpy.complex64,  None,             ),   # noqa
        ('complex128',   False, False, True,  complex,   numpy.complex128, None,             )))  # noqa
    # pylint: enable=C0301
