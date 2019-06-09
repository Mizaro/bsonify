from collections import namedtuple

import bson
import pytest
import six

from bsonify.adapters.long_adapter import LongAdapter
from bsonify.api import Dictifier


class A(object):
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2


B = namedtuple("B", "x y")


class C(B):
    pass


class D(object):
    __slots__ = ["field1", "field2"]

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2


TESTS_TYPE_KEY = "%%type"


@pytest.fixture(name="dictifier")
def get_dictifier():
    return Dictifier(TESTS_TYPE_KEY)


TEST_ARGS = [
    ("basic", A(1, A("@", 5.9)), {
        "field1": 1,
        "field2": {
            "field1": "@",
            "field2": 5.9,
            TESTS_TYPE_KEY: "tests.test_sanity.A"
        },
        TESTS_TYPE_KEY: "tests.test_sanity.A"
    }),
    ("dict", {"Foo": "Bar"}, {
        "Foo": "Bar",
        TESTS_TYPE_KEY: "__builtin__.dict" if six.PY2 else 'builtins.dict'
    }),
    ("unsigned_int64", 2 ** 64, {
        LongAdapter.KEY: six.text_type(2 ** 64),
        TESTS_TYPE_KEY: "__builtin__.long" if six.PY2 else 'builtins.int'
    }),
    ("namedtuple", B(1, 2), {
        "x": 1,
        "y": 2,
        TESTS_TYPE_KEY: "tests.test_sanity.B"
    }),
    ("namedtuple_subclass", C(1, 2), {
        "x": 1,
        "y": 2,
        TESTS_TYPE_KEY: "tests.test_sanity.C"
    }),
    ("slots", D(1, 3), {
        "field1": 1,
        "field2": 3,
        TESTS_TYPE_KEY: "tests.test_sanity.D"
    }),
    ("textual_bytes_string", b"Hello World",
     u"Hello World" if six.PY2 else b"Hello World"),
    ("binary_bytes_string", b"Hello\xfc World",
     bson.Binary(b"Hello\xfc World") if six.PY2 else b"Hello\xfc World"),
]


@pytest.mark.parametrize(
    argnames=["data", "expected"],
    argvalues=[x[1:] for x in TEST_ARGS],
    ids=[x[0] for x in TEST_ARGS])
def test__io__sanity(dictifier, data, expected):
    assert dictifier.to_dictify(data) == expected

# def test__bytearray():
#     pass
#
# def test__slots_object__sanity():
#     pass
