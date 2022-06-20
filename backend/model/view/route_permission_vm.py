from typing import Any

from pydantic import BaseModel


class RoutePermissionVm(BaseModel):
    route_path: str
    need_login: bool
    allow_all: bool

    menu_list: Any
    role_list: Any
