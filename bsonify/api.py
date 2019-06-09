from datetime import datetime
from numbers import Number

import bson
import six

from bsonify.adapters.long_adapter import LongAdapter
from bsonify.exceptions import UnknownObjectToDictifyError
from bsonify.namedtupletype import NamedTuple
from bsonify.reflection import get_class_path

PRIMITIVE_TYPES = (
    six.binary_type, six.text_type, Number, bool, datetime, float,
    bson.ObjectId, type(None))

MAX_SIGNED_INTEGER = 2 ** 63 - 1


def _cannot_be_utf8(obj):
    """
    Checking whether the given
    :param obj: bytes-string to check whether is can be converted to unicode
                string.
    :type obj: L{six.binary_type}
    :return:
    """
    try:
        obj.decode("utf-8")
        return False
    except UnicodeDecodeError:
        return True


class Dictifier(object):

    def __init__(self, type_field_key, adapters=None,
                 convert_bytes_to_binary=None,
                 dictify_unsigned_long=True):
        """
        :param type_field_key: name of the key that will hold the information
                               about the type of the source object.
        :type type_field_key: C{six.text_type}
        :param adapters:
        :type adapters: C{list} of L{bsonify.adapters.base.BsonifyAdapter}
        :param convert_bytes_to_binary:
        :type convert_bytes_to_binary: C{bool}
        """
        self.type_field_key = type_field_key
        self.adapters = adapters or []
        self.convert_bytes_to_binary = (convert_bytes_to_binary
                                        if convert_bytes_to_binary is not None
                                        else six.PY2)
        self.dictify_unsigned_long = dictify_unsigned_long

    def to_dictify(self, obj, depth=-1):
        if depth == 0:
            return obj

        if (self.convert_bytes_to_binary and
                isinstance(obj, six.binary_type) and
                _cannot_be_utf8(obj)):
            return bson.Binary(obj)

        if (self.dictify_unsigned_long and
                isinstance(obj, six.integer_types) and
                obj > MAX_SIGNED_INTEGER):
            return LongAdapter(self.type_field_key).to_dict(obj)

        if isinstance(obj, PRIMITIVE_TYPES):
            return obj

        if NamedTuple.isinstance(obj):
            data_dict = obj._asdict()
        elif isinstance(obj, list):
            data_dict = [self.to_dictify(i) for i in obj]
        elif hasattr(obj, "__slots__"):
            data_dict = {x: getattr(obj, x) for x in obj.__slots__}
        elif hasattr(obj, "__dict__"):
            data_dict = obj.__dict__
        elif isinstance(obj, dict):
            data_dict = obj
        else:
            raise UnknownObjectToDictifyError(obj)

        data_dict = {
            key: self.to_dictify(value, depth - 1)
            for key, value in six.iteritems(data_dict)
        }

        data_dict[self.type_field_key] = get_class_path(obj)

        return data_dict

    def from_dictified(self, dictionary, depth=-1):
        if depth == 0:
            return dictionary

        if (self.convert_bytes_to_binary and
                isinstance(dictionary, bson.Binary)):
            return six.binary_type(dictionary)
