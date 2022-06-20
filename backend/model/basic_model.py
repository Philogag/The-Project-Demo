import json
from typing import Optional

from pydantic import BaseModel


class _BasicModel(BaseModel):

    id: Optional[str]
    version: int = 1

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._parse_json_fields()

    def to_orm_dict(self, flat=True):
        """用于获取向数据库写入的 dict ，将嵌套类转化为 json """
        obj = self.dict()
        if flat:  # 扁平化，递归项转json字符串
            for k, v in obj.items():
                if isinstance(v, (list, set, dict, tuple, BaseModel)):
                    obj[k] = json.dumps(v, ensure_ascii=False)
        return obj

    def _parse_json_fields(self):
        for field in self.Config.orm_json_fields:
            value = getattr(self, field)
            if isinstance(value, str):
                value = json.loads(value)
                setattr(self, field, value)

    class Config:
        # 数据库加载时需要json解析的字段
        orm_json_fields = []


BasicModel = _BasicModel
BasicEditModel = _BasicModel
