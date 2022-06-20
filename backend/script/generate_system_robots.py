"""
注册系统机器人
"""
import logging

from flask_script import Command

from backend.data.system_enum import EnumRobotCode
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.robot_em import RobotEm
from backend.repository.robot_repository import RobotRepository
from backend.utility.enum_helper import enum_to_dict
from backend.utility.string_helper import generate_uuid_id


class GenerateSystemRobots(Command):
    @classmethod
    def run(cls):
        data = enum_to_dict(EnumRobotCode)

        handler = RobotRepository.get_by_params({"code": EnumRobotCode.init_robot.name})
        if handler:
            logging.info("Skip.")

        handler = RobotEm(
            id=generate_uuid_id(),
            name=EnumRobotCode.init_robot.value,
            code=EnumRobotCode.init_robot.name,
        )

        with SqlAlchemyUOW(
            handler=handler, action="generate_system_robot", action_params=data
        ) as uow:
            for code, name in data.items():
                if code == EnumRobotCode.init_robot.name:
                    RobotRepository.create(robot=handler, transaction=uow.transaction)
                else:
                    RobotRepository.create(
                        robot=RobotEm(id=generate_uuid_id(), code=code, name=name),
                        transaction=uow.transaction,
                    )
