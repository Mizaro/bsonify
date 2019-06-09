from abc import abstractmethod

from bsonify.reflection import get_class_path, import_path


class BsonifyAdapter(object):

    def __init__(self, type_field_key):
        self.type_field_key = type_field_key

    def to_dict(self, obj):
        returned_dict = self._to_dict(obj)
        returned_dict[self.type_field_key] = get_class_path(obj)
        return returned_dict

    def from_dict(self, dictionary):
        a_copy = dictionary.copy()
        obj_type = import_path(a_copy.pop(self.type_field_key))
        return self._from_dict(a_copy, obj_type)

    @abstractmethod
    def types_filter(self):
        """
        :return: iterable of all the type that should have unique behavior.
        """
        pass

    @abstractmethod
    def _to_dict(self, obj):
        pass

    @abstractmethod
    def _from_dict(self, dictionary, obj_type):
        pass
