from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class BasicSelectionVm(BaseModel):
    label: str
    value: str


class BasicTreeSelectionVm(BasicSelectionVm):
    children: Optional[List[BasicTreeSelectionVm]]

BasicTreeSelectionVm.update_forward_refs()
