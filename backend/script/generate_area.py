import logging

from flask_script import Command

from backend.blueprint import get_system_init_robot
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.area_em import AreaEm
from backend.repository.area_repository import AreaRepository


class GenerateArea(Command):
    @classmethod
    def run(cls):
        with SqlAlchemyUOW(handler=get_system_init_robot(), action="import-area", action_params={}) as uow:
            with open("./build/area.csv", encoding='gbk') as f:
                for row in f.readlines():
                    if row:
                        area_id, name, parent_id, level = row.split(',')
                        try:
                            AreaRepository.create_area(
                                data=AreaEm(
                                    id=area_id,
                                    name=name,
                                    parent_id=parent_id if parent_id else None,
                                    level=level,
                                ),
                                transaction=uow.transaction,
                            )
                        except Exception:
                            pass
            logging.info("Done.")
