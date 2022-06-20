from typing import List

from pydantic import BaseModel


class MenuDataRouteMapVm(BaseModel):
    menu_id: str
    route_id_list: List[str]
