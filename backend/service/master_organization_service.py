from typing import List

from backend.data.pagination_carrier import PaginationCarrier, PaginationParams
from backend.data.transaction import Transaction
from backend.model.basic_selection_vm import BasicSelectionVm
from backend.model.edit.master_organization_em import MasterOrganizationEm
from backend.model.edit.user_organization_map_em import UserOrganizationMapEm
from backend.model.view.master_organization_vm import MasterOrganizationListItemVm
from backend.repository.master_organizaion_repository import MasterOrganizationRepository
from backend.repository.user_organization_map_repository import UserOrganizationMapRepository
from backend.utility.string_helper import is_fake_uuid


def get_user_organization_id(user_id):
    em = UserOrganizationMapRepository.get_first_entity_by_params(params={
        "user_id": user_id
    })
    if em is not None:
        return em.organization_id
    else:
        return None
        # raise BusinessError("找不到用户所属组织")


def get_organization_list_for_management(params: PaginationParams) -> PaginationCarrier[MasterOrganizationListItemVm]:
    return MasterOrganizationRepository.get_organization_list_page(params=params)


def create_or_update_master_organization(
    data: MasterOrganizationEm,
    transaction: Transaction,
) -> str:
    if is_fake_uuid(data.id):
        return MasterOrganizationRepository.create_entity(data, transaction)
    else:
        MasterOrganizationRepository.update_entity(data, transaction)
        return data.id


def delete_organization_by_id(organization_id: str, transaction: Transaction):
    MasterOrganizationRepository.delete_entity_by_id(organization_id, transaction)


def get_organization_selection(params) -> List[BasicSelectionVm]:
    return MasterOrganizationRepository.get_selection_by_params()


def get_guest_login_organization_selection() -> List[BasicSelectionVm]:
    return MasterOrganizationRepository.get_selection_by_params(
        guest_enabled=True
    )


def set_user_belong_to_organization(organization_id: str, user_id: str, transaction: Transaction):
    uom: UserOrganizationMapEm = UserOrganizationMapRepository.get_first_entity_by_params(
        params={"user_id": user_id}
    )

    if not uom:
        UserOrganizationMapRepository.create_entity(
            data=UserOrganizationMapEm(user_id=user_id, organization_id=organization_id),
            transaction=transaction,
        )
    elif uom.organization_id != organization_id:
        uom.organization_id = organization_id
        UserOrganizationMapRepository.update_entity(
            data=uom,
            transaction=transaction,
            col_list=["organization_id"],
        )