from sqlalchemy import Column, String, Integer

from backend.model.basic_entity import BasicEntity


class AreaEntity(BasicEntity):
    __tablename__ = "st_area"

    name = Column(String(255), comment="名称", nullable=False)
    parent_id = Column(String(40), comment="父节点", nullable=True)
    level = Column(Integer, comment="层级")