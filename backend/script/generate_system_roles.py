"""
注册系统角色
"""
from flask_script import Command

from backend.blueprint import get_system_init_robot
from backend.data.system_enum import EnumRoleCode
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.role_em import RoleEm
from backend.repository.role_repository import RoleRepository
from backend.utility.enum_helper import enum_to_dict


class GenerateSystemRoles(Command):
    @classmethod
    def run(cls):
        data = enum_to_dict(EnumRoleCode)

        with SqlAlchemyUOW(
            handler=get_system_init_robot(),
            action="generate_system_role",
            action_params=data,
        ) as uow:
            exist_role_em = RoleRepository.get_all_role()
            exist_role_code = {
                em.code
                for em in exist_role_em
            }
            for code, name in data.items():
                if code not in exist_role_code:
                    RoleRepository.create_role(
                        role_em=RoleEm(code=code, role_name=name),
                        transaction=uow.transaction,
                    )
