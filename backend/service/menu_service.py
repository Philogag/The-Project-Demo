from typing import List

from backend.blueprint import get_current_user_id
from backend.data.system_enum import EnumDataPermissionCategory
from backend.data.transaction import Transaction
from backend.model.basic_tree_vm import build_tree
from backend.model.edit.data_permission_em import DataPermissionEm
from backend.model.edit.menu_em import MenuEm
from backend.model.view.menu_data_route_map_vm import MenuDataRouteMapVm
from backend.model.view.menu_tree_vm import MenuTreeVm
from backend.model.view.role_menu_vm import RoleMenuVm
from backend.repository.data_permission_detail_repository import DataPermissionDetailRepository
from backend.repository.data_permission_repository import DataPermissionRepository
from backend.repository.menu_repository import MenuRepository
from backend.service.data_permission_service import delete_data_permission_and_detail
from backend.service.master_organization_service import get_user_organization_id
from backend.service.role_service import get_user_current_role
from backend.utility.error_helper import BusinessError
from backend.utility.string_helper import is_fake_uuid


def get_current_menu_by_user() -> List[MenuTreeVm]:
    current_user_id = get_current_user_id()
    current_role = get_user_current_role(current_user_id)
    current_user_org_id = get_user_organization_id(current_user_id)

    menu_list = MenuRepository.get_current_menu(current_user_id=current_user_id, current_role_id=current_role.id)

    for menu_item in menu_list:
        menu_item.create_meta()

    result = build_tree(menu_list, order_key=lambda x: x.order)

    if current_user_org_id:
        sport_meeting_menu = get_pinned_sport_meeting_menu(
            current_role=current_role,
            current_user_id=current_user_id,
            organization_id=current_user_org_id,
        )
        result += sport_meeting_menu
    result.sort(key=lambda x: x.order)
    return filter_menu_tree(result)


def filter_menu_tree(item_list) -> List[MenuTreeVm]:
    """根据fn_filter筛选树"""
    def fn_filter(x):
        return x.enabled and x.selected

    def filter_sub_tree(o, parent_selected=True, parent_enabled=True):
        o.selected = True if parent_selected else o.selected  # 当父节点选中时选中所有
        o.enabled = False if not parent_enabled else o.enabled  # 当父节点禁用时禁用所有
        if o.children:
            child_result = []
            for child in o.children:
                child = filter_sub_tree(child, o.selected, o.enabled)
                if fn_filter(child):
                    child_result.append(child)
            o.children = child_result
        if o.children is not None:
            o.selected = len(o.children) > 0
        return o

    result = []
    for item in item_list:
        item = filter_sub_tree(item, item.selected, item.enabled)
        if fn_filter(item):
            result.append(item)
    return result


def get_all_menu_list() -> List[MenuTreeVm]:
    menu_list = MenuRepository.get_all_menu_for_manager()
    return build_tree(menu_list, order_key=lambda x: x.order)


def create_or_update_menu_item(data: MenuEm, transaction: Transaction, do_update=False) -> str:
    if not do_update:
        return MenuRepository.insert_menu_item(data=data, transaction=transaction)
    else:
        if data.id == data.parent_id:
            raise BusinessError("上级菜单不得为当前菜单！")
        MenuRepository.update_menu_item(data=data, transaction=transaction)
        return data.id


def delete_menu_item(menu_id: str, transaction: Transaction):
    return MenuRepository.delete_menu_item(
        menu_id=menu_id,
        transaction=transaction,
    )


def get_menu_id_list_for_role(role_id: str):
    return DataPermissionRepository.get_detail_object_id_list_by_params({
        "authorized_object_category": "role",
        "authorized_object_id": role_id,
        "permitted_object_category": "menu",
        "permission_category": EnumDataPermissionCategory.allow.name,
    })


def set_menu_id_list_for_role(role_menu_vm: RoleMenuVm, transaction: Transaction):
    data_permission_id = DataPermissionRepository.get_or_create_data_permission(
        data_permission_em=DataPermissionEm(
            authorized_object_category="role",
            authorized_object_id=role_menu_vm.role_id,
            permitted_object_category="menu",
            permission_category=EnumDataPermissionCategory.allow.name,
        ),
        transaction=transaction,
    )

    DataPermissionDetailRepository.update_detail_id_list_of_data_permission(
        data_permission_id=data_permission_id,
        new_object_id_list=set(role_menu_vm.menu_id_list),
        permitted_object_category="menu",
        transaction=transaction,
    )


def get_menu_data_route_list(menu_id: str):
    return DataPermissionRepository.get_detail_object_id_list_by_params({
        "authorized_object_category": "menu",
        "authorized_object_id": menu_id,
        "permitted_object_category": "route",
        "permission_category": EnumDataPermissionCategory.allow.name,
    })


def set_menu_data_route_list(data: MenuDataRouteMapVm, transaction: Transaction):
    """设置菜单所使用的DataRoute"""

    data.route_id_list = filter(lambda x: not is_fake_uuid(x), data.route_id_list)

    data_permission_id = DataPermissionRepository.get_or_create_data_permission(
        data_permission_em=DataPermissionEm(
            authorized_object_category="menu",
            authorized_object_id=data.menu_id,
            permitted_object_category="route",
            permission_category=EnumDataPermissionCategory.allow.name,
        ),
        transaction=transaction,
    )

    DataPermissionDetailRepository.update_detail_id_list_of_data_permission(
        data_permission_id=data_permission_id,
        new_object_id_list=set(data.route_id_list),
        permitted_object_category="route",
        transaction=transaction,
    )


def clear_menu_data_route_list(menu_id: str, transaction: Transaction):
    return delete_data_permission_and_detail(
        authorized_object_category='menu',
        authorized_object_id=menu_id,
        permitted_object_category='route',
        permission_category='allow',
        transaction=transaction,
    )