from flask import Blueprint, request

from backend.blueprint import basic_carrier_result, get_current_user_handler, get_current_user_id
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.role_em import RoleEm
from backend.service.role_service import (
    create_or_update_role_item,
    delete_role_item_by_id,
    get_role_list_for_management,
    set_user_current_role,
)
from backend.utility.route_premission_helper import RoutePermissionHelper

role_blueprint = Blueprint(
    name="role",
    import_name=__name__,
    url_prefix="/role"
)
route_permission = RoutePermissionHelper(role_blueprint, group="角色管理")


@role_blueprint.route("/switch-current-role/<string:role_id>", methods=["GET"])
@route_permission.set(name="切换角色", allow_all=True)
@basic_carrier_result()
def route_switch_current_role(role_id):
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="switch-current-role",
        action_params={"id": role_id}
    ) as uow:
        return set_user_current_role(
            user_id=get_current_user_id(),
            role_id=role_id,
            transaction=uow.transaction
        )


@role_blueprint.route("/get-role-management-list", methods=["GET"])
@route_permission.set(name="角色管理列表")
@basic_carrier_result()
def route_get_role_management_list():
    return get_role_list_for_management()


@role_blueprint.route("/create-or-update", methods=["POST"])
@route_permission.set(name="编辑角色")
@basic_carrier_result()
def route_create_or_update_role_item():
    data = request.get_json(silent=True)
    with SqlAlchemyUOW(
            handler=get_current_user_handler(),
            action="create-or-update-role-item",
            action_params=data,
    ) as uow:
        role_em = RoleEm(**data, editable=True)
        return create_or_update_role_item(
            data=role_em,
            transaction=uow.transaction,
            do_update=(role_em.id is not None)
        )


@role_blueprint.route("/delete/<string:role_id>", methods=["GET"])
@route_permission.set(name="删除角色")
@basic_carrier_result()
def route_delete_role_item(role_id: str):
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="delete-role-item",
        action_params=role_id,
    ) as uow:
        return delete_role_item_by_id(
            role_id,
            transaction=uow.transaction,
        )
