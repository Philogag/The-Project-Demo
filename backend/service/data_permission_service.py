from typing import Iterable, List, Union

from backend.data.system_enum import EnumDataPermissionCategory
from backend.data.transaction import Transaction
from backend.model.edit.data_permission_detail_em import DataPermissionDetailEm
from backend.model.edit.data_permission_em import DataPermissionEm
from backend.model.view.data_permission_vm import DataPermissionSetVm
from backend.repository.data_permission_detail_repository import DataPermissionDetailRepository
from backend.repository.data_permission_repository import DataPermissionRepository


def set_data_permission(
    authorized_object_category: str,
    authorized_object_id: str,
    permitted_object_category: str,
    transaction: Transaction,
    permission_category: str = EnumDataPermissionCategory.allow.name,
    new_permitted_object_id_list: Iterable[str] = None,
):
    """
    创建或更新数据权限，将 new_permitted_object_id_list 授权给 authorized_object_id

    :param authorized_object_category: 被授权项目类型
    :param authorized_object_id: 被授权项目ID
    :param permitted_object_category: 授权项目类型
    :param permission_category: 授权类型 EnumDataPermissionCategory
    :param new_permitted_object_id_list: 授权项目ID列表
    :param transaction: 操作信息
    """
    data_permission_id = DataPermissionRepository.get_or_create_data_permission(
        data_permission_em=DataPermissionEm(
            authorized_object_category=authorized_object_category,
            authorized_object_id=authorized_object_id,
            permitted_object_category=permitted_object_category,
            permission_category=permission_category,
        ),
        transaction=transaction
    )
    DataPermissionDetailRepository.update_detail_id_list_of_data_permission(
        data_permission_id=data_permission_id,
        new_object_id_list=new_permitted_object_id_list if new_permitted_object_id_list is not None else [],
        permitted_object_category=permitted_object_category,
        transaction=transaction,
    )


def delete_data_permission_and_detail(
    authorized_object_category: str,
    authorized_object_id: str,
    permitted_object_category: str,
    permission_category: str,
    transaction: Transaction,
):
    """
    删除 authorized_object_id 所拥有的 对 permitted_object_category 的权限

    :param authorized_object_category: 被授权项目类型
    :param authorized_object_id: 被授权项目ID
    :param permitted_object_category: 授权项目类型
    :param permission_category: 授权类型 EnumDataPermissionCategory
    :param transaction: 操作信息
    """
    data_permission = DataPermissionRepository.get_first_entity_by_params({
        "authorized_object_category": authorized_object_category,
        "authorized_object_id": authorized_object_id,
        "permitted_object_category": permitted_object_category,
        "permission_category": permission_category,
    })
    if data_permission is not None:
        DataPermissionRepository.delete_data_permission_with_detail(data_permission.id, transaction=transaction)


def delete_data_permission_to_object(
    permitted_object_category: str,
    permitted_object_id: str,
    transaction: Transaction,
):
    """删除所有对于 permitted_object 的权限，如 all master_user of team"""
    data_permission_details = DataPermissionDetailRepository.get_all_entity_by_params(
        permitted_object_category=permitted_object_category,
        permitted_object_id=permitted_object_id,
    )
    for detail in data_permission_details:
        DataPermissionDetailRepository.delete_detail_by_id(detail.id, transaction)


def add_data_permission_detail(
        authorized_object_category: str,
        authorized_object_id: str,
        permitted_object_category: str,
        permitted_object_id: Union[str, List[str]],
        permission_category: str = EnumDataPermissionCategory.allow.name,
        transaction: Transaction = None,
):
    data_permission_id = DataPermissionRepository.get_or_create_data_permission(
        DataPermissionEm(
            authorized_object_category=authorized_object_category,
            authorized_object_id=authorized_object_id,
            permitted_object_category=permitted_object_category,
            permission_category=permission_category,
        ),
        transaction=transaction,
    )
    if not DataPermissionDetailRepository.check_entity_exist(
        data_permission_id=data_permission_id,
        permitted_object_category=permitted_object_category,
        permitted_object_id=permitted_object_id,
    ):
        if isinstance(permitted_object_id, list):
            for object_id in permitted_object_id:
                DataPermissionDetailRepository.insert_detail(
                    DataPermissionDetailEm(
                        data_permission_id=data_permission_id,
                        permitted_object_category=permitted_object_category,
                        permitted_object_id=object_id,
                    ),
                    transaction=transaction,
                )
        else:
            DataPermissionDetailRepository.insert_detail(
                DataPermissionDetailEm(
                    data_permission_id=data_permission_id,
                    permitted_object_category=permitted_object_category,
                    permitted_object_id=permitted_object_id,
                ),
                transaction=transaction,
            )


def delete_data_permission_detail(
        authorized_object_category: str,
        authorized_object_id: str,
        permitted_object_category: str,
        permitted_object_id: Union[str, List[str]],
        permission_category: str = EnumDataPermissionCategory.allow.name,
        transaction: Transaction = None,
):
    data_permission_id = DataPermissionRepository.get_or_create_data_permission(
        DataPermissionEm(
            authorized_object_category=authorized_object_category,
            authorized_object_id=authorized_object_id,
            permitted_object_category=permitted_object_category,
            permission_category=permission_category,
        ),
        transaction=transaction,
    )

    if isinstance(permitted_object_id, str):
        permitted_object_id = [permitted_object_id]

    data_permission_details = DataPermissionDetailRepository.get_all_entity_by_params(
        data_permission_id=data_permission_id,
        permitted_object_category=permitted_object_category,
        permitted_object_id=permitted_object_id,
    )

    for d in data_permission_details:
        DataPermissionDetailRepository.delete_entity_by_id(
            d.id,
            transaction=transaction,
        )


def check_data_permission_exist(
        authorized_object_category: str,
        authorized_object_id: str,
        permitted_object_category: str,
        permitted_object_id: Union[str, List[str]],
        permission_category: str = EnumDataPermissionCategory.allow.name,
):
    return DataPermissionRepository.check_data_permission_exist(
        authorized_object_category=authorized_object_category,
        authorized_object_id=authorized_object_id,
        permitted_object_category=permitted_object_category,
        permitted_object_id=permitted_object_id,
        permission_category=permission_category,
    )


def add_data_permission_detail_item_by_model(
        data: DataPermissionSetVm,
        transaction: Transaction,
):
    return add_data_permission_detail(
        **data.dict(),
        transaction=transaction,
    )


def delete_data_permission_item_by_model(
        data: DataPermissionSetVm,
        transaction: Transaction,
):
    return delete_data_permission_detail(
        **data.dict(),
        transaction=transaction,
    )
