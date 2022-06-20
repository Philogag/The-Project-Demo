import json
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.ext.declarative import declarative_base

from backend.data.system_enum import EnumHandlerCategory
from backend.data.transaction import Transaction
from backend.factory import db
from backend.utility.enum_helper import enum_to_value_name_dict
from backend.utility.error_helper import InvalidClassAttrError
from backend.utility.string_helper import generate_uuid_id

SqlAlchemyEntity = declarative_base()


class UnitOfWorkEntity(SqlAlchemyEntity):
    """
    工作单元实体
    """

    __tablename__ = "unit_of_work"
    id = Column(String(40), comment="操作ID", primary_key=True)
    handler_category = Column(String(255), comment="操作人类型")
    handler_id = Column(String(40), comment="操作人ID")
    handled_begin_at = Column(
        DateTime(timezone=True),
        comment="操作起始时间",
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    handled_end_at = Column(DateTime(timezone=True), comment="操作结束时间", nullable=True)
    action = Column(String(255), comment="操作概述")
    action_params = Column(Text, comment="操作数据")


class SqlAlchemyUOW:
    entity: UnitOfWorkEntity
    transaction: Transaction

    def __init__(self, handler, action: str, action_params):
        if not hasattr(handler, "id"):
            raise InvalidClassAttrError(handler, "id")

        self.entity = UnitOfWorkEntity(
            id=generate_uuid_id(),
            handler_category=enum_to_value_name_dict(EnumHandlerCategory)[
                handler.__class__.__name__
            ],
            handler_id=handler.id,
            handled_begin_at=datetime.now(),
            action=action,
            action_params=json.dumps(action_params, ensure_ascii=False),
        )

        self.transaction = Transaction(
            id=self.entity.id,
            handler_category=self.entity.handler_category,
            handler_id=self.entity.handler_id,
            handled_at=self.entity.handled_begin_at,
        )

    def __enter__(self):
        self.entity.handled_begin_at = datetime.utcnow()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:  # 捕获异常时直接退出
            raise exc_val
        self.entity.handled_end_at = datetime.utcnow()
        db.session.add(self.entity)
        db.session.commit()
        return self
