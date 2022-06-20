from datetime import datetime
from typing import Any, Callable, List

from pydantic import BaseModel

from backend.utility.error_helper import BusinessError
from backend.utility.string_helper import name_underline_to_camel


def __is_iterable_obj(obj):
    t = type(obj)
    return t == dict or t == list or t == tuple or t == set


def rebuild_obj_key(obj: Any, rebuild_fn: Callable) -> Any:
    if __is_iterable_obj(obj):
        if type(obj) == dict:
            return {
                rebuild_fn(k): rebuild_obj_key(v, rebuild_fn) if __is_iterable_obj(v) else v
                for k, v in obj.items()
            }
        else:
            return [rebuild_obj_key(item, rebuild_fn) for item in obj]
    else:
        return obj


class BasicCarrier(BaseModel):
    """
    统一的数据返回格式
    """

    code: int = 200
    timestamp: datetime = datetime.now()
    message: List[str] = []
    result: Any

    def to_dict(self, to_camel=True):
        obj = self.dict()
        if to_camel:
            obj = rebuild_obj_key(obj, name_underline_to_camel)
        return obj

    def push_exception(self, err: Exception, code: int = 200):
        self.code = code
        if isinstance(err, BusinessError):
            if type(err.message) in [list, tuple, set]:
                self.message += err.message
            else:
                self.message.append(str(err.message))
        else:
            self.message.append(str(err))


MessageCarrier = BasicCarrier
