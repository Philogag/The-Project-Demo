from sqlalchemy import Column, String, DateTime, Integer

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.master_people_history import MasterPeopleHistoryEntity


class MasterPeopleEntity(BasicVersionControlledEntity):
    __tablename__ = "st_master_people"
    __history_entity__ = MasterPeopleHistoryEntity

    team_id = Column(String(40), comment="代表队id", nullable=False)
    team_group_id = Column(String(40), comment="参赛组id", nullable=False)

    people_name = Column(String(255), comment="姓名")
    people_gender = Column(String(10), comment="性别")
    people_birth = Column(DateTime(timezone=True), comment="生日")

    number_cloth_id = Column(Integer, comment="号码布编号")
    number_cloth = Column(String(20), comment="号码布")
