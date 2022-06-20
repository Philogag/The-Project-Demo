from typing import Iterable, List

from backend.data.transaction import Transaction
from backend.model.edit.menu_em import MenuEm
from backend.model.entity.menu_entity import MenuEntity
from backend.model.view.menu_tree_vm import MenuTreeVm
from backend.repository.basic_repository import BasicRepository


class MenuRepository(BasicRepository):

    @classmethod
    def get_current_menu(cls, current_user_id: str, current_role_id: str) -> List[MenuTreeVm]:
        """根据用户id和用户当前role生成菜单"""
        sql = """
        with menu_tree as (
            select parent.*, childs.childrens as child_id_list from st_menu parent
            left join (
                select parent_id, array_agg(id) as childrens from st_menu 
                where parent_id is not NULL 
                group by parent_id
            ) as childs on childs.parent_id = parent.id
        )
        select menu_tree.*, rp.menu_id is not null as selected from menu_tree
        left join (
            select sdpd.permitted_object_id as menu_id
            from st_data_permission_detail sdpd
            inner join st_data_permission sdp on sdp.id = sdpd.data_permission_id
            where (
                sdp.authorized_object_category = 'role'
                and sdp.permitted_object_category = 'menu'
                and sdp.permission_category = 'allow'
                and sdp.authorized_object_id = :current_role_id
            ) or (
                sdp.authorized_object_category = 'master_user'
                and sdp.permitted_object_category = 'menu'
                and sdp.permission_category = 'allow'
                and sdp.authorized_object_id = :current_user_id
            )
        ) as rp on menu_tree.id = rp.menu_id
        where menu_tree.enabled
        order by menu_tree.order asc
        """

        return cls._fetch_all(
            model_cls=MenuTreeVm,
            sql=sql,
            params={
                "current_user_id": current_user_id,
                "current_role_id": current_role_id,
            }
        )

    @classmethod
    def get_all_menu_for_manager(cls):
        """获取所有菜单配置以供管理员配置"""
        sql = """
        with menu_tree as (
            select parent.*, childs.childrens as child_id_list from st_menu parent
            left join (
                select parent_id, array_agg(id) as childrens from st_menu 
                where parent_id is not NULL 
                group by parent_id
            ) as childs on childs.parent_id = parent.id
        ), menu_route_cnt as (
            select sdp.authorized_object_id as menu_id, count(sdpd.permitted_object_id) as route_count
            from st_data_permission_detail sdpd
            inner join st_data_permission sdp 
                on sdp.id=sdpd.data_permission_id
                and sdp.authorized_object_category='menu'
                and sdp.permitted_object_category='route'
                and sdp.permission_category='allow'
            group by sdp.authorized_object_id
        )
        select menu_tree.*, menu_route_cnt.route_count from menu_tree
        left join menu_route_cnt on menu_route_cnt.menu_id=menu_tree.id
        order by menu_tree.order asc
        """
        return cls._fetch_all(
            model_cls=MenuTreeVm,
            sql=sql,
            params={},
        )

    @classmethod
    def insert_menu_item(cls, data: MenuEm, transaction: Transaction) -> str:
        """
        :return: id of data.
        """
        return cls._insert_entity(
            entity_cls=MenuEntity,
            data=data,
            transaction=transaction,
        )

    @classmethod
    def update_menu_item(cls, data: MenuEm, transaction: Transaction, col_list: Iterable[str] = None) -> None:
        return cls._update_entity(
            entity_cls=MenuEntity,
            data=data,
            transaction=transaction,
            col_list=col_list,
        )

    @classmethod
    def delete_menu_item(cls, menu_id: str, transaction: Transaction) -> str:
        cls._delete_entity_by_id(
            entity_cls=MenuEntity,
            entity_id=menu_id,
            transaction=transaction,
        )
        return menu_id

    @classmethod
    def get_child_menu(cls, menu_name: str, current_user_id: str, current_role_id: str) -> List[MenuTreeVm]:
        sql = """
        with RECURSIVE menu_tree as (
            select root.*
            from st_menu root where root.parent_id is null and root.name=:menu_name
            union all
            select son.*
            from st_menu son, menu_tree where son.parent_id=menu_tree.id
        )
        select menu_tree.*, rp.menu_id is not null as selected, childs.child_id_list
        from menu_tree
        left join (
            select parent_id, array_agg(id) as child_id_list from st_menu 
            where parent_id is not NULL 
            group by parent_id
        ) childs on childs.parent_id = menu_tree.id
        left join (
            select sdpd.permitted_object_id as menu_id
            from st_data_permission_detail sdpd
            inner join st_data_permission sdp on sdp.id = sdpd.data_permission_id
            where (
                sdp.authorized_object_category = 'role'
                and sdp.permitted_object_category = 'menu'
                and sdp.permission_category = 'allow'
                and sdp.authorized_object_id = :current_role_id
            ) or (
                sdp.authorized_object_category = 'master_user'
                and sdp.permitted_object_category = 'menu'
                and sdp.permission_category = 'allow'
                and sdp.authorized_object_id = :current_user_id
            )
        ) rp on menu_tree.id = rp.menu_id
        """
        return cls._fetch_all(
            model_cls=MenuTreeVm,
            sql=sql,
            params={
                "menu_name": menu_name,
                "current_user_id": current_user_id,
                "current_role_id": current_role_id,
            }
        )
