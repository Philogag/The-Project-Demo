from typing import Iterable, Optional, List

from backend.data.pagination_carrier import PaginationCarrier, PaginationParams
from backend.data.transaction import Transaction
from backend.model.edit.master_user_em import MasterUserEm
from backend.model.entity.master_user_entity import MasterUserEntity
from backend.model.view.master_user_info_vm import MasterUserInfoVm
from backend.model.view.master_user_list_vm import MasterUserListVm
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder


class MasterUserRepository(BasicRepository):

    __entity_cls__ = MasterUserEntity
    __model_cls__ = MasterUserEm

    @staticmethod
    def get_by_id(*, user_id: str) -> Optional[MasterUserEm]:
        return MasterUserRepository._get_model_by_id(
            model_cls=MasterUserEm, entity_cls=MasterUserEntity, model_id=user_id
        )

    @classmethod
    def get_user_info(cls, user_id: str) -> Optional[MasterUserInfoVm]:
        sql = """
        select smu.*, uom.organization_id
        from st_master_user smu
        left join user_organization_map uom on uom.user_id = smu.id
        where smu.id = :user_id
        """
        return cls._fetch_first(
            model_cls=MasterUserInfoVm,
            sql=sql,
            params={"user_id": user_id}
        )

    @staticmethod
    def get_by_params(*, params) -> Optional[MasterUserEm]:
        return MasterUserRepository._get_model_by_params(
            model_cls=MasterUserEm, entity_cls=MasterUserEntity, params=params
        )

    @staticmethod
    def insert_user(*, user_em: MasterUserEm, transaction: Transaction) -> str:
        return MasterUserRepository._insert_entity(
            entity_cls=MasterUserEntity, data=user_em, transaction=transaction
        )

    @staticmethod
    def update_user(
        *, data: MasterUserEm, transaction: Transaction, col_list: Iterable[str] = None
    ) -> Optional[MasterUserEm]:
        return MasterUserRepository._update_entity(
            entity_cls=MasterUserEntity,
            data=data,
            transaction=transaction,
            col_list=col_list,
        )

    @classmethod
    def get_organization_user_list_page(cls, params: PaginationParams) -> PaginationCarrier[MasterUserListVm]:
        sql = """
        select smu.*, 
        smo.id as organization_id, smo.name as organization_name, 
        role.role_list 
        from st_master_user smu
        left join user_organization_map uom on uom.user_id=smu.id
        left join st_master_organization smo on smo.id=uom.organization_id
        left join (
            select urm.user_id, json_agg(json_build_object(
                'id', sr.id,
                'role_name', sr.role_name
            )) as role_list from user_role_map as urm
            left join st_role sr on sr.id = urm.role_id
            group by urm.user_id
        ) as role on role.user_id=smu.id
        order by smu.username asc
        """

        pagination_query = PaginationQueryBuilder(
            result_type=MasterUserListVm,
            sql=sql,
            search_columns=['username'],
            filter_columns=['organization_id'],
            order_columns=params.order_columns if params.order_columns is not None else {},
            params={},
        )
        return pagination_query.get_query_result(
            page_size=params.page_size,
            page_index=params.page_index,
            search_text=params.search_text,
            filter_option=params.filter_columns,
        )

    @classmethod
    def get_user_page_by_data_permission(
            cls,
            permitted_object_category: str,
            permitted_object_id: str,
            params: PaginationParams,
            invert: bool = False
    ) -> PaginationCarrier[MasterUserListVm]:
        """

        :param invert: 是否反选，默认为否
        """
        sql = """
        select smu.*
        , smo.id as organization_id
        , smo.name as organization_name
        , role.role_list 
        , role.role_code_list
        from st_master_user smu
        left join user_organization_map uom on uom.user_id=smu.id
        left join st_master_organization smo on smo.id=uom.organization_id
        left join (
            select urm.user_id, json_agg(json_build_object(
                'id', sr.id,
                'role_name', sr.role_name
            )) as role_list
            , array_agg(sr.code) as role_code_list
            from user_role_map as urm
            left join st_role sr on sr.id = urm.role_id
            group by urm.user_id
        ) as role on role.user_id=smu.id
        left join (
            select sdp.authorized_object_id as user_id
            from st_data_permission_detail sdpd
            inner join st_data_permission sdp on sdpd.data_permission_id = sdp.id
            where sdp.authorized_object_category = 'master_user'
            and sdp.permitted_object_category = :permitted_object_category
            and sdpd.permitted_object_id = :permitted_object_id
            and sdp.permission_category = 'allow'
        ) allowed_object on allowed_object.user_id = smu.id
        where allowed_object.user_id is {invert}
        """.format(invert="null" if invert else "not null")

        search_params = {}
        if params.filter_columns and 'role_code_list' in params.filter_columns.keys():
            sql += " and role_code_list && array[:role_code_list]::varchar[] "
            search_params["role_code_list"] = params.filter_columns["role_code_list"]

        pagination_query = PaginationQueryBuilder(
            result_type=MasterUserListVm,
            sql=sql,
            search_columns=['username'],
            filter_columns=[],
            order_columns={},
            params={
                "permitted_object_category": permitted_object_category,
                "permitted_object_id": permitted_object_id,
                **search_params,
            },
        )
        return pagination_query.get_query_result(
            page_size=params.page_size,
            page_index=params.page_index,
            search_text=params.search_text,
            filter_option=params.filter_columns,
        )

    @classmethod
    def get_team_bind_master_user_by_sport_meeting_id(
        cls,
        sport_meeting_id: str
    ) -> List[MasterUserEm]:
        """获取运动会代表队绑定的所有用户, 用于批量操作"""
        sql = """
        select smu.* 
        from st_master_user smu
        inner join st_data_permission sdp on sdp.authorized_object_category = 'master_user'
            and sdp.authorized_object_id = smu.id
            and sdp.permitted_object_category = 'team'
        inner join st_data_permission_detail sdpd on sdpd.data_permission_id = sdp.id
        inner join st_team st on st.id = sdpd.permitted_object_id
        where st.sport_meeting_id = :sport_meeting_id
        """
        return cls._fetch_all(
            model_cls=MasterUserEm,
            sql=sql,
            params={
                "sport_meeting_id": sport_meeting_id
            }
        )
    
    @classmethod
    def get_organization_guest(
        cls,
        organization_id: str
    ) -> Optional[MasterUserEm]:
        sql = """
        select smu.* 
        from st_master_user smu
        inner join user_organization_map uom 
            on uom.user_id = smu.id
            and uom.organization_id = :organization_id
        inner join user_role_map urm on urm.user_id = smu.id
        inner join st_role sr on sr.id = urm.role_id and sr.code = :role_code
        """

        return cls._fetch_first(
            model_cls=MasterUserEm,
            sql=sql,
            params={
                "organization_id": organization_id,
                "role_code": 'guest',
            }
        )