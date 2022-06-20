from typing import Type, TypeVar

ClassValue = TypeVar(name="ClassValue")


def singleton_class(cls: Type[ClassValue]):
    """
    单例类包装器

    @singleton_class
    class A():
        ...

    a1 = A()
    a2 = A()
    """
    _instance = {}

    def _singleton(*args, **kargs) -> ClassValue:
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
