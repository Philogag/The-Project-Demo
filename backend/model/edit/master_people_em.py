
from typing import Optional
from datetime import datetime

from backend.model.basic_model import BasicEditModel


class MasterPeopleEm(BasicEditModel):
    team_id: str
    team_group_id: str
    people_name: str
    people_gender: str
    people_birth: datetime

    number_cloth_id: Optional[int]
    number_cloth: Optional[str]  # not input by user, generate by system
