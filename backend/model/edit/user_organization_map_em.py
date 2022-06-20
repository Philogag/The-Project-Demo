
from backend.model.basic_model import BasicModel


class UserOrganizationMapEm(BasicModel):
    user_id: str
    organization_id: str
