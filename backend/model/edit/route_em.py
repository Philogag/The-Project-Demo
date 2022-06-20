"""
路由
"""

from pydantic import BaseModel

# from backend.model.basic_model import BasicModel


class RouteEm(BaseModel):
    id: str = None
    route_path: str

    group: str
    name: str
    need_login: bool = True
    allow_all: bool = False

    def to_orm_dict(self, flat=True):
        return self.dict()
