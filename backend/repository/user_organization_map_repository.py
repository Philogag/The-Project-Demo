from backend.model.edit.user_organization_map_em import UserOrganizationMapEm
from backend.model.entity.user_organization_map_entity import UserOrganizationMapEntity
from backend.repository.basic_repository import BasicRepository


class UserOrganizationMapRepository(BasicRepository):
    __entity_cls__ = UserOrganizationMapEntity
    __model_cls__ = UserOrganizationMapEm

