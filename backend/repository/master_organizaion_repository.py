from typing import List

from backend.data.pagination_carrier import PaginationCarrier, PaginationParams
from backend.model.basic_selection_vm import BasicSelectionVm
from backend.model.edit.master_organization_em import MasterOrganizationEm
from backend.model.entity.master_organization_entity import MasterOrganizationEntity
from backend.model.view.master_organization_vm import MasterOrganizationListItemVm
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder


class MasterOrganizationRepository(BasicRepository):

    __entity_cls__ = MasterOrganizationEntity
    __model_cls__ = MasterOrganizationEm

    @classmethod
    def get_organization_list_page(cls, params: PaginationParams) -> PaginationCarrier[MasterOrganizationListItemVm]:

        sql = """
        with RECURSIVE area_tree as (
            select sa1.*, array[sa1.id::varchar] as path, array[sa1.name::varchar] as full_name 
            from st_area sa1 where sa1.level=0
            union all
            select sa2.*, array_append(area_tree.path, sa2.id::varchar) as path,
            array_append(area_tree.full_name, sa2.name::varchar)
            from st_area sa2, area_tree where sa2.parent_id=area_tree.id 
        )
        select smo.*,
        area_tree.path as area_path, 
        array_to_string(area_tree.full_name, '-') as area_full_name
        from st_master_organization smo
        left join area_tree on area_tree.id = smo.area_id
        order by smo.name asc
        """

        pagination_query = PaginationQueryBuilder(
            result_type=MasterOrganizationListItemVm,
            sql=sql,
            search_columns=['name', 'code'],
            order_columns=params.order_columns if params.order_columns is not None else {},
            params={},
        )
        return pagination_query.get_query_result(
            page_size=params.page_size,
            page_index=params.page_index,
            search_text=params.search_text,
        )


    @classmethod
    def get_selection_by_params(
        cls,
        **params,
    ) -> List[BasicSelectionVm]:
        """[SQL注入警告]"""
        sql = """
        select smo.id as value, smo.name as label
        from st_master_organization smo
        where 1=1
        """

        for k in params.keys():
            sql += " and " + k + " = :" + k 

        return cls._fetch_all(
            sql=sql,
            model_cls=BasicSelectionVm,
            params=params,
        )
