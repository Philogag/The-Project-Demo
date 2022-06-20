"""
蓝图：权限绑定
"""
import logging

from flask import request
from flask.blueprints import Blueprint

from backend.blueprint import basic_carrier_result, get_current_user_handler
from backend.data.pagination_carrier import PaginationParams
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.view.data_permission_vm import DataPermissionSetVm
from backend.service.data_permission_service import (
    add_data_permission_detail_item_by_model,
    delete_data_permission_item_by_model,
)
from backend.service.master_user_service import get_user_page_by_data_permission
from backend.utility.route_premission_helper import RoutePermissionHelper

data_permission_blueprint = Blueprint(
    name="data_permission",
    import_name=__name__,
    url_prefix="/data-permission",
)
route_permission = RoutePermissionHelper(data_permission_blueprint, group="数据权限")


@data_permission_blueprint.route('/set-data-permission-item', methods=['POST'])
@route_permission.set(name="添加授权")
@basic_carrier_result()
def route_set_data_permission_item():
    data = request.get_json(silent=True)
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action='set-data-permission-item',
        action_params=data,
    ) as uow:
        add_data_permission_detail_item_by_model(
            DataPermissionSetVm(**data),
            transaction=uow.transaction,
        )


@data_permission_blueprint.route('/delete-data-permission-item', methods=['POST'])
@route_permission.set(name="解除授权")
@basic_carrier_result()
def route_delete_data_permission_item():
    data = request.get_json(silent=True)
    with SqlAlchemyUOW(
        handler=get_current_user_handler(),
        action='delete-data-permission-item',
        action_params=data,
    ) as uow:
        delete_data_permission_item_by_model(
            DataPermissionSetVm(**data),
            transaction=uow.transaction,
        )


@data_permission_blueprint.route(
    '/get-permitted-user-page/<string:permitted_object_category>/<string:permitted_object_id>',
    methods=['POST']
)
@route_permission.set(name="授权用户列表")
@basic_carrier_result()
def route_sport_meeting_unbind_user_page(permitted_object_category: str, permitted_object_id: str):
    data = request.get_json(silent=True)
    invert = request.args.get('invert', default='false') == 'true'  # 反选
    return get_user_page_by_data_permission(
        permitted_object_category=permitted_object_category,
        permitted_object_id=permitted_object_id,
        invert=invert,
        params=PaginationParams(**data)
    )
