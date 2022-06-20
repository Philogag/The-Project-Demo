from sqlalchemy import Column, String

from backend.model.basic_entity import BasicHistoryEntity


class UserOrganizationMapHistoryEntity(BasicHistoryEntity):
    __tablename__ = "user_organization_map_history"

    user_id = Column(String(40), index=True, comment="用户id", nullable=False)
    organization_id = Column(String(40), index=True, comment="组织id", nullable=False)