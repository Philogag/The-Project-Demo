import logging
import os
import traceback
from logging.config import fileConfig
from typing import Optional

from flask import Flask, current_app, jsonify, request
from flask_jwt_extended import verify_jwt_in_request
from jwt import InvalidTokenError as NoAuthorizationError

from backend.blueprint import get_current_user_id
from backend.data.basic_carrier import MessageCarrier
from backend.data.system_enum import EnumRoleCode
from backend.service.role_service import get_user_current_role
from backend.service.route_service import get_route_permission_map, prepare_route
from backend.utility.error_helper import NoPermissionError
from backend.utility.route_premission_helper import RoutePermission


def scan_blueprint():
    blueprints = []
    for file in os.listdir("./backend/blueprint"):
        if file.endswith("blueprint.py"):
            module = file[:-3]
            blueprint = getattr(
                __import__("backend.blueprint." + module, fromlist=True), module
            )
            blueprint.append(blueprint)
    return blueprints

def init_error_handler(flask_instance: Flask):
    
    logger = logging.getLogger()

    @flask_instance.errorhandler(404)
    def page_not_found(error):
        logger.exception(error)
        carrier = MessageCarrier()
        carrier.push_exception("Not found.", 404)
        return jsonify(carrier.dict())

    @flask_instance.errorhandler(Exception) # 处理除上述异常以外的所有异常
    def process_error_handler(error: Exception):
        """
        这个handler可以catch住所有的abort(500)和raise exception.
        注入方式：
        app_instance.errorhandler(Exception)(process_error_handler)
        """

        logger.exception(error)
        carrier = MessageCarrier()
        carrier.push_exception(error, 402)
        return jsonify(carrier.dict())


def init_app_process(flask_instance: Flask):
    """
    初始化 app 处理
    :param flask_instance:
    :return:
    """
    try:
        prepare_route(
            flask_instance=flask_instance,
            default_route_permission=RoutePermission(  # 默认允许所有已登录用户访问
                allow_all=False, login_required=True,
            ),
        )
    except Exception as e:
        logging.exception(e)
        logging.error("Prepare route permission failed.")
        return


def init_logger(logger_config_file):
    if not os.path.exists(logger_config_file):
        raise Exception("Can not find logger config file.")
    if not os.path.exists("log"):
        os.mkdir("log")
    fileConfig(logger_config_file)
    logger = logging.getLogger()

    logger.info("Logger init successfully.")


def _check_route_authorization():

    request_url = get_match_route()
    if not request_url:
        return 

    route_permission_map = get_route_permission_map()
    route_permission = route_permission_map[request_url]

    has_authorization = request.headers.get("Authorization")
    if route_permission["need_login"] or has_authorization:
        verify_jwt_in_request()
    if not route_permission["need_login"]:
        return

    if route_permission["allow_all"]:
        return

    current_user_id = get_current_user_id()
    current_role = get_user_current_role(current_user_id)
    if current_role.code == EnumRoleCode.super_admin.name:
        return  # 超级管理员权限
    if current_role and current_role.code in route_permission["role_list"]:
        return  # permit by user's role

    raise NoPermissionError(request_url)  # Do not have any permission.


def process_before_request():
    """
    请求前处理
    :return:
    """
    carrier = MessageCarrier()
    try:
        if request.method in ["OPTIONS"]:
            return
        _check_route_authorization()
    except NoPermissionError as err:
        traceback.print_exc()
        carrier.push_exception(err=err, code=403)
        return jsonify(carrier.dict())
    except NoAuthorizationError as err:
        traceback.print_exc()
        carrier.push_exception(err=err, code=401)
        return jsonify(carrier.dict())
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
        return jsonify(carrier.dict())


def get_match_route() -> Optional[str]:
    """
    获取匹配的路由表达式
    """

    def __match_url(_url_rule):
        """
        检查是否匹配
        :param _url_rule:
        :return:
        """
        if request.url_rule:
            # logging.debug(request.url_rule)
            # 正式环境的context有可能不是从/过来的,需要处理prepare_url
            if request.method in _url_rule.methods and (
                    # (_url_rule.rule == prepare_url(request.url_rule.rule))
                    # or (_url_rule.rule == request.url_rule.rule)
                    _url_rule.rule == request.url_rule.rule
            ):
                return True
        return False

    app_url_map_rules = list(current_app.url_map.iter_rules())
    matched_rules = [
        app_url_rule
        for app_url_rule in app_url_map_rules
        if __match_url(app_url_rule)
    ]
    # 对于url_rule不区分methods，所以处理第一个即可
    return matched_rules[0].rule if len(matched_rules) > 0 else None
