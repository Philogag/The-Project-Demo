"""
蓝图：用户管理
"""
import logging

from flask import Blueprint, jsonify, request

from backend.blueprint import get_current_user_handler, get_current_user_id
from backend.data.basic_carrier import BasicCarrier
from backend.data.pagination_carrier import PaginationParams
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.master_user_em import MasterUserManageEm
from backend.service.master_user_service import (
    create_or_update_master_user,
    delete_master_user,
    get_user_info,
    get_user_list_for_management,
)
from backend.utility.error_helper import BusinessError
from backend.utility.route_premission_helper import RoutePermissionHelper

master_user_blueprint = Blueprint(
    name="master_user",
    import_name=__name__,
    url_prefix="/master-user"
)
route_permission = RoutePermissionHelper(master_user_blueprint, group="用户管理")


@master_user_blueprint.route("/get-current-user-info", methods=["GET"])
@route_permission.set(login_required=True, allow_all=True, name="当前用户信息")
def route_get_current_user_info():
    carrier = BasicCarrier()
    try:
        carrier.result = get_user_info(
            user_id=get_current_user_id()
        )
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict(to_camel=True))


@master_user_blueprint.route("/get-master-user-management-list", methods=["POST"])
@route_permission.set(name="用户管理列表")
def route_get_user_list_for_management():
    carrier = BasicCarrier()
    try:
        data = request.get_json(silent=True)
        carrier.result = get_user_list_for_management(
            params=PaginationParams(**data)
        )
    except BusinessError as err:
        logging.exception(err)
        carrier.push_exception(err)
    return jsonify(carrier.to_dict(to_camel=True))


@master_user_blueprint.route('/create-or-update', methods=['POST'])
@route_permission.set(name="编辑用户")
def route_create_or_update_master_user():
    carrier = BasicCarrier()
    try:
        data = request.get_json(silent=True)
        with SqlAlchemyUOW(
            handler=get_current_user_handler(),
            action="create-or-update-master-user",
            action_params=data,
        ) as uow:
            carrier.result = create_or_update_master_user(
                data=MasterUserManageEm(**data),
                transaction=uow.transaction,
            )
    except BusinessError as e:
        logging.exception(e)
        carrier.push_exception(e)
    return jsonify(carrier.to_dict())


@master_user_blueprint.route('/delete/<string:user_id>', methods=['POST'])
@route_permission.set(name="删除用户")
def route_delete_organization(user_id: str):
    carrier = BasicCarrier()
    try:
        with SqlAlchemyUOW(
            handler=get_current_user_handler(),
            action="delete-master-user",
            action_params={"id": user_id},
        ) as uow:
            carrier.result = delete_master_user(
                user_id=user_id,
                transaction=uow.transaction,
            )
    except BusinessError as e:
        logging.exception(e)
        carrier.push_exception(e)
    return jsonify(carrier.to_dict())
