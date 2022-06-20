from sqlalchemy import Column, String, Boolean

from backend.model.basic_entity import BasicHistoryEntity


class MasterOrganizationHistoryEntity(BasicHistoryEntity):
    __tablename__ = 'st_master_organization_history'

    name = Column(String(255), nullable=False)
    code = Column(String(255))
    area_id = Column(String(255))
    comment = Column(String(1000))
    enabled = Column(Boolean, default=True)
    guest_enabled = Column(Boolean, default=False)
