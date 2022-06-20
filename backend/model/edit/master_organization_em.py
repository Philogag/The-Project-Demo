from typing import Optional

from backend.model.basic_model import BasicEditModel


class MasterOrganizationEm(BasicEditModel):
    name: str
    code: str
    area_id: str
    comment: Optional[str]
    enabled: bool
    guest_enabled: Optional[bool]
