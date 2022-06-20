from typing import List, Optional

from pydantic import BaseModel

from backend.model.edit.role_em import RoleEm


class MasterUserInfoVm(BaseModel):
    id: str
    username: str
    organization_id: Optional[str]
    current_role: Optional[RoleEm]
    roles: Optional[List[RoleEm]] = []
