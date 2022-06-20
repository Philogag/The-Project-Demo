"""
权限Em
"""
from datetime import datetime
from typing import Optional

from backend.model.basic_model import BasicModel


class DataPermissionEm(BasicModel):

    authorized_object_category: str
    authorized_object_id: str

    end_at: Optional[datetime]

    permitted_object_category: str
    permission_category: str
