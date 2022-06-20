from enum import Enum
from typing import Type

from backend.data import system_enum
from backend.utility.error_helper import BusinessError


def get_enum_class_by_underline_name(enum_name: str) -> Type[Enum]:
    """
    get system enum by name
    :params enum_name: str like "role_code"
    :return : EnumClass like EnumRoleCode
    """
    enum_class_name = "Enum" + "".join([s.capitalize() for s in enum_name.split('_')])
    try:
        return getattr(system_enum, enum_class_name)
    except Exception:
        raise BusinessError("枚举 {0} 不存在".format(enum_class_name))
