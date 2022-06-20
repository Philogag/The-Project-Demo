"""
用户实体
"""
from sqlalchemy import Boolean, Column, String, DateTime

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.master_user_history import (
    MasterUserHistoryEntity
)


class MasterUserEntity(BasicVersionControlledEntity):
    __tablename__ = "st_master_user"
    __history_entity__ = MasterUserHistoryEntity

    username = Column(String(40), comment="用户名", nullable=False, unique=True)
    password = Column(String(40), comment="密码", nullable=False)
    salt = Column(String(8), comment="盐", nullable=False)
    last_login_at = Column(DateTime(timezone=True), comment="最后登录", nullable=True)
    is_active = Column(Boolean, default=True, comment="是否启用")
