import importlib

from os.path import splitext


def get_class_path(obj):
    obj_type = type(obj)
    return "{}.{}".format(obj_type.__module__, obj_type.__name__)


def import_path(type_path):
    module_path, type_name = splitext(type_path)
    module = importlib.import_module(module_path)
    return getattr(module, type_name)
