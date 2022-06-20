"""
用户历史实体
"""

from sqlalchemy import Boolean, Column, String, DateTime

from backend.model.basic_entity import BasicHistoryEntity


class MasterUserHistoryEntity(BasicHistoryEntity):
    __tablename__ = "st_master_user_history"

    username = Column(String(40), comment="用户名", nullable=False)
    password = Column(String(40), comment="密码", nullable=False)
    salt = Column(String(8), comment="盐", nullable=False)
    is_active = Column(Boolean, default=True, comment="是否启用")
    last_login_at = Column(DateTime(timezone=True), comment="最后登录", nullable=True)
