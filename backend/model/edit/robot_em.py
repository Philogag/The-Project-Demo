"""
系统机器人，用于初始化数据、后台任务和定期任务
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RobotEm(BaseModel):
    id: str
    name: str
    code: Optional[str]

    permission_end_at: Optional[datetime]

    def to_orm_dict(self, flat=True):
        return self.dict()