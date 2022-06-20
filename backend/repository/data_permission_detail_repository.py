"""
仓库层：权限详情
"""
from typing import Iterable, List

from backend.data.transaction import Transaction
from backend.model.edit.data_permission_detail_em import DataPermissionDetailEm
from backend.model.entity.data_permission_detail_entity import DataPermissionDetailEntity
from backend.repository.basic_repository import BasicRepository


class DataPermissionDetailRepository(BasicRepository):
    __entity_cls__ = DataPermissionDetailEntity
    __model_cls__ = DataPermissionDetailEm

    @classmethod
    def get_details_by_data_permission_id(cls, data_permission_id) -> List[DataPermissionDetailEm]:
        return cls._fetch_all(
            sql="select * from st_data_permission_detail where data_permission_id=:data_permission_id",
            model_cls=DataPermissionDetailEm,
            params={
                "data_permission_id": data_permission_id,
            }
        )

    @classmethod
    def insert_detail(cls, data: DataPermissionDetailEm, transaction: Transaction) -> str:
        return cls._insert_entity(
            entity_cls=DataPermissionDetailEntity,
            data=data,
            transaction=transaction,
        )

    @classmethod
    def delete_detail_by_id(cls, detail_id: str, transaction: Transaction) -> None:
        cls._delete_entity_by_id(
            entity_cls=DataPermissionDetailEntity,
            entity_id=detail_id,
            transaction=transaction,
        )

    @classmethod
    def update_detail_id_list_of_data_permission(
        cls, data_permission_id, new_object_id_list: Iterable[str], permitted_object_category: str, transaction: Transaction
    ):
        """更新指定data_permission所授权的object列表"""
        exist_object_id_set = set(map(
            lambda x: x.permitted_object_id,
            cls.get_details_by_data_permission_id(data_permission_id)
        ))
        new_object_id_set = set(new_object_id_list)
        need_add_object_id = new_object_id_set - exist_object_id_set
        need_del_object_id = exist_object_id_set - new_object_id_set

        for object_id in need_add_object_id:
            cls.insert_detail(data=DataPermissionDetailEm(
                data_permission_id=data_permission_id,
                permitted_object_category=permitted_object_category,
                permitted_object_id=object_id,
            ), transaction=transaction)
        for object_id in need_del_object_id:
            cls._delete_entity_by_params(
                entity_cls=DataPermissionDetailEntity,
                params={
                    "data_permission_id": data_permission_id,
                    "permitted_object_category": permitted_object_category,
                    "permitted_object_id": object_id,
                },
                transaction=transaction,
            )
