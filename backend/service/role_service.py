from datetime import datetime
from typing import List

from backend.data.system_enum import EnumHandlerCategory
from backend.data.transaction import Transaction
from backend.model.edit.role_em import RoleEm
from backend.model.edit.user_role_map_em import UserRoleMapEm
from backend.repository.data_permission_repository import DataPermissionRepository
from backend.repository.role_repository import RoleRepository
from backend.repository.user_role_map_repository import UserRoleMapRepository
from backend.utility.error_helper import BusinessError


def get_user_current_role(user_id: str) -> RoleEm:
    return UserRoleMapRepository.get_user_current_role_by_user_id(user_id)


def get_user_current_role_code(user_id: str) -> str:
    current_role = get_user_current_role(user_id)
    if current_role:
        return current_role.code
    else:
        raise BusinessError("无法获取用户当前角色")


def set_user_current_role(user_id: str, role_id: str, transaction: Transaction):
    urm: UserRoleMapEm = UserRoleMapRepository.get_first_entity_by_params({
        "user_id": user_id,
        "role_id": role_id,
    })
    if urm is None:
        raise BusinessError("您没有权限切换到目标角色")
    urm.last_enabled_time = datetime.now()
    UserRoleMapRepository.update_entity(
        data=urm,
        transaction=transaction,
        col_list=["last_enabled_time"],
    )


def set_user_role_list(user_id: str, role_id_list: List[str], transaction: Transaction):
    goal_role_id = set(role_id_list)
    exist_roles_id = set(map(
        lambda x: x.id,
        UserRoleMapRepository.fetch_roles_by_user_id(user_id)
    ))

    need_add_role_id = goal_role_id - exist_roles_id
    need_del_role_id = exist_roles_id - goal_role_id

    for role_id in need_add_role_id:
        UserRoleMapRepository.add_user_role_map(user_id, role_id, transaction)
    for role_id in need_del_role_id:
        UserRoleMapRepository.del_user_role_map(user_id, role_id, transaction)


def get_role_list_for_management() -> List[RoleEm]:
    return RoleRepository.get_all_role()


def create_or_update_role_item(data: RoleEm, transaction: Transaction, do_update) -> str:
    if not do_update:
        return RoleRepository.create_role(role_em=data, transaction=transaction)
    else:
        exist_role = RoleRepository.get_role_by_id(data.id)
        if exist_role and not exist_role.editable:
            raise BusinessError("该角色不可编辑")
        RoleRepository.update_menu_item(data=data, transaction=transaction)
        return data.id


def delete_role_item_by_id(role_id: str, transaction: Transaction):
    exist_role = RoleRepository.get_role_by_id(role_id)
    if exist_role and not exist_role.editable:
        raise BusinessError("该角色不可编辑")

    RoleRepository.delete_role_by_id(role_id=role_id, transaction=transaction)
    data_permissions = DataPermissionRepository.get_all_data_permission_by_params(
        params={
            "authorized_object_category": EnumHandlerCategory.role.name,
            "authorized_object_id": role_id
        }
    )

    for data_permission in data_permissions:
        DataPermissionRepository.delete_data_permission_with_detail(
            data_permission_id=data_permission.id,
            transaction=transaction
        )
