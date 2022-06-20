from typing import Optional

from pydantic import BaseModel


class CurrentUserInfo(BaseModel):
    id: str
    organization_id: Optional[str]
    current_role_code: str
