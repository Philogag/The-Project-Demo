from sqlalchemy import Column, String, Integer, Boolean

from backend.model.basic_entity import BasicVersionControlledEntity
from backend.model.entity.history.menu_history import MenuHistoryEntity


class MenuEntity(BasicVersionControlledEntity):
    __tablename__ = "st_menu"
    __history_entity__ = MenuHistoryEntity

    parent_id = Column(String(40), comment="父项目")

    path = Column(String(255), comment="路由", nullable=False)
    component = Column(String(255), comment="组件", nullable=False)
    icon = Column(String(255), comment="名称", nullable=False)
    title = Column(String(40), comment="标题", nullable=False)
    name = Column(String(40), comment="代码", nullable=False)
    order = Column(Integer, comment="排序", nullable=False)

    redirect = Column(String(255), comment="重定向")
    enabled = Column(Boolean, comment="启用", default=True)
