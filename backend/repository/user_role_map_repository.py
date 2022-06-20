from typing import List

from backend.data.transaction import Transaction
from backend.model.edit.role_em import RoleEm
from backend.model.edit.user_role_map_em import UserRoleMapEm
from backend.model.entity.user_role_map_entity import UserRoleMapEntity
from backend.repository.basic_repository import BasicRepository


class UserRoleMapRepository(BasicRepository):
    __entity_cls__ = UserRoleMapEntity
    __model_cls__ = UserRoleMapEm

    @classmethod
    def get_user_current_role_by_user_id(cls, user_id: str) -> RoleEm:
        sql = """
        select sr.* from st_role sr
        inner join user_role_map urm on urm.role_id = sr.id
        inner join st_master_user smu on smu.id = urm.user_id
        where smu.id = :user_id
        order by last_enabled_time is null asc, urm.last_enabled_time desc 
        """
        return cls._fetch_first(
            model_cls=RoleEm,
            sql=sql,
            params={
                "user_id": user_id
            }
        )

    @classmethod
    def check_user_in_role(cls, user_id: str, role_id: str) -> bool:
        return cls._check_entity_existed(
            entity_cls=UserRoleMapEntity,
            params={
                "user_id": user_id,
                "role_id": role_id,
            }
        )

    @classmethod
    def fetch_roles_by_user_id(cls, user_id: str) -> List[RoleEm]:
        sql = """
        select sr.* from user_role_map urm
        inner join st_role sr on urm.role_id=sr.id
        where urm.user_id = :user_id
        """
        return cls._fetch_all(
            model_cls=RoleEm,
            sql=sql,
            params={
                "user_id": user_id,
            }
        )

    @classmethod
    def del_user_role_map(cls, user_id: str, role_id: str, transaction: Transaction):
        return cls._delete_entities_by_params(
            entity_cls=UserRoleMapEntity,
            params={"user_id": user_id, "role_id": role_id},
            transaction=transaction,
        )

    @classmethod
    def add_user_role_map(cls, user_id: str, role_id: str, transaction: Transaction):
        return cls._insert_entity(
            entity_cls=UserRoleMapEntity,
            data=UserRoleMapEm(
                user_id=user_id,
                role_id=role_id,
            ),
            transaction=transaction,
        )
