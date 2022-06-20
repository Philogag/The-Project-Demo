from typing import List

from backend.data.transaction import Transaction
from backend.model.edit.area_em import AreaEm
from backend.model.entity.area_entity import AreaEntity
from backend.repository.basic_repository import BasicRepository


class AreaRepository(BasicRepository):

    @classmethod
    def create_area(cls, data: AreaEm, transaction: Transaction):
        cls._insert_entity(
            entity_cls=AreaEntity,
            data=data,
            transaction=transaction,
        )

    @classmethod
    def get_area_by_parent_id(cls, parent_id: str = None) -> List[AreaEm]:
        sql = "select * from st_area where "
        if parent_id is None:
            sql += "parent_id is null"
        else:
            sql += "parent_id = :parent_id"

        return cls._fetch_all(
            model_cls=AreaEm,
            sql=sql,
            params={
                "parent_id": parent_id,
            }
        )

    @classmethod
    def get_full_area_list_by_id(cls, area_id):
        """获取 从area_id到根的链表 """
        sql = """
        with RECURSIVE area_tree as (
          select sa1.* from st_area sa1 where sa1.id=:area_id
          union all
          select sa2.* from st_area sa2, area_tree where sa2.id=area_tree.parent_id
        )
        
        SELECT * FROM area_tree order by level asc
        """
        return cls._fetch_all(
            model_cls=AreaEm,
            sql=sql,
            params={
                "area_id": area_id,
            }
        )
