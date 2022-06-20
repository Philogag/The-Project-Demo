
from sqlalchemy import Column, String, DateTime

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.user_role_map_history import UserRoleMapHistoryEntity


class UserRoleMapEntity(BasicVersionControlledEntity):
    __tablename__ = "user_role_map"
    __history_entity__ = UserRoleMapHistoryEntity

    user_id = Column(String(40), index=True, comment="用户id", nullable=False)
    role_id = Column(String(40), index=True, comment="角色id", nullable=False)
    last_enabled_time = Column(DateTime(timezone=True), comment="路由类型", nullable=True)
