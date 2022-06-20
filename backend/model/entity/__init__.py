import os
from typing import Any, List

skip_entity = ["BasicVersionControlledEntity"]


def scan_all_entities() -> List[Any]:
    results = []
    for file in os.listdir("./backend/model/entity/"):
        if file.endswith("entity.py"):
            module_name = file[:-3]
            module = __import__("backend.model.entity." + module_name, fromlist=True)
            for name, sub_cls in module.__dict__.items():
                if name in skip_entity:
                    continue
                if name.endswith("Entity"):
                    results.append(sub_cls)
    return results
