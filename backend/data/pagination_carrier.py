from typing import Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class PaginationParams(BaseModel):
    search_text: Optional[str] = ""  # 模糊搜索, 在 PaginationQueryBuilder.search_columns 中搜索
    order_columns: Dict[str, str] = None  # 排序 { col_name: asc/desc }
    filter_columns: Dict[str, Union[None, str, List[str]]] = None  # 筛选 { col_name: [list of value of col_name] }
    page_size: int = 10
    page_index: int = 0


class PaginationCarrier(GenericModel, Generic[DataT]):
    search_text: Optional[str]
    total_count: int = 0
    filter_count: int = 0
    page_index: int = 0
    page_size: int = 10
    data: List[DataT]

