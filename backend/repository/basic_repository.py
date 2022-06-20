# standard library
import copy
import inspect
import logging
import string
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import ColumnProperty, Query, class_mapper

from backend.data.pagination_carrier import PaginationCarrier
from backend.data.transaction import Transaction
from backend.factory import db
from backend.model.basic_entity import (
    BasicHistoryEntity,
    BasicVersionControlledEntity,
    SqlAlchemyEntity,
)
from backend.model.basic_model import BasicEditModel
from backend.utility.error_helper import (
    BusinessError,
    ClassConfigNotSetError,
    DoesNotSupportUpdatingBySql,
    EntityNotFoundError,
    InvalidHistoryDataError,
    InvalidSqlAlchemyClassAttrError,
    InvalidSqlAlchemyClassColumnError,
    InvalidSqlAlchemyClassError,
    InvalidSqlAlchemyClassWithIdError,
)
from backend.utility.string_helper import generate_random_string, generate_uuid_id, is_blank
# project library
from backend.utility.type_helper import is_simple_iterable

GenericData = TypeVar("GenericData", bound=BaseModel)
ModelClassType = TypeVar("ModelClassType", bound=BaseModel)
EntityClassType = TypeVar("EntityClassType", bound=BaseModel)

logger = logging.getLogger('repository')


