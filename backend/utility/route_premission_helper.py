from typing import Callable, List, Optional

from flask import Blueprint
from pydantic import BaseModel

from backend.data.system_enum import EnumRoleCode
from backend.utility.enum_helper import enum_to_name_set
from backend.utility.singleton_helper import singleton_class

all_roles_set = enum_to_name_set(EnumRoleCode)


class RoutePermission(BaseModel):
    group: str = "通用"
    name: Optional[str]
    allow_all: Optional[bool]
    login_required: Optional[bool]


@singleton_class
class RoutePermissionMap(dict):
    def __init__(self):
        super().__init__()
        self.default_permission = RoutePermission()
        self.default_fields = [
            "group",
            "allow_all",
            "login_required",
        ]

    def set_default_permission(self, default_permission: RoutePermission, default_fields: List[str]=None):
        """
        Set the default permission of the undefined routes
        """
        self.default_permission = default_permission
        if default_fields:
            self.default_fields = default_fields

    def __setitem__(self, entrypoint, permission: RoutePermission):
        super().__setitem__(entrypoint, permission)

    def __getitem__(self, key) -> RoutePermission:
        if key in self.keys():
            item = super().__getitem__(key)
            for field in self.default_fields:
                if getattr(item, field) is None:
                    setattr(item, field, getattr(self.default_permission, field))
            return item
        else:
            return self.default_permission


class RoutePermissionHelper:
    def __init__(self, blueprint: Blueprint, group: str = None):
        """
        通过蓝图名和函数名定位路由并配置权限
        """
        self.blueprint_name = blueprint.name
        self.group_name = group if group else blueprint.name

    def set(
        self,
        login_required: bool = None,
        allow_all: bool = None,
        name: str = None
    ) -> Callable:
        """
        通过蓝图名和函数名定位路由并配置权限
        permitted_roles = include_roles + (all_roles if allow_all) - exclude_roles
        如果 permitted_roles 中包含 ”*“ 则强制 allow_all
        """

        def decorator(f: Callable):
            entrypoint = self.blueprint_name + "." + f.__name__
            RoutePermissionMap()[entrypoint] = RoutePermission(
                group=self.group_name,
                login_required=login_required,
                allow_all=allow_all,
                name=name if name else entrypoint,
            )
            return f

        return decorator
