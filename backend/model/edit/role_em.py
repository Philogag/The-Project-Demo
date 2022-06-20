from typing import Optional

from backend.model.basic_model import BasicModel


class RoleEm(BasicModel):

    role_name: str
    code: Optional[str]

    comment: Optional[str]

    enabled: bool = True
    editable: bool = True
