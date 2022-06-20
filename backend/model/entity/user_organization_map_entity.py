
from sqlalchemy import Column, String

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.user_organization_map_history import UserOrganizationMapHistoryEntity


class UserOrganizationMapEntity(BasicVersionControlledEntity):
    __tablename__ = "user_organization_map"
    __history_entity__ = UserOrganizationMapHistoryEntity

    user_id = Column(String(40), index=True, comment="用户id", nullable=False, unique=True)
    organization_id = Column(String(40), index=True, comment="组织id", nullable=False)
