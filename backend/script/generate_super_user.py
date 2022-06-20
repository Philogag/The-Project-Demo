"""
生成超级管理员用户
"""
import getpass

from flask_script import Command

from backend.blueprint import get_system_init_robot
from backend.data.system_enum import EnumRoleCode
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.master_user_em import MasterUserRegisterEm
from backend.repository.role_repository import RoleRepository
from backend.repository.user_role_map_repository import UserRoleMapRepository
from backend.service.master_user_service import try_register_user


class GenerateSuperUser(Command):
    """生成超级管理员用户"""
    @classmethod
    def run(cls):
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        password_confirm = getpass.getpass("Confirm password: ")

        with SqlAlchemyUOW(
            handler=get_system_init_robot(),
            action="generate_super_user",
            action_params={
                "username": username
            },
        ) as uow:
            user_id = try_register_user(
                user_em=MasterUserRegisterEm(
                    username=username,
                    password=password,
                    password_confirm=password_confirm,
                ),
                transaction=uow.transaction,
            )

            super_user_role = RoleRepository.get_role_by_code(
                EnumRoleCode.super_admin.name,
            )

            UserRoleMapRepository.add_user_role_map(
                user_id=user_id,
                role_id=super_user_role.id,
                transaction=uow.transaction,
            )

            print("OK.")
