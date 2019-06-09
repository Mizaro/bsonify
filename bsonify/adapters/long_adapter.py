import six

from bsonify.adapters.base import BsonifyAdapter


class LongAdapter(BsonifyAdapter):
    KEY = "value"

    def types_filter(self):
        return six.integer_types

    def _to_dict(self, obj):
        return {self.KEY: six.text_type(obj)}

    def _from_dict(self, dictionary, obj_type):
        return obj_type(dictionary[self.KEY])
