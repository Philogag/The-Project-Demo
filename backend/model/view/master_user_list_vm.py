from datetime import datetime
from typing import Optional, List

from backend.model.basic_model import BasicEditModel
from backend.model.edit.role_em import RoleEm


class MasterUserListVm(BasicEditModel):
    username: str
    is_active: bool
    last_login_at: Optional[datetime]

    organization_id: Optional[str]
    organization_name: Optional[str]

    role_list: List[RoleEm] = []

