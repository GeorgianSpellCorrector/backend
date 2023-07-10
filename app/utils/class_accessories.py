import importlib
import inspect

from pydantic import BaseModel


def get_meta_classes(package_name):
    # Import the package
    package = importlib.import_module(package_name)

    # Get all the members (classes, functions, etc.) in the package
    members = inspect.getmembers(package)

    # Iterate over the members and filter Meta classes
    meta_classes = []
    for _, obj in members:
        if inspect.ismodule(obj):
            for _, _obj in inspect.getmembers(obj):
                if inspect.isclass(_obj) and issubclass(_obj, BaseModel) and hasattr(_obj, 'Meta'):
                    meta_classes.append(_obj.Meta)
    return meta_classes
