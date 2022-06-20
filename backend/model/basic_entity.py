"""
数据库基本类
"""
# standard library
from typing import Type

from sqlalchemy import Column, DateTime, Integer, String, func, text
from sqlalchemy.ext.declarative import declarative_base

from backend.utility.string_helper import generate_uuid_id

SqlAlchemyEntity = declarative_base()


class BasicEntity(SqlAlchemyEntity):
    """
    基本数据库类
    """
    __tablename__ = None
    __abstract__ = True
    id = Column(
        String(40),
        comment="id",
        # server_default=text("uuid_generate_v4()"),
        default=generate_uuid_id(),
        primary_key=True,
    )
    handler_category = Column(String(255), comment="更新者类型", nullable=False)
    handler_id = Column(String(255), comment="更新者", nullable=False)
    handled_at = Column(
        DateTime(timezone=True),
        comment="更新于",
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


BasicEntity = declarative_base(cls=BasicEntity)


class BasicHistoryEntity(SqlAlchemyEntity):
    """
    历史
    """

    __abstract__ = True
    history_id = Column(
        String(40),
        comment="history_id",
        # server_default=text("uuid_generate_v4()"),
        default=generate_uuid_id(),
        primary_key=True,
    )
    begin_at = Column(DateTime(timezone=True), comment="开始于", nullable=False)
    begin_transaction_id = Column(
        String(40), index=True, comment="begin_transaction_id"
    )
    end_at = Column(DateTime(timezone=True), comment="结束于")
    end_transaction_id = Column(String(40), index=True, comment="end_transaction_id")
    # 主表的对应字段
    id = Column(String(40), comment="id", nullable=False)
    version = Column(Integer, comment="版本", nullable=False)
    handler_category = Column(String(255), comment="更新者类型", nullable=False)
    handler_id = Column(String(255), comment="更新者", nullable=False)
    handled_at = Column(DateTime(timezone=True), comment="更新于", nullable=False)


BasicHistoryEntity = declarative_base(cls=BasicHistoryEntity)


class BasicVersionControlledEntity(BasicEntity):
    """
    有版本控制的实体基本类
    """

    __history_entity__: Type[BasicHistoryEntity] = None
    __abstract__ = True
    version = Column(Integer, comment="版本", server_default=text("1"), nullable=False)

    __mapper_args__ = {
        "version_id_col": version,
        "version_id_generator": lambda x: (x or 0) + 1,
    }


BasicVersionControlledEntity = declarative_base(cls=BasicVersionControlledEntity)
