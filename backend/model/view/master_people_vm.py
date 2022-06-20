
from typing import List, Optional
from pydantic import BaseModel, Field

from backend.model.basic_model import BasicModel
from backend.model.edit.master_people_em import MasterPeopleEm
from backend.model.edit.team_em import TeamEm

class MasterPeopleListVm(MasterPeopleEm):
    organization_id: str
    organization_name: str
    sport_meeting_id: str
    sport_meeting_name: str

    team_name: str
    team_group_name: str


class MasterPeopleSignUpSelectionVm(BasicModel):
    id: str
    people_name: str
    people_gender: str
    signed_competition_count: int


class MasterPeopleByTeamVm(BaseModel):
    team: TeamEm
    peoples: Optional[List[MasterPeopleEm]]
