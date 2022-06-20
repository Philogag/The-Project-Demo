from flask import Blueprint

from backend.blueprint import basic_carrier_result
from backend.service.enum_service import get_enum_class_by_underline_name
from backend.utility.enum_helper import enum_to_tuple, enum_to_dict, enum_to_selection
from backend.utility.error_helper import BusinessError
from backend.utility.route_premission_helper import RoutePermissionHelper

enum_blueprint = Blueprint(
    name="enum",
    import_name=__name__,
    url_prefix="/enum",
)
route_permission = RoutePermissionHelper(enum_blueprint, group="枚举")


@enum_blueprint.route("/<string:result_type>/<string:enum_name>", methods=["GET"])
@route_permission.set(name="获取枚举", allow_all=True)
@basic_carrier_result()
def route_get_enum_tuple(result_type, enum_name):
    """
    :param result_type: 'tuple'|'dict'|'selection'
    :param enum_name: role_code for EnumRoleCode
    """
    result_type_transform = {
        "tuple": enum_to_tuple,
        "dict": enum_to_dict,
        "selection": enum_to_selection,
    }
    if result_type not in result_type_transform.keys():
        raise BusinessError("不支持的返回类型 {0}.".format(result_type))
    return result_type_transform[result_type](get_enum_class_by_underline_name(enum_name))