class BasicRepository:
    """
    Repository 基类
    """

    __entity_cls__: Type[EntityClassType] = None
    __model_cls__: Type[EntityClassType] = None

    @staticmethod
    def _fetch_all_for_dict(sql: str, params: Dict[str, Any] = None) -> List:
        """
         获取对应sql和参数的所有记录
        :param sql:
        :param params:
        :return:
        """
        logger.debug("fetch_all: %s <= %s", sql, params)
        result_list = BasicRepository._execute_sql(sql=sql, params=params)
        return result_list

    @staticmethod
    def _fetch_all(
            model_cls: Type[GenericData], sql: str, params: Dict[str, Any] = None
    ) -> List[GenericData]:
        """
         获取对应sql和参数的所有记录
        :param model_cls:
        :param sql:
        :param params:
        :return:
        """
        logger.debug("fetch_all: %s <= %s", sql, params)
        result_list = BasicRepository._execute_sql(sql=sql, params=params)
        return [model_cls(**result_dict) for result_dict in result_list]

    @staticmethod
    def _fetch_first(
            model_cls: Type[GenericData], sql: str, params: Dict[str, Any] = None
    ) -> Optional[GenericData]:
        """
         获取对应sql和参数的对应第一条数据
        :param model_cls:
        :param sql:
        :param params:
        :return:
        """
        sql_stmt = "select * from ({0}) first_only limit 1".format(sql)
        result = BasicRepository._fetch_all(
            sql=sql_stmt, params=params, model_cls=model_cls
        )
        if result and len(result) > 0:
            return result[0]
        return None

    @staticmethod
    def _execute_sql(sql: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        执行sql语句，并返回字典列表
        :param sql:
        :param params:
        # :param is_update:
        :return:
        """
        stmt = text(sql)
        logger.debug("execute_sql: %s <= %s", sql, params)
        result = db.session.execute(stmt, params=params)
        return BasicRepository._row_result_to_list(result)

    @staticmethod
    def _fetch_count(sql: str, params: Dict[str, Any] = None) -> int:
        """
        获取对应sql和参数的记录总数
        :param sql:
        :param params:
        :return:
        """
        stmt = text(
            "select count(0) from ({0}) count_{1}".format(
                sql, generate_random_string(6, chars=string.ascii_lowercase)
            )
        )
        logger.debug("fetch_count: %s <= %s", sql, params)
        return db.session.execute(stmt, params=params).scalar()

    @staticmethod
    def _get_model_by_id(
            model_cls: Type[GenericData], entity_cls: SqlAlchemyEntity, model_id: str
    ) -> Optional[GenericData]:
        """
        根据数据库对象id来获取对象
        :param model_cls:
        :param entity_cls:
        :param model_id:
        :return:
        """
        if BasicRepository._is_sqlalchemy_class_has_id(input_cls=entity_cls):
            table_name = BasicRepository.__get_entity_table_name(entity_cls=entity_cls)
            sql = f"""select * from {table_name} where id = :model_id"""
            return BasicRepository._fetch_first(
                model_cls=model_cls, sql=sql, params={"model_id": model_id}
            )
        raise InvalidSqlAlchemyClassWithIdError(cls=entity_cls)

    @staticmethod
    def _get_model_by_params(
            model_cls: Type[GenericData],
            entity_cls: SqlAlchemyEntity,
            params: Dict[str, Any] = None,
    ) -> Optional[GenericData]:
        """
        将完全等于字典列举条件的对象捞出来第一个
        :param model_cls:
        :param entity_cls:
        :param params:
        :return:
        """
        sql = BasicRepository.__build_sql(entity_cls=entity_cls, params=params)
        return BasicRepository._fetch_first(model_cls=model_cls, sql=sql, params=params)

    @staticmethod
    def _get_model_list_by_params(
            model_cls: Type[GenericData],
            entity_cls: SqlAlchemyEntity,
            params: Dict[str, Any],
    ) -> List[GenericData]:
        """
        将完全等于字典列举条件的对象以列表形式捞出来
        :param entity_cls:
        :param params:
        :return:
        """
        sql = BasicRepository.__build_sql(entity_cls=entity_cls, params=params)
        return BasicRepository._fetch_all(model_cls=model_cls, sql=sql, params=params)

    @staticmethod
    def _get_dict_list_by_params(
            entity_cls: SqlAlchemyEntity, params: Dict[str, Any]
    ) -> List:
        """
        将完全等于字典列举条件的对象以列表形式捞出来
        :param entity_cls:
        :param params:
        :return:
        """
        sql = BasicRepository.__build_sql(entity_cls=entity_cls, params=params)
        return BasicRepository._fetch_all_for_dict(sql=sql, params=params)

    @staticmethod
    def _get_entities_count_by_params_exclude_self(
            entity_cls: SqlAlchemyEntity,
            params: Dict[str, Any] = None,
            entity_id: str = None,
    ) -> int:
        """
        統計完全等于字典列举条件并且id不等於輸入的id的对象的個數
        :param entity_cls:
        :param params:
        :return:
        """
        sql = BasicRepository.__build_sql(entity_cls=entity_cls, params=params)
        if entity_id:
            is_history = BasicRepository.__check_entity_is_history(
                entity_cls=entity_cls
            )
            filter_col = "history_id" if is_history else "id"
            entity_id_param = f"entity_id_{generate_random_string()}"
            sql += f""" and {filter_col} != :{entity_id_param}"""
            params[entity_id_param] = entity_id
        return BasicRepository._fetch_count(sql=sql, params=params)

    @staticmethod
    def _insert_entity(
            entity_cls: SqlAlchemyEntity, data: BasicEditModel, transaction: Transaction
    ) -> str:
        """
        根据字典信息来插入数据库数据
        :param entity_cls:
        :param data:
        :param transaction:
        :return:
        """
        entity_data = data.to_orm_dict(flat=True)
        entity_column_name_list = BasicRepository._get_entity_column_name_list(
            entity_cls=entity_cls
        )
        BasicRepository.__prepare_handler_info(
            entity_column_name_list=entity_column_name_list,
            entity_data=entity_data,
            transaction=transaction,
        )
        entity_id = BasicRepository.__insert_entity_by_dict(
            entity_cls=entity_cls, entity_data=entity_data
        )
        if BasicRepository.__check_entity_is_version_controlled(entity_cls=entity_cls):
            BasicRepository.__insert_history_entity_by_dict(
                original_entity_cls=entity_cls,
                entity_data=entity_data,
                transaction_id=transaction.id,
            )
        return entity_id

    @staticmethod
    def _insert_entity_by_dict(
            entity_cls: SqlAlchemyEntity, entity_data: Dict, transaction: Transaction
    ) -> str:
        """
        根据字典信息来插入数据库数据
        :param entity_cls:
        :param entity_data:
        :param transaction:
        :return:
        """
        entity_column_name_list = BasicRepository._get_entity_column_name_list(
            entity_cls=entity_cls
        )
        BasicRepository.__prepare_handler_info(
            entity_column_name_list=entity_column_name_list,
            entity_data=entity_data,
            transaction=transaction,
        )
        entity_id = BasicRepository.__insert_entity_by_dict(
            entity_cls=entity_cls, entity_data=entity_data
        )
        if BasicRepository.__check_entity_is_version_controlled(entity_cls=entity_cls):
            BasicRepository.__insert_history_entity_by_dict(
                original_entity_cls=entity_cls,
                entity_data=entity_data,
                transaction_id=transaction.id,
            )
        return entity_id

    @staticmethod
    def _update_entity(
            entity_cls: SqlAlchemyEntity,
            data: BasicEditModel,
            transaction: Transaction,
            col_list: List = None,
    ):
        """
        根据字典信息来更新数据库数据
        :param entity_cls:
        :param data:
        :param transaction:
        :param col_list: 需要更新的列，如果传入，则只更新传入的字段
        :return:
        """
        entity_data = data.to_orm_dict(flat=True)
        col_name_list = BasicRepository.__prepare_entity_updated_col(
            entity_cls=entity_cls, col_list=col_list
        )
        BasicRepository.__prepare_handler_info(
            entity_column_name_list=col_name_list,
            entity_data=entity_data,
            transaction=transaction,
        )
        is_version_controlled = BasicRepository.__check_entity_is_version_controlled(
            entity_cls=entity_cls
        )
        entity_data = BasicRepository.__update_entity_by_dict(
            entity_cls=entity_cls,
            entity_data=entity_data,
            col_name_list=col_name_list,
            is_version_controlled=is_version_controlled,
        )
        if is_version_controlled:
            BasicRepository.__update_history_entity_record(
                original_entity_cls=entity_cls,
                entity_data=entity_data,
                transaction_id=transaction.id,
            )
        return entity_data["id"]

    @staticmethod
    def _delete_entity_by_id(
            entity_cls: SqlAlchemyEntity, entity_id: str, transaction: Transaction
    ):
        """
        根据类和id来删除对应的数据
        :param entity_cls:
        :param entity_id:
        :param transaction:
        :return:
        """
        if not BasicRepository._is_sqlalchemy_class_has_id(input_cls=entity_cls):
            raise InvalidSqlAlchemyClassWithIdError(cls=entity_cls)
        db.session.query(entity_cls).filter(entity_cls.id == entity_id).delete()
        entity_data = {
            "id": entity_id,
            "end_transaction_id": transaction.id,
            "handled_at": transaction.handled_at,
        }
        history_cls = BasicRepository.__get_entity_history_cls(entity_cls)
        BasicRepository.__update_history_entity_by_dict(
            history_cls=history_cls, entity_data=entity_data
        )

    @staticmethod
    def _delete_entity_by_params(
            entity_cls: SqlAlchemyEntity, params: dict, transaction: Transaction
    ):
        """
        根据参数删除实体
        :param entity_cls:
        :param params:
        :param transaction:
        :return:
        """
        entity_list = BasicRepository._build_sqlalchemy_query(
            entity_cls=entity_cls, params=params
        ).all()
        for entity in entity_list:
            BasicRepository._delete_entity_by_id(
                entity_cls=entity_cls, entity_id=entity.id, transaction=transaction
            )

    @staticmethod
    def _delete_entities_by_params(
            entity_cls: SqlAlchemyEntity, params: Dict[str, Any], transaction: Transaction
    ):
        """
        根据输入的参数删除匹配的数据
        :param entity_cls:
        :param params:
        :param transaction:
        :return:
        """
        query = BasicRepository._build_sqlalchemy_query(
            entity_cls=entity_cls, params=params
        )
        for entity in query.all():
            BasicRepository._delete_entity_by_id(
                entity_cls=entity_cls, entity_id=entity.id, transaction=transaction
            )

    @staticmethod
    def _check_entity_existed(
            entity_cls: SqlAlchemyEntity, params: Dict[str, Any]
    ) -> bool:
        """
        根据传入条件判断对象是否存在
        :param entity_cls:
        :param params:
        :return:
        """
        sql = BasicRepository.__build_sql(entity_cls=entity_cls, params=params)
        count = BasicRepository._fetch_count(sql=sql, params=params)
        return count > 0

    @staticmethod
    def _row_result_to_list(execute_result: CursorResult) -> List[Dict[str, Any]]:
        """
        将SqlAlchemy的RowResultProxy结果集转换为字典列表
        :param execute_result:
        :return:
        """
        if not execute_result.returns_rows:
            raise DoesNotSupportUpdatingBySql()
        result = []
        cols = execute_result.cursor.description
        for row in execute_result:
            row_dict = {}
            for column in cols:
                row_dict[column.name] = row[column.name]
            result.append(row_dict)
        return result

    @staticmethod
    def _is_sqlalchemy_class_has_id(input_cls: Type) -> bool:
        """
        判断是否是一个有id字段的sql alchemy实体类
        :param input_cls:
        :return:bool
        """
        return bool(
            BasicRepository._is_sqlalchemy_class(input_cls=input_cls)
            and hasattr(input_cls, "id")
        )

    @staticmethod
    def _is_sqlalchemy_class(input_cls: Type) -> bool:
        """
        判断一个类是否是sql alchemy的类
        :param input_cls: 类
        :return:bool
        """
        try:
            class_mapper(input_cls)
            return True
        except SQLAlchemyError:
            return False

    @staticmethod
    def __insert_entity_by_dict(
            entity_cls: SqlAlchemyEntity, entity_data: Dict[str, Any]
    ) -> str:
        """
        根据字典信息来插入数据库数据
        :param entity_cls:
        :param entity_data:
        :return:str
        """
        if not entity_data.get("id") or is_blank(entity_data.get("id")):
            entity_data["id"] = generate_uuid_id()
        new_entity = BasicRepository.__prepare_new_entity_data(
            entity_cls=entity_cls, entity_data=entity_data
        )
        db.session.add(new_entity)
        return entity_data["id"]

    @staticmethod
    def __insert_history_entity_by_dict(
            original_entity_cls: SqlAlchemyEntity,
            entity_data: Dict[str, Any],
            transaction_id: str,
    ):
        """
        插入历史数据
        :param original_entity_cls:
        :param entity_data:
        :param transaction_id:
        :return:str
        """
        history_cls = BasicRepository.__get_entity_history_cls(original_entity_cls)
        history_data = copy.deepcopy(entity_data)
        history_data["begin_transaction_id"] = transaction_id
        history_data["begin_at"] = history_data["handled_at"]
        history_data["history_id"] = generate_uuid_id()
        new_entity = BasicRepository.__prepare_new_entity_data(
            entity_cls=history_cls, entity_data=history_data
        )
        db.session.add(new_entity)
        return entity_data["id"]

    @staticmethod
    def _get_entity_column_name_list(entity_cls: Type) -> List[str]:
        """
        根据数据库模型类获取该类的字段属性列表
        :param entity_cls:
        :return:List
        """
        if BasicRepository._is_sqlalchemy_class(entity_cls):
            return [
                prop.key
                for prop in class_mapper(entity_cls).iterate_properties
                if isinstance(prop, ColumnProperty)
            ]
        raise InvalidSqlAlchemyClassError(cls=entity_cls)

    @staticmethod
    def __prepare_handler_info(
            entity_column_name_list: List[str],
            entity_data: Dict[str, Any],
            transaction: Transaction,
    ):
        """
        清除操作列数据并更新更系列
        :param entity_column_name_list:
        :param entity_data:
        :param transaction:
        :return:None
        """
        if "handler_category" in entity_column_name_list and not entity_data.get(
                "handler_category"
        ):
            entity_data["handler_category"] = transaction.handler_category
        if "handler_id" in entity_column_name_list and not entity_data.get(
                "handler_id"
        ):
            entity_data["handler_id"] = transaction.handler_id
        if "handled_at" in entity_column_name_list and not entity_data.get(
                "handled_at"
        ):
            entity_data["handled_at"] = transaction.handled_at

    @staticmethod
    def _new_entity_from_model(entity_cls: Type) -> SqlAlchemyEntity:
        """
        根据类来生成一个对象
        :param entity_cls:
        :return:SqlAlchemyEntity
        """
        if BasicRepository._is_sqlalchemy_class(entity_cls):
            return entity_cls()
        raise InvalidSqlAlchemyClassError(cls=entity_cls)

    @staticmethod
    def __prepare_new_entity_data(
            entity_cls: SqlAlchemyEntity, entity_data: Dict[str, Any]
    ) -> SqlAlchemyEntity:
        """
        准备实体数据
        :param entity_cls:
        :param entity_data:
        :return:
        """
        new_entity = BasicRepository._new_entity_from_model(entity_cls=entity_cls)
        for dict_key, dict_value in entity_data.items():
            if hasattr(new_entity, dict_key) and dict_value is not None:
                if isinstance(dict_value, Enum):
                    setattr(new_entity, dict_key, dict_value.name)
                else:
                    setattr(new_entity, dict_key, dict_value)
        return new_entity

    @staticmethod
    def __update_entity_by_dict(
            entity_cls: SqlAlchemyEntity,
            entity_data: Dict,
            col_name_list: List[str],
            is_version_controlled: bool,
    ) -> Dict[str, Any]:
        """
        根据字典信息来更新数据库数据
        :param entity_cls:
        :param entity_data:
        :return:
        """

        # 字典里面有entity没有的值会报错
        entity_data = {
            key: values for key, values in entity_data.items() if key in col_name_list
        }

        query = db.session.query(entity_cls)
        if not entity_data.get("id") or is_blank(entity_data.get("id")):
            raise InvalidSqlAlchemyClassColumnError(cls=entity_cls, column_name="id")
        query = query.filter(entity_cls.id == entity_data["id"])
        if is_version_controlled:
            if "version" in col_name_list and entity_data.get("version") is None:
                raise BusinessError("版本号不能为空")
            version = entity_data["version"]
            query = query.filter(entity_cls.version == entity_data["version"])
            entity_data["version"] = version + 1

        effected_rows = query.update(entity_data)
        if effected_rows == 0:
            raise EntityNotFoundError(
                cls=entity_cls,
                entity_id=entity_data["id"],
                version=version if is_version_controlled else None,
            )
        return entity_data

    @staticmethod
    def __update_history_entity_record(
            original_entity_cls: SqlAlchemyEntity, entity_data: Dict, transaction_id: str
    ):
        """
        更新历史实体记录， 填入最新一条的end_at和end_transaction_id,并插入最新条
        :param original_entity_cls:
        :param entity_data:
        :param transaction_id:
        :return:
        """
        history_cls = BasicRepository.__get_entity_history_cls(original_entity_cls)
        his_entity_data = copy.deepcopy(entity_data)
        his_entity_data["end_transaction_id"] = transaction_id
        last_data = BasicRepository.__update_history_entity_by_dict(
            history_cls=history_cls, entity_data=his_entity_data
        )
        fully_col_list = BasicRepository._get_entity_column_name_list(
            entity_cls=history_cls
        )
        for col in fully_col_list:
            if col not in entity_data:
                entity_data[col] = last_data[col]
        BasicRepository.__insert_history_entity_by_dict(
            original_entity_cls=original_entity_cls,
            entity_data=entity_data,
            transaction_id=transaction_id,
        )

    @staticmethod
    def __update_history_entity_by_dict(
            history_cls: SqlAlchemyEntity, entity_data: Dict
    ) -> Dict[str, Any]:
        """
        根据字典信息来更新数据库数据
        :param entity_data:
        :return:
        """
        col_name_list = ["id", "end_transaction_id", "end_at"]
        # 字典里面有entity没有的值会报错
        handled_at = entity_data.get("handled_at")
        entity_data = {
            key: values for key, values in entity_data.items() if key in col_name_list
        }
        entity_data["end_at"] = handled_at
        history_table = BasicRepository.__get_entity_table_name(entity_cls=history_cls)
        sql = f"""select * from {history_table} where id = :entity_id
        and end_at is null"""
        data = BasicRepository._execute_sql(
            sql=sql, params={"entity_id": entity_data["id"]}
        )
        if len(data) != 1:
            raise InvalidHistoryDataError(
                f"{history_cls} [{entity_data['id']}] has {len(data)} rows"
            )
        entity_data["history_id"] = data[0]["history_id"]
        query = db.session.query(history_cls)
        query = query.filter(history_cls.history_id == data[0]["history_id"])
        query.update(entity_data)
        return data[0]

    @staticmethod
    def __prepare_entity_updated_col(
            entity_cls: SqlAlchemyEntity, col_list: List = None
    ) -> List[str]:
        """
        准备更新实体的列名集合
        :param entity_cls:
        :param col_list:
        :return:
        """
        if col_list:
            entity_col_list = BasicRepository._get_entity_column_name_list(entity_cls)
            invalid_col_list = [x for x in col_list if x not in entity_col_list]
            if invalid_col_list:
                raise InvalidSqlAlchemyClassColumnError(
                    cls=entity_cls, column_name=";".join(invalid_col_list)
                )
            basic_col_set = {
                "id",
                "version",
                "handled_at",
                "handler_id",
                "handler_category",
            }
            return list(basic_col_set | set(col_list))
        return BasicRepository._get_entity_column_name_list(entity_cls)

    @staticmethod
    def __get_entity_history_cls(original_cls: SqlAlchemyEntity) -> SqlAlchemyEntity:
        """
        获取实体的历史类
        :param original_cls:
        :return:
        """
        return BasicRepository.__get_entity_cls_attr(
            entity_cls=original_cls, attr="__history_entity__"
        )

    @staticmethod
    def __get_entity_cls_attr(entity_cls: SqlAlchemyEntity, attr: str) -> Any:
        """
        获取实体类中的属性
        :param entity_cls:
        :param attr:
        :return:
        """
        if not hasattr(entity_cls, attr):
            raise InvalidSqlAlchemyClassAttrError(entity_cls, attr)
        return getattr(entity_cls, attr)

    @staticmethod
    def __get_entity_table_name(entity_cls: SqlAlchemyEntity) -> str:
        """
        获取实体的历史类
        :return:
        """
        return BasicRepository.__get_entity_cls_attr(
            entity_cls=entity_cls, attr="__tablename__"
        )

    @staticmethod
    def _build_sqlalchemy_query(
            entity_cls: SqlAlchemyEntity, params: Dict[str, Any] = None
    ) -> Query:
        """
        根据输入的数据库类及查询条件构建查询
        :param entity_cls:
        :param params:
        :return:
        """
        if not BasicRepository._is_sqlalchemy_class(entity_cls):
            raise InvalidSqlAlchemyClassError(cls=entity_cls)
        query = db.session.query(entity_cls)
        if params:
            for attr, value in params.items():
                # 需要判断数据库类是否有该对应字段
                if hasattr(entity_cls, attr):
                    query = query.filter(getattr(entity_cls, attr) == value)
        return query

    @staticmethod
    def __build_sql(entity_cls: SqlAlchemyEntity, params: Dict[str, Any]) -> str:
        """
        根据输入的数据库类及查询条件构建查询
        :param entity_cls:
        :param params:
        :return:
        """
        table_name = BasicRepository.__get_entity_table_name(entity_cls=entity_cls)
        sql = f"""select * from {table_name} where 1=1 """
        for key, value in params.items():
            key_method = f'any(array[:{key}])' if is_simple_iterable(value) else f':{key}'
            sql += f""" and {key} = {key_method}"""
        return sql

    @staticmethod
    def __check_entity_is_version_controlled(entity_cls: SqlAlchemyEntity) -> bool:
        """
        坚持实体是否为版本控制类
        :param entity_cls:
        :return:
        """
        entity_mro = inspect.getmro(entity_cls)
        return BasicVersionControlledEntity in entity_mro

    @staticmethod
    def __check_entity_is_history(entity_cls: SqlAlchemyEntity) -> bool:
        """
        坚持实体是否为版本控制类
        :param entity_cls:
        :return:
        """
        entity_mro = inspect.getmro(entity_cls)
        return BasicHistoryEntity in entity_mro

    @staticmethod
    def _fetch_page(
            sql: str, page_size: int, page_index: int, params: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        获取对应sql和参数的对应分页的数据
        :param sql:
        :param page_size:
        :param page_index:
        :param params:
        :return:
        """
        sql_page = f"{sql} offset {page_size} limit {page_index}"
        stmt = text(sql_page)
        logger.debug("fetch_page: %s <= %s", sql_page, params)
        return BasicRepository._row_result_to_list(
            db.session.execute(stmt, params=params)
        )

    @staticmethod
    def _build_pagination_segment(page_size: int, page_index: int) -> str:
        """
        获取分页sql后缀
        """
        return "offset {0} limit {1}".format(page_index, page_size)

    @classmethod
    def _get_entity_cls_(cls):
        if cls.__entity_cls__ is not None:
            return cls.__entity_cls__
        raise ClassConfigNotSetError(cls, '__entity_cls__')

    @classmethod
    def _get_model_cls_(cls):
        if cls.__model_cls__ is not None:
            return cls.__model_cls__
        raise ClassConfigNotSetError(cls, '__model_cls__')

    @classmethod
    def get_first_entity_by_params(cls, params) -> Optional[ModelClassType]:
        return cls._get_model_by_params(
            entity_cls=cls._get_entity_cls_(),
            model_cls=cls._get_model_cls_(),
            params=params,
        )

    @classmethod
    def get_all_entity_by_params(cls, **params) -> List[ModelClassType]:
        return cls._get_model_list_by_params(
            entity_cls=cls._get_entity_cls_(),
            model_cls=cls._get_model_cls_(),
            params=params,
        )

    @classmethod
    def check_entity_exist(cls, **params) -> bool:
        return cls._check_entity_existed(
            entity_cls=cls._get_entity_cls_(),
            params=params,
        )

    @classmethod
    def create_entity(cls, data: GenericData, transaction: Transaction) -> str:
        data.id = cls._insert_entity(
            entity_cls=cls._get_entity_cls_(),
            data=data,
            transaction=transaction,
        )
        return data.id

    @classmethod
    def update_entity(cls, data: GenericData, transaction: Transaction, col_list: List[str] = None) -> Any:
        return cls._update_entity(
            entity_cls=cls._get_entity_cls_(),
            data=data,
            transaction=transaction,
            col_list=col_list
        )

    @classmethod
    def fetch_by_id(cls, entity_id: object) -> Optional[ModelClassType]:
        return cls._get_model_by_params(
            entity_cls=cls._get_entity_cls_(),
            model_cls=cls._get_model_cls_(),
            params={
                "id": entity_id
            },
        )

    @classmethod
    def delete_entity_by_id(cls, entity_id: str, transaction: Transaction):
        cls._delete_entity_by_id(
            entity_cls=cls._get_entity_cls_(),
            entity_id=entity_id,
            transaction=transaction,
        )


class QueryCondition:
    """
    查询过滤条件
    """

    def __init__(self, column_name: str, operator: str, value: Any):
        self._column_name = column_name
        self._operator = operator
        self._value = value

    def build_sql_parameter(self) -> Tuple[str, tuple]:
        """
        构建查询的sql片段以及参数
        :return:
        """
        param_name = f"{self._column_name}{generate_random_string()}"
        sql_segment = f"{self._column_name} {self._operator} :{param_name}"
        params_segment = (param_name, self._value)
        return sql_segment, params_segment


class PaginationQueryBuilder(BasicRepository):
    """
    分页查询
    """

    def __init__(
            self,
            result_type: Type[GenericData],
            sql: str,
            search_columns: List[str],
            order_columns: Dict[str, Optional[str]],
            filter_columns: List[str] = None,
            params: Dict[str, Any] = None,
    ):
        """
        分页查询
        :param result_type: 返回数据类型
        :param sql: 查询sql，可以带参数，具体在get_query_result的时候将值传入
        :param search_columns: 列表，用于模糊搜索的字段名
        :param filter_columns: 列表，用于筛选的字段名
        :param order_columns: 字典，key是字段名，value是排序（asc/desc）
        """
        self._result_type = result_type
        self._sql = sql
        self._search_columns = search_columns
        self._filter_columns = filter_columns
        self._order_columns = order_columns
        self._query_para = params
        if params is None:
            self._query_para = {}

    def get_query_result(
            self,
            page_size: int,
            page_index: int,
            search_text: str = "",
            filter_option: Dict[str, Union[None, str, List[str]]] = None,
            draw: int = 1,
            extra_para_list: List[QueryCondition] = None,
    ) -> PaginationCarrier[GenericData]:

        """
        获取分页数据结果
        :param search_text:
        :param filter_option:
        :param page_size:
        :param page_index:
        :param extra_para_list:
        :param draw:
        :return:
        """

        def __build_query_conditions(
                query_filter_list: List[QueryCondition] = None,
        ) -> Tuple[str, Dict[str, Any]]:
            """
            根据query filter列表构建对应的sql和参数列表
            :param query_filter_list:
            :return:
            """
            __sql_segment = ""
            result_dict = {}
            if query_filter_list:
                for query_filter in query_filter_list:
                    _, extra_tuple = query_filter.build_sql_parameter()
                    result_dict[extra_tuple[0]] = extra_tuple[1]
            return __sql_segment, result_dict

        search_segment_list = [x.strip() for x in search_text.split(" ") if x != ""]
        search_sql, search_para_dict = self._build_search_condition(search_segment_list)
        filter_sql, filter_para_dict = self._build_filter_condition(filter_option)
        extra_sql, extra_para_dict = __build_query_conditions(extra_para_list)

        sql_segment = " {0} {1} {2} ".format(search_sql, filter_sql, extra_sql)
        execute_para_dict = search_para_dict | filter_para_dict | extra_para_dict
        return PaginationCarrier(
            search_text=search_text,
            total_count=self._total_count(),
            filter_count=self._filter_count(sql_segment, execute_para_dict),
            page_index=page_index,
            page_size=page_size,
            draw=draw,
            data=self._query_filter_data(
                page_size=page_size,
                page_index=page_index,
                sql_segment=sql_segment,
                params=execute_para_dict,
            ),
        )

    def _build_search_condition(
            self,
            search_segment: List[str],
    ) -> Tuple[str, Dict[str, Any]]:
        """
        根据检索字符串及参数字典构造过滤条件
        :param search_segment:
        :return:
        """
        filter_para = {}
        attach_segment = ""
        idx = 0
        for search_column in self._search_columns:
            for i, search_text in enumerate(search_segment):
                query_para_name = "search_text{0}".format(i)
                if idx == 0:
                    attach_segment += " {0} like :{1}".format(
                        search_column, query_para_name
                    )
                else:
                    attach_segment += " or {0} like :{1}".format(
                        search_column, query_para_name
                    )
                filter_para[query_para_name] = "%{0}%".format(search_text)
                idx += 1
        if attach_segment != "":
            attach_segment = " and ({0})".format(attach_segment)
        return attach_segment, filter_para

    def _build_filter_condition(
            self, filter_options: Dict[str, Union[None, str, List[str]]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        if self._filter_columns is None or filter_options is None:
            return "", {}

        filter_para = {}
        attach_segment = ""
        for column_name in self._filter_columns:
            if column_name in filter_options.keys() and filter_options[column_name] is not None:
                value = filter_options[column_name]
                filter_para_name = "filter_value_{0}".format(column_name)
                if isinstance(value, str):
                    attach_segment += " and {0}=:{1} ".format(
                        column_name, filter_para_name
                    )
                    filter_para[filter_para_name] = value
                else:
                    attach_segment += " and {0}=any(array[:{1}]) ".format(
                        column_name, filter_para_name
                    )
                    filter_para[filter_para_name] = value
        return attach_segment, filter_para

    def _total_count(self) -> int:
        """获取所有数据的数量"""
        return self._fetch_count(sql=self._sql, params=self._query_para)

    def _filter_count(self, sql_segment: str, params: Dict[str, Any]) -> int:
        sql_filter_count = """select * from ({0}) pqb where 1=1 {1} """.format(
            self._sql, sql_segment
        )
        execute_para_dict = self._query_para | params
        return self._fetch_count(sql_filter_count, execute_para_dict)

    def _query_filter_data(
            self, page_size: int, page_index: int, sql_segment: str, params: Dict[str, Any]
    ) -> List[GenericData]:
        sql_filter_data = """select * from ({0}) pqb where 1=1 {1} {2} {3}""".format(
            self._sql,
            sql_segment,
            self._build_order_conditions(),
            self._build_pagination_segment(page_size, page_index),
        )
        execute_para_dict = self._query_para | params
        return self._fetch_all(
            model_cls=self._result_type, sql=sql_filter_data, params=execute_para_dict
        )

    def _build_order_conditions(self) -> str:
        """
        构建排序sql
        :return:
        """
        if self._order_columns:
            order_segment = " order by "
            for order_column in self._order_columns:
                order_segment += order_column
                if self._order_columns[order_column]:
                    order_segment += " " + self._order_columns[order_column].strip()
                order_segment += ","
            order_segment = order_segment[:-1]
            return order_segment
        return ""
