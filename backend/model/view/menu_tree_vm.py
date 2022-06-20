from typing import Any, Dict, Optional

from backend.model.basic_tree_vm import BasicTreeVm


class MenuTreeVm(BasicTreeVm):
    parent_id: Optional[str]

    path: str
    real_path: Optional[str]  # 实际path
    component: str
    icon: str
    title: str
    name: str
    order: int

    route_count: Optional[int] = 0

    meta: Optional[Dict[str, Any]]
    redirect: Optional[str]
    enabled: Optional[bool]
    selected: Optional[bool]

    def create_meta(self):
        self.meta = {
            "order_no": self.order,
            "icon": self.icon,
            "title": self.title,
        }
