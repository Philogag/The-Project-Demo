"""
权限详情
"""

from backend.model.basic_model import BasicModel


class DataPermissionDetailEm(BasicModel):
    data_permission_id: str
    permitted_object_category: str
    permitted_object_id: str
