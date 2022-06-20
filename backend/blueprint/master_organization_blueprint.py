import logging

from flask import Blueprint, request

from backend.blueprint import (
    get_current_user_handler,
    basic_carrier_result,
)
from backend.data.pagination_carrier import PaginationParams
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.master_organization_em import MasterOrganizationEm
from backend.service.master_organization_service import (
    get_organization_list_for_management,
    create_or_update_master_organization,
    delete_organization_by_id,
    get_organization_selection,
    get_guest_login_organization_selection,
)
from backend.utility.route_premission_helper import RoutePermissionHelper

master_organization_blueprint = Blueprint(
    name="master_organization",
    import_name=__name__,
    url_prefix="/organization",
)
route_permission = RoutePermissionHelper(master_organization_blueprint, group="组织管理")


@master_organization_blueprint.route('/get-organization-management-list', methods=['POST'])
@route_permission.set(name="获取列表")
@basic_carrier_result()
def route_get_list_for_management():
    data = request.get_json(silent=True)
    return get_organization_list_for_management(
        params=PaginationParams(**data)
    )


@master_organization_blueprint.route('/create-or-update', methods=['POST'])
@route_permission.set(name="编辑组织")
@basic_carrier_result()
def route_create_or_update_organization():
    data = request.get_json(silent=True)
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="create-or-update-organization",
        action_params=data,
    ) as uow:
        return create_or_update_master_organization(
            data=MasterOrganizationEm(**data),
            transaction=uow.transaction,
        )


@master_organization_blueprint.route('/delete/<string:org_id>', methods=['GET'])
@route_permission.set(name="删除组织")
@basic_carrier_result()
def route_delete_organization(org_id: str):
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action="delete-organization",
        action_params={"id": org_id},
    ) as uow:
        return delete_organization_by_id(
            organization_id=org_id,
            transaction=uow.transaction,
        )


@master_organization_blueprint.route('/get-selection', methods=['POST'])
@route_permission.set(name="获取选项列表")
@basic_carrier_result()
def route_get_organization_selection():
    params = request.get_json(silent=True)
    return get_organization_selection(params)


@master_organization_blueprint.route('/guest-login-selection', methods=['GET'])
@route_permission.set(name="访客登录组织选项列表", login_required=False, allow_all=True)
@basic_carrier_result()
def route_get_guest_login_organization_selection():
    return get_guest_login_organization_selection()
