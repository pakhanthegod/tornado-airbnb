import decimal
import asyncio
import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from aiopg.sa.connection import SAConnection
from aiopg.sa.result import ResultProxy, RowProxy
from aiopg.sa import create_engine
from sqlalchemy import Table
from sqlalchemy.sql.ddl import CreateTable, _CreateDropBase
from sqlalchemy.dialects.postgresql import dialect
from psycopg2.errors import DuplicateTable, DuplicateObject

from airbnb.models.houses import house
from airbnb.models.orders import order
from airbnb.models.users import user, user_role


if TYPE_CHECKING:
    from aiopg.sa.result import ResultProxy, RowProxy
    from aiopg.sa.connection import SAConnection
    from aiopg.utils import _PoolContextManager


class DAO(ABC):
    """
    Data access object allows access to data of database
    """
    table: Table
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    database = os.environ.get('DB_NAME')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')

    def __init__(self):
        super().__init__()

    async def get_engine(self) -> '_PoolContextManager':
        engine: '_PoolContextManager' = await create_engine(
            user=self.user, database=self.database, host=self.host,
            port=self.port, password=self.password
        )
        return engine

    async def create_table(self, connection: 'SAConnection'):
        try:
            print(CreateTable(self.table).compile(dialect=dialect()))
            await connection.execute(CreateTable(self.table))
        except DuplicateTable:
            print('>>> Diplicate table')  # TODO: logging

    async def insert(self, connection: 'SAConnection', **kwargs) -> int:
        result: 'ResultProxy' = await connection.execute(self.table.insert().values(**kwargs))
        return (await result.first())[0]

    async def delete(self, connection: 'SAConnection', id: int, **kwargs) -> None:
        await connection.execute(self.table.delete().where(self.table.c.id==id))

    async def update(self, connection: 'SAConnection', id: int, **kwargs) -> None:
        await connection.execute(self.table.update().where(self.table.c.id==id).values(**kwargs))

    async def selectById(self, connection: 'SAConnection', id: int, **kwargs) -> 'RowProxy':
        result: 'ResultProxy' = await connection.execute(self.table.select().where(self.table.c.id==id))
        return await result.first()

    async def selectAll(self, connection: 'SAConnection', **kwargs) -> 'RowProxy':
        result: 'ResultProxy' = await connection.execute(self.table.select())
        return await result.fetchall()


class HouseDAO(DAO):
    table = house

    def __init__(self):
        super().__init__()


class OrderDAO(DAO):
    table = order

    def __init__(self):
        super().__init__()


class UserDAO(DAO):
    table = user

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    class CreateEnumType(_CreateDropBase):
        """
        Helper class to create Enum type in database
        aiopg doesn't create it on its own.
        """
        __visit_name__ = "create_enum_type"


    hd = HouseDAO()
    od = OrderDAO()
    ud = UserDAO()
    tasks = []
    async def create_tables():
        try:  # CreateTable doesn't create type for Enum so it need to be created manually
            ud = UserDAO()
            engine = await ud.get_engine()
            async with engine.acquire() as connection:
                print(CreateEnumType(user_role).compile(dialect=dialect()))
                await connection.execute(CreateEnumType(user_role))
        except DuplicateObject:
            print('>>> Duplicate enum type')  # TODO: change to logging
        for dao in (ud, hd, od):
            engine = await dao.get_engine()
            async with engine.acquire() as connection:
                await dao.create_table(connection)
    asyncio.run(create_tables())
