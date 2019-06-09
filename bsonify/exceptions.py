class BsonifyError(Exception):
    """
    Most generic exception in bsonify library.
    """
    pass


class BsonifyToDictifyError(BsonifyError):
    pass


class UnknownObjectToDictifyError(BsonifyToDictifyError):

    def __init__(self, problematic_obj, *args):
        super(UnknownObjectToDictifyError, self).__init__(*args)
        self.problematic_obj = problematic_obj
