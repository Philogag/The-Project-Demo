"""
角色实体
"""
from sqlalchemy import Column, String, Boolean

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.role_history import RoleHistoryEntity


class RoleEntity(BasicVersionControlledEntity):
    __tablename__ = "st_role"
    __history_entity__ = RoleHistoryEntity

    role_name = Column(String(255), comment="角色名称", unique=True)
    code = Column(String(255), comment="代码", nullable=True, unique=True)
    comment = Column(String(1000), comment="备注", nullable=True)
    editable = Column(Boolean, comment="可编辑", default=True)
    enabled = Column(Boolean, comment="启用", default=True)
