"""
路由实体，包括前后端路由
"""
from sqlalchemy import Boolean, Column, String

from backend.model.basic_entity import BasicEntity


class RouteEntity(BasicEntity):
    __tablename__ = "st_route"

    route_path = Column(String(255), comment="路由", unique=True, nullable=False)

    group = Column(String(255), comment="分组", nullable=True)
    name = Column(String(255), comment="名称", nullable=True)
    need_login = Column(Boolean, comment="需要登录", default=True)
    allow_all = Column(Boolean, comment="允许所有用户", default=False)
