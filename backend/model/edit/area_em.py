from typing import Optional

from pydantic import BaseModel


class AreaEm(BaseModel):
    id: str
    name: str
    parent_id: Optional[str]
    level: Optional[int]
