"""
生成基本菜单
"""

from flask_script import Command

from backend.blueprint import get_system_init_robot
from backend.data.system_enum import EnumRoleCode
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.menu_em import MenuEm
from backend.model.view.role_menu_vm import RoleMenuVm
from backend.repository.role_repository import RoleRepository
from backend.service.menu_service import create_or_update_menu_item, set_menu_id_list_for_role

basic_menu_item = [
    MenuEm(
        path="/dashboard",
        component="/dashboard/workbench/index",
        name="Dashboard",
        order=10000,
        icon="ant-design:dashboard-outlined",
        title="控制台"
    ),
    MenuEm(
        path="/system-config/menu",
        component="/system-config/menu/index",
        name="MenuConfig",
        order=19001,
        icon="gala:menu-left",
        title="菜单配置",
    ),
]


class GenerateBasicMenu(Command):
    """生成基本菜单"""
    @classmethod
    def run(cls):
        with SqlAlchemyUOW(
            handler=get_system_init_robot(),
            action="generate_basic_menu",
            action_params={},
        ) as uow:
            menu_id_list = []

            for menu_em in basic_menu_item:
                menu_id_list.append(
                    create_or_update_menu_item(menu_em, uow.transaction)
                )
            print(menu_id_list)

            set_menu_id_list_for_role(
                role_menu_vm=RoleMenuVm(
                    role_id=RoleRepository.get_role_by_code(EnumRoleCode.super_admin.name).id,
                    menu_id_list=menu_id_list,
                ),
                transaction=uow.transaction,
            )

        print("Done.")
