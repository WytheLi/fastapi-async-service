#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker, Session

from settings import settings

# 创建引擎（数据库连接的工厂，它还保留连接池内的连接以便快速重用）
engine = create_engine(
    settings.PGSQL_URL,
    # echo=True,  # 打印SQL语句
    pool_pre_ping=True,
    pool_size=50,  # 连接池大小
    pool_recycle=1800,  # 连接回收时间
    max_overflow=50,  # 允许的最大连接池溢出数量
    pool_timeout=30,
    # echo=True,  # 打印SQL语句
    future=True,  # 使用异步模式
    # connect_args={"check_same_thread": False},  # SQLite数据库专用
    # json_serializer=json.dumps,  # 自定义JSON序列化器
    # json_deserializer=json.loads,  # 自定义JSON反序列
)

sync_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_sync_session() -> Session:
    with sync_session() as session:
        try:
            yield session
        except Exception as ex:
            session.rollback()
            raise ex
        else:
            session.commit()
        finally:
            session.close()

# # 创建监听器，将SQL输出到控制台，便于调试。（event事件监听器，暂时不支持异步引擎连接数据库对象）
# @event.listens_for(async_engine, "before_cursor_execute", retval=True)
# def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     conn.info.setdefault('query_start_time', []).append(time.time())
#     print("Start Query: %s", statement)

# @event.listens_for(async_engine, "after_cursor_execute", retval=True)
# def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     total = time.time() - conn.info['query_start_time'].pop(-1)
#     print("Query Complete: %s, Time: %f", statement, total)
