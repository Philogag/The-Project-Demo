from typing import Any, Callable, List, Optional

from backend.model.basic_model import BasicModel


class BasicTreeVm(BasicModel):
    child_id_list: Optional[List[str]] = []
    children: Optional[List[Any]] = []


def build_tree(item_list, order_key: Callable = None):
    """
    将节点列表构建为多个树
    item.parent_id 为 None 时判定为根，根据 item.child_id_list 建树
    """
    item_dict = {
        item.id: item
        for item in item_list
    }

    def build_sub_tree(o: BasicTreeVm):
        if o.child_id_list:
            for i in o.child_id_list:
                if i in item_dict.keys():
                    o.children.append(item_dict[i])
            for item in o.children:
                build_sub_tree(item)
            if order_key is not None:
                o.children.sort(key=order_key)
        else:
            o.children = None
        return o

    result = []
    for item in item_list:
        if item.parent_id is None:
            result.append(build_sub_tree(item))

    return result
