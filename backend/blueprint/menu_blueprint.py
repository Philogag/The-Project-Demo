"""
蓝图层：菜单
"""
import logging

from flask import Blueprint, jsonify, request

from backend.blueprint import basic_carrier_result, get_current_user_handler
from backend.data.basic_carrier import BasicCarrier
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.menu_em import MenuEm
from backend.model.view.menu_data_route_map_vm import MenuDataRouteMapVm
from backend.model.view.role_menu_vm import RoleMenuVm
from backend.service.menu_service import (
    clear_menu_data_route_list,
    create_or_update_menu_item,
    delete_menu_item,
    get_all_menu_list,
    get_current_menu_by_user,
    get_menu_data_route_list,
    get_menu_id_list_for_role,
    set_menu_data_route_list,
    set_menu_id_list_for_role,
)
from backend.utility.error_helper import BusinessError
from backend.utility.route_premission_helper import RoutePermissionHelper

menu_blueprint = Blueprint(
    name="menu",
    import_name=__name__,
    url_prefix="/menu"
)
route_permission = RoutePermissionHelper(menu_blueprint, group="菜单管理")
logger = logging.getLogger(__name__)


@menu_blueprint.route("/get-menu-list", methods=["GET"])
@route_permission.set(allow_all=True, name="获取当前用户菜单")
def route_get_menu_list():
    carrier = BasicCarrier()
    try:
        carrier.result = get_current_menu_by_user()
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/get-menu-management-list", methods=["GET"])
@route_permission.set(name="菜单管理列表")
def route_get_menu_management_list():
    carrier = BasicCarrier()
    try:
        # query = request.get_json(silent=True)
        carrier.result = get_all_menu_list()
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/create-or-update", methods=["POST"])
@route_permission.set(name="编辑菜单")
def route_create_or_update_menu_item():
    carrier = BasicCarrier()
    try:
        data = request.get_json(silent=True)
        with SqlAlchemyUOW(
            handler=get_current_user_handler(),
            action="create_or_update_menu_item",
            action_params=data,
        ) as uow:
            menu_item = MenuEm(**data)
            carrier.result = create_or_update_menu_item(
                data=menu_item,
                transaction=uow.transaction,
                do_update=(menu_item.id is not None)
            )
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/delete/<string:menu_id>", methods=["GET"])
@route_permission.set(name="删除菜单")
def route_delete_menu_item(menu_id: str):
    carrier = BasicCarrier()
    try:
        with SqlAlchemyUOW(
                handler=get_current_user_handler(),
                action="delete_menu_item",
                action_params={"menu_entity_id": menu_id},
        ) as uow:
            carrier.result = delete_menu_item(
                menu_id=menu_id,
                transaction=uow.transaction,
            )
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/get-role-menu-id-list/<string:role_id>", methods=["GET"])
@route_permission.set(name="角色菜单-读取")
def route_get_role_menu_id_list(role_id: str):
    carrier = BasicCarrier()
    try:
        carrier.result = get_menu_id_list_for_role(role_id)
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/set-role-menu-id-list", methods=["POST"])
@route_permission.set(name="角色菜单-更新")
def route_set_role_menu_id_list():
    carrier = BasicCarrier()
    try:
        data = request.get_json(silent=True)
        with SqlAlchemyUOW(
            handler=get_current_user_handler(),
            action="set-role-menu-id-list",
            action_params=data,
        ) as uow:
            carrier.result = set_menu_id_list_for_role(
                role_menu_vm=RoleMenuVm(**data),
                transaction=uow.transaction,
            )
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/get-menu-data-route-list/<string:menu_id>", methods=["GET"])
@route_permission.set(name="数据权限-读取")
def route_get_data_route_list(menu_id: str):
    carrier = BasicCarrier()
    try:
        carrier.result = get_menu_data_route_list(menu_id)
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/set-menu-data-route-list", methods=["POST"])
@route_permission.set(name="数据权限-更新")
def route_set_data_route_list():
    """
    设置菜单项所使用的数据路由，
    当菜单授权给角色或用户后，从中校验权限
    """
    carrier = BasicCarrier()
    try:
        data = request.get_json(silent=True)
        with SqlAlchemyUOW(
            handler=get_current_user_handler(),
            action="set-menu-data-route-list",
            action_params=data,
        ) as uow:
            carrier.result = set_menu_data_route_list(
                data=MenuDataRouteMapVm(**data),
                transaction=uow.transaction,
            )
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict())


@menu_blueprint.route("/clear-menu-data-route-list/<string:menu_id>", methods=["GET"])
@route_permission.set(name="数据权限-清除")
@basic_carrier_result()
def route_clear_data_route_list(menu_id: str):
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="clear-menu-data-route-list",
        action_params={"menu_id": menu_id},
    ) as uow:
        return clear_menu_data_route_list(
            menu_id=menu_id,
            transaction=uow.transaction,
        )