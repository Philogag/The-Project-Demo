from typing import List

from backend.model.basic_selection_vm import BasicTreeSelectionVm
from backend.model.edit.route_em import RouteEm
from backend.model.entity.route_entity import RouteEntity
from backend.model.view.route_permission_vm import RoutePermissionVm
from backend.repository.basic_repository import BasicRepository


class RouteRepository(BasicRepository):

    __entity_cls__ = RouteEntity
    __model_cls__ = RouteEm

    @classmethod
    def get_data_route_selection(cls) -> List[BasicTreeSelectionVm]:
        sql = """
        select sr.group as label, sr.group as value,
        json_agg(json_build_object(
            'label', sr.name,
            'value', sr.id
        )) as children
        from (
            select sr.* from st_route sr
            where sr.allow_all=false and sr.need_login=true
            order by sr.name asc
        ) sr
        group by sr.group
        """
        return cls._fetch_all(
            model_cls=BasicTreeSelectionVm,
            sql=sql,
            params={},
        )

    @classmethod
    def get_role_route_permissions(cls) -> List[RoutePermissionVm]:
        sql = """
        select sr.route_path, sr.need_login, sr.allow_all, 
        array_agg(menu_route_map.menu_code) as menu_list, 
        array_agg(role_menu_map.role_code) as role_list
        from st_route sr
        left join (
            select st_menu.id as menu_id, st_menu.name as menu_code, sdpd_menu_route.permitted_object_id as route_id
            from st_data_permission_detail sdpd_menu_route
            inner join st_data_permission sdp_menu_route 
                on sdp_menu_route.id=sdpd_menu_route.data_permission_id
                and sdp_menu_route.authorized_object_category='menu'
                and sdp_menu_route.permitted_object_category='route'
                and sdp_menu_route.permission_category='allow'
            inner join st_menu on st_menu.id=sdp_menu_route.authorized_object_id
        ) menu_route_map on menu_route_map.route_id=sr.id
        left join (
            select st_role.id as role_id, st_role.code as role_code, sdpd_role_menu.permitted_object_id as menu_id
            from st_data_permission_detail sdpd_role_menu
            inner join st_data_permission sdp_role_menu 
                on sdp_role_menu.id=sdpd_role_menu.data_permission_id
                and sdp_role_menu.authorized_object_category='role'
                and sdp_role_menu.permitted_object_category='menu'
                and sdp_role_menu.permission_category='allow'
            inner join st_role on st_role.id=sdp_role_menu.authorized_object_id
        ) role_menu_map on role_menu_map.menu_id=menu_route_map.menu_id
        group by sr.id
        """

        return cls._fetch_all(
            model_cls=RoutePermissionVm,
            sql=sql,
            params={},
        )
