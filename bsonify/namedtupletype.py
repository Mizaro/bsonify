class NamedTuple(object):

    @staticmethod
    def isinstance(obj):
        return (isinstance(obj, tuple) and
                hasattr(obj, "_fields") and
                hasattr(obj, "_asdict"))
