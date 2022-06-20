from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Type

from backend.model.basic_selection_vm import BasicSelectionVm
from backend.utility.error_helper import BusinessError


def enum_to_dict(enum_cls: Type[Enum]) -> Dict[str, str]:
    result = {}
    for name, value in enum_cls.__members__.items():
        result[name] = value.value
    return result


def enum_to_tuple(enum_cls: Type[Enum]) -> List[Tuple[str, str]]:
    result = []
    for name, value in enum_cls.__members__.items():
        result.append((name, value.value))
    return result


def enum_to_value_name_dict(enum_cls: Type[Enum]) -> Dict[str, str]:
    result = {}
    for name, value in enum_cls.__members__.items():
        result[value.value] = name
    return result


def enum_to_selection(enum_cls: Type[Enum]) -> List[BasicSelectionVm]:
    result = []
    for name, value in enum_cls.__members__.items():
        result.append(BasicSelectionVm(
            label=value.value,
            value=name,
        ))
    return result


def enum_to_name_set(enum_cls: Type[Enum]) -> Set[str]:
    return set(enum_cls.__members__.keys())


def enum_get_value_by_code(enum_cls: Type[Enum], key: str) -> Optional[str]:
    d = enum_to_dict(enum_cls)
    assert key in d.keys(), BusinessError("`{key}` not exist in enum `{enum_name}`".format(key=key,enum_name=enum_cls.__name__))
    return d[key]
