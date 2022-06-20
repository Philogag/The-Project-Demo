from typing import List, Optional, Union

from pydantic import BaseModel, Field

from backend.data.system_enum import EnumDataPermissionCategory


class DataPermissionSetVm(BaseModel):
    authorized_object_category: str
    authorized_object_id: str
    permitted_object_category: str
    permitted_object_id: Union[str, List[str]]
    permission_category: Optional[str] = Field(default=EnumDataPermissionCategory.allow.name)
