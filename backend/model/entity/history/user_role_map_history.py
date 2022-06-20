
from sqlalchemy import Column, String, DateTime

from backend.model.basic_entity import BasicHistoryEntity


class UserRoleMapHistoryEntity(BasicHistoryEntity):
    __tablename__ = "user_role_map_history"

    user_id = Column(String(40), index=True, comment="用户id", nullable=False)
    role_id = Column(String(40), index=True, comment="角色id", nullable=False)
    last_enabled_time = Column(DateTime, comment="路由类型", nullable=True)
