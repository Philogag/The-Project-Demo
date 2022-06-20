"""
仓库层：机器人注册
"""
from typing import Optional

from backend.data.transaction import Transaction
from backend.model.edit.robot_em import RobotEm
from backend.model.entity.robot_entity import RobotEntity
from backend.repository.basic_repository import BasicRepository


class RobotRepository(BasicRepository):
    @classmethod
    def get_by_id(cls, robot_id) -> Optional[RobotEm]:
        return RobotRepository._get_model_by_id(
            entity_cls=RobotEntity, model_cls=RobotEm, model_id=robot_id
        )

    @classmethod
    def get_by_params(cls, params) -> Optional[RobotEm]:
        return RobotRepository._get_model_by_params(
            entity_cls=RobotEntity, model_cls=RobotEm, params=params
        )

    @classmethod
    def create(cls, robot: RobotEm, transaction: Transaction) -> Optional[str]:
        return RobotRepository._insert_entity(
            entity_cls=RobotEntity, data=robot, transaction=transaction
        )
