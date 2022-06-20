from typing import List, Optional

from backend.data.transaction import Transaction
from backend.model.edit.role_em import RoleEm
from backend.model.entity.role_entity import RoleEntity
from backend.repository.basic_repository import BasicRepository


class RoleRepository(BasicRepository):
    @classmethod
    def get_role_by_id(cls, role_id) -> Optional[RoleEm]:
        return RoleRepository._get_model_by_id(
            entity_cls=RoleEntity, model_cls=RoleEm, model_id=role_id
        )

    @classmethod
    def get_role_by_code(cls, code) -> Optional[RoleEm]:
        return RoleRepository._get_model_by_params(
            entity_cls=RoleEntity, model_cls=RoleEm, params={"code": code}
        )

    @classmethod
    def create_role(cls, role_em: RoleEm, transaction: Transaction) -> Optional[str]:
        return RoleRepository._insert_entity(
            entity_cls=RoleEntity, data=role_em, transaction=transaction
        )

    @classmethod
    def get_all_role(cls) -> List[RoleEm]:
        return cls._fetch_all(
            sql="SELECT * FROM st_role order by handled_at asc", model_cls=RoleEm, params={}
        )

    @classmethod
    def update_menu_item(cls, data: RoleEm, transaction: Transaction, col_list: List[str] = None):
        return cls._update_entity(
            entity_cls=RoleEntity,
            data=data,
            transaction=transaction,
            col_list=col_list,
        )

    @classmethod
    def delete_role_by_id(cls, role_id: str, transaction: Transaction):
        return cls._delete_entity_by_id(entity_cls=RoleEntity, transaction=transaction, entity_id=role_id)

