"""
角色实体History
"""
from sqlalchemy import Column, String, Boolean

from backend.model.basic_entity import BasicHistoryEntity


class RoleHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_role_history"

    role_name = Column(String(255), comment="角色名称")
    code = Column(String(255), comment="代码", nullable=True)
    comment = Column(String(1000), comment="备注", nullable=True)
    editable = Column(Boolean, comment="可编辑", default=True)
    enabled = Column(Boolean, comment="启用", default=True)
