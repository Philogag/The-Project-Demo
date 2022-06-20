"""
路由数据层
"""
import logging
from typing import Any, Dict

from flask import Flask

from backend.blueprint import get_system_init_robot
from backend.data.unit_of_work import SqlAlchemyUOW
from backend.model.edit.route_em import RouteEm
from backend.repository.route_repository import RouteRepository
from backend.utility.route_premission_helper import RoutePermission, RoutePermissionMap


def prepare_route(flask_instance: Flask, default_route_permission: RoutePermission):
    """
    扫描后端路由, 注入权限
    """
    logger = logging.getLogger(__name__)
    logger.debug('Scan data routes.')

    url_map = flask_instance.url_map
    route_permission_map = RoutePermissionMap()
    route_permission_map.set_default_permission(default_route_permission)

    with SqlAlchemyUOW(
        handler=get_system_init_robot(), action="init backend routes", action_params={}
    ) as uow:
        try:
            # 注入路由
            for url in url_map.iter_rules():
                route_em = RouteRepository.get_first_entity_by_params({
                    "route_path": url.rule
                })
                permission = route_permission_map[url.endpoint]
                new_route = RouteEm(
                    route_path=url.rule,
                    group=permission.group,
                    name=permission.name if permission.name else url.endpoint,
                    need_login=permission.login_required,
                    allow_all=permission.allow_all,
                )
                if route_em is None:
                    RouteRepository.create_entity(
                        data=new_route,
                        transaction=uow.transaction,
                    )
                else:
                    new_route.id = route_em.id
                    RouteRepository.update_entity(
                        data=new_route,
                        transaction=uow.transaction,
                        col_list=[
                            "group", "name", "need_login", "allow_all"
                        ]

                    )
        except Exception as error:
            logger.exception(error)


def get_data_route_selection():
    return RouteRepository.get_data_route_selection()


# @redis_cached(expired_seconds=300)
def get_route_permission_map() -> Dict[str, Any]:
    """
    获取角色对应路由权限，使用redis缓存
    """
    result_list = RouteRepository.get_role_route_permissions()
    result = {}
    for route_vm in result_list:
        result[route_vm.route_path] = route_vm.dict()
    return result
