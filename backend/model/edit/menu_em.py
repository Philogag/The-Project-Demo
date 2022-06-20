from typing import Optional

from backend.model.basic_model import BasicEditModel


class MenuEm(BasicEditModel):
    parent_id: Optional[str]

    path: str
    component: str
    icon: str
    title: str
    name: str
    order: int

    redirect: Optional[str]
    enabled: bool = True
