"""
权限授权详情历史实体
"""
from sqlalchemy import Column, String

from backend.model.basic_entity import BasicHistoryEntity


class DataPermissionDetailHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_data_permission_detail_history"

    data_permission_id = Column(String(40), comment="授权信息", nullable=False)

    permitted_object_category = Column(String(255), comment="授权项目类型", nullable=False)
    permitted_object_id = Column(String(40), comment="授权项目ID", nullable=False)
