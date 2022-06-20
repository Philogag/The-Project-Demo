"""
授权历史实体
"""

from sqlalchemy import Column, DateTime, String

from backend.model.basic_entity import BasicHistoryEntity


class DataPermissionHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_data_permission_history"

    authorized_object_category = Column(String(255), comment="被授权实体类型", nullable=False)
    authorized_object_id = Column(String(40), comment="被授权实体ID", nullable=False)

    begin_at = Column(DateTime(timezone=True), comment="授权起始时间", nullable=True)
    end_at = Column(DateTime(timezone=True), comment="授权起始时间", nullable=True)

    permitted_object_category = Column(String(255), comment="授权项目类型", nullable=False)
    permission_category = Column(String(255), comment="授权类型", nullable=False)
