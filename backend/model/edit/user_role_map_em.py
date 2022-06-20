from datetime import datetime
from typing import Optional

from backend.model.basic_model import BasicModel


class UserRoleMapEm(BasicModel):
    user_id: str
    role_id: str
    last_enabled_time: Optional[datetime]
