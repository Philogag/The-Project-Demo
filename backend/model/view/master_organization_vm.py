from typing import List, Optional

from backend.model.edit.master_organization_em import MasterOrganizationEm


class MasterOrganizationListItemVm(MasterOrganizationEm):
    area_path: Optional[List[str]]
    area_full_name: Optional[str]
