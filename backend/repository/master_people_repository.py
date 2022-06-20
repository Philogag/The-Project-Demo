from typing import List

from backend.data.pagination_carrier import PaginationCarrier, PaginationParams
from backend.model.edit.master_people_em import MasterPeopleEm
from backend.model.entity.master_people_entity import MasterPeopleEntity
from backend.model.view.master_people_vm import (
    MasterPeopleListVm,
    MasterPeopleSignUpSelectionVm,
    MasterPeopleByTeamVm,
)
from backend.repository.basic_repository import BasicRepository, PaginationQueryBuilder
from backend.utility.string_helper import is_fake_uuid


class MasterPeopleRepository(BasicRepository):
    __entity_cls__ = MasterPeopleEntity
    __model_cls__ = MasterPeopleEm

    @classmethod
    def fetch_page(cls, params: PaginationParams) -> PaginationCarrier[MasterPeopleListVm]:
        sql = """
        select smp.*
        ,st.name as team_name
        ,stg.name as team_group_name
        ,ssm.id as sport_meeting_id
        ,ssm.name as sport_meeting_name
        ,smo.id as organization_id
        ,smo.name as organization_name
        from st_master_people smp
        inner join st_team st on st.id = smp.team_id
        inner join st_team_group stg on stg.id = smp.team_group_id
        inner join st_sport_meeting ssm on ssm.id = st.sport_meeting_id
        inner join st_master_organization smo on smo.id = st.organization_id
        order by smo.name asc, ssm.name asc, smp.number_cloth asc
        """

        pagination_query = PaginationQueryBuilder(
            result_type=MasterPeopleListVm,
            sql=sql,
            search_columns=['people_name'],
            filter_columns=['organization_id', 'sport_meeting_id', 'team_id'],
            order_columns=params.order_columns if params.order_columns is not None else {},
            params={},
        )
        return pagination_query.get_query_result(
            page_size=params.page_size,
            page_index=params.page_index,
            search_text=params.search_text,
            filter_option=params.filter_columns,
        )

    @classmethod
    def get_people_selection_by_team_for_sign_up(cls, team_id) -> List[MasterPeopleSignUpSelectionVm]:
        """用于报名的运动员列表，包含当前所报项目数量"""
        sql = """
        select smp.id, smp.people_name, smp.people_gender
        , coalesce(competition.signed_competition_count, 0) as signed_competition_count
        from st_master_people smp
        left join (
            select cr.contestant_id, count(distinct cr.competition_id) as signed_competition_count
            from competition_result cr
            where cr.contestant_category = 'people'
            group by cr.contestant_id
        ) competition on competition.contestant_id = smp.id
        inner join st_team st on st.id = smp.team_id
        where smp.team_id = :team_id
            and (
                st.competition_per_people = 0 
                or st.competition_per_people > competition.signed_competition_count
                or competition.signed_competition_count is null
            )
        """
        return cls._fetch_all(
            model_cls=MasterPeopleSignUpSelectionVm,
            sql=sql,
            params={
                "team_id": team_id,
            }
        )

    @classmethod
    def get_people_count(cls, team_id: str, people_gender: str):
        sql = """
        select * from st_master_people smp
        where team_id = :team_id and people_gender = :people_gender
        """
        return cls._fetch_count(
            sql=sql,
            params={
                "team_id": team_id, "people_gender": people_gender,
            }
        )

    @classmethod
    def check_number_cloth_unique(cls, sport_meeting_id: str, number_cloth_id: int, master_people_id: str):
        if not is_fake_uuid(master_people_id) \
            and cls.check_entity_exist(id=master_people_id, number_cloth_id=number_cloth_id):
            # Not changed
            return True
        else:
            sql = """
            select * 
            from st_master_people smp 
            inner join st_team st on st.id = smp.team_id
            where smp.number_cloth_id = :number_cloth_id
              and st.sport_meeting_id = :sport_meeting_id
            """
            return cls._fetch_count(
                sql=sql,
                params={
                    "sport_meeting_id": sport_meeting_id,
                    "number_cloth_id": number_cloth_id,
                }
            ) <= 0
    
    @classmethod
    def get_used_number_cloth_id_of_team(cls, team_id: str, people_gender: str) -> List[int]:
        data = cls._fetch_all_for_dict(
            sql="""
            select smp.number_cloth_id
            from st_master_people smp
            where smp.team_id = :team_id
              and smp.people_gender = :people_gender
            """,
            params={
                "team_id": team_id,
                "people_gender": people_gender,
            }
        )
        return list(map(lambda x: x['number_cloth_id'], data))

    @classmethod
    def get_people_list_group_by_team(cls, sport_meeting_id: str) -> List[MasterPeopleByTeamVm]:
        sql = """
        select 
        row_to_json(st) as team
        , peoples.list as peoples
        from st_team st
        left join (
            select smp.team_id, json_agg(row_to_json(smp)) as list
            from st_master_people smp
            group by smp.team_id
        ) peoples on peoples.team_id = st.id
        where st.sport_meeting_id = :sport_meeting_id
        order by st.number_cloth_begin
        """
        return cls._fetch_all(
            sql=sql,
            model_cls=MasterPeopleByTeamVm,
            params={
                "sport_meeting_id": sport_meeting_id
            }
        )
    