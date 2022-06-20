from sqlalchemy import Column, DateTime, String

from backend.model.basic_entity import BasicEntity


class RobotEntity(BasicEntity):
    __tablename__ = "st_robot"

    name = Column(String(255), comment="名称", unique=True)
    code = Column(String(255), comment="代码", unique=True, nullable=True)

    permission_end_at = Column(DateTime(timezone=True), nullable=True)
