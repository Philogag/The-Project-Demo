from flask import Blueprint

from backend.blueprint import basic_carrier_result
from backend.service.route_service import get_data_route_selection
from backend.utility.route_premission_helper import RoutePermissionHelper

route_blueprint = Blueprint(
    name="route",
    import_name=__name__,
    url_prefix="/route"
)
route_permission = RoutePermissionHelper(route_blueprint, group="数据权限")


@route_blueprint.route("/get-selection", methods=["GET", ])
@route_permission.set(name="获取选项列表")
@basic_carrier_result()
def route_get_data_route_selection():
    return get_data_route_selection()
