from typing import List

from pydantic import BaseModel


class RoleMenuVm(BaseModel):
    role_id: str
    menu_id_list: List[str]
