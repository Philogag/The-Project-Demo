"""
仓库层：权限
"""
from typing import Any, Dict, List, Optional, Union

from backend.data.system_enum import EnumDataPermissionCategory
from backend.data.transaction import Transaction
from backend.model.edit.data_permission_em import DataPermissionEm
from backend.model.entity.data_permission_detail_entity import DataPermissionDetailEntity
from backend.model.entity.data_permission_entity import DataPermissionEntity
from backend.repository.basic_repository import BasicRepository


class DataPermissionRepository(BasicRepository):
    __entity_cls__ = DataPermissionEntity
    __model_cls__ = DataPermissionEm

    @classmethod
    def get_data_permission_by_params(
        cls, params: Dict[str, Any]
    ) -> Optional[DataPermissionEm]:
        return cls._get_model_by_params(
            entity_cls=DataPermissionEntity, model_cls=DataPermissionEm, params=params
        )

    @classmethod
    def get_all_data_permission_by_params(
        cls, params: Dict[str, Any]
    ) -> List[DataPermissionEm]:
        return cls._get_model_list_by_params(
            entity_cls=DataPermissionEntity, model_cls=DataPermissionEm, params=params
        )

    @classmethod
    def create_data_permission(
        cls, data_permission_em: DataPermissionEm, transaction: Transaction
    ) -> Optional[str]:
        return cls._insert_entity(
            entity_cls=DataPermissionEntity,
            data=data_permission_em,
            transaction=transaction,
        )

    @classmethod
    def get_or_create_data_permission(
        cls, data_permission_em: DataPermissionEm, transaction: Transaction
    ) -> str:
        """:return: id of data_permission"""
        exist_dp = cls.get_data_permission_by_params(
            params={
                "authorized_object_category": data_permission_em.authorized_object_category,
                "authorized_object_id": data_permission_em.authorized_object_id,
                "permitted_object_category": data_permission_em.permitted_object_category,
                "permission_category": data_permission_em.permission_category,
            }
        )
        if not exist_dp:
            return cls.create_data_permission(data_permission_em, transaction)
        else:
            return exist_dp.id

    @classmethod
    def get_detail_object_id_list_by_params(cls, params):
        sql = """
        select sdpd.permitted_object_id as id from st_data_permission_detail sdpd
        inner join st_data_permission sdp on sdp.id = sdpd.data_permission_id
        where sdp.authorized_object_category=:authorized_object_category
          and sdp.authorized_object_id=:authorized_object_id
          and sdp.permitted_object_category=:permitted_object_category
          and sdp.permission_category=:permission_category
        """

        data_list = cls._fetch_all_for_dict(
            sql=sql,
            params=params,
        )
        return list(map(lambda x: x["id"], data_list))

    @classmethod
    def delete_data_permission_with_detail(cls, data_permission_id: str, transaction: Transaction):
        cls._delete_entity_by_id(
            entity_cls=DataPermissionEntity,
            entity_id=data_permission_id,
            transaction=transaction,
        )
        cls._delete_entities_by_params(
            entity_cls=DataPermissionDetailEntity,
            params={"data_permission_id": data_permission_id},
            transaction=transaction,
        )

    @classmethod
    def get_user_allowed_team_at_sport_meeting(cls, user_id: str, sport_meeting_id: str) -> List[str]:
        """Return the list of team id"""
        sql = """
        select sdpd.permitted_object_id as id from st_data_permission_detail sdpd
        inner join st_data_permission sdp on sdp.id = sdpd.data_permission_id
        inner join st_team st on st.id = sdpd.permitted_object_id
        where sdp.authorized_object_category=:authorized_object_category
          and sdp.authorized_object_id=:authorized_object_id
          and sdp.permitted_object_category=:permitted_object_category
          and sdp.permission_category=:permission_category
          and st.sport_meeting_id=:sport_meeting_id
        """
        data_list = cls._fetch_all_for_dict(
            sql=sql,
            params={
                'authorized_object_category': 'master_user',
                'authorized_object_id': user_id,
                'permitted_object_category': 'team',
                'permission_category': EnumDataPermissionCategory.allow.name,
                'sport_meeting_id': sport_meeting_id,
            },
        )
        return list(map(lambda x: x["id"], data_list))

    @classmethod
    def check_data_permission_exist(
            cls,
            authorized_object_category: str,
            authorized_object_id: str,
            permitted_object_category: str,
            permitted_object_id: Union[str, List[str]],
            permission_category: str = EnumDataPermissionCategory.allow.name,
    ):
        if isinstance(permitted_object_id, str):
            permitted_object_id = [permitted_object_id]
        sql = """
        select sdpd.permitted_object_id as id from st_data_permission_detail sdpd
        inner join st_data_permission sdp on sdp.id = sdpd.data_permission_id
        where sdp.authorized_object_category=:authorized_object_category
          and sdp.authorized_object_id=:authorized_object_id
          and sdp.permitted_object_category=:permitted_object_category
          and sdp.permission_category=:permission_category
          and sdpd.permitted_object_id=any(array[:permitted_object_id])
        """
        return cls._fetch_count(
            sql=sql,
            params={
                "authorized_object_category": authorized_object_category,
                "authorized_object_id": authorized_object_id,
                "permitted_object_category": permitted_object_category,
                "permitted_object_id": permitted_object_id,
                "permission_category": permission_category,
            }
        ) > 0
