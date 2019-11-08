import decimal
import asyncio
import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from aiopg.sa.connection import SAConnection
from aiopg.sa.result import ResultProxy, RowProxy
from aiopg.sa import create_engine

from models.houses import houses
from models.orders import orders
from models.users import users


if TYPE_CHECKING:
    from aiopg.sa.result import ResultProxy, RowProxy
    from aiopg.sa.connection import SAConnection
    from aiopg.utils import _PoolContextManager


class DBMS(ABC):
    connection = None
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    database = os.environ.get('DB_NAME')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')

    def __init__(self):
        pass

    async def get_engine(self) -> '_PoolContextManager':
        engine: '_PoolContextManager' = await create_engine(
            user=self.user, database=self.database, host=self.host,
            port=self.port, password=self.password
        )
        return engine

    @abstractmethod
    async def insert(self):
        pass

    @abstractmethod
    async def delete(self):
        pass

    @abstractmethod
    async def update(self):
        pass


class HouseDBMS(DBMS):
    def __init__(self):
        super().__init__()
        self.houses = houses
    
    async def insert(self, connection: 'SAConnection', **kwargs) -> int:
        result: 'ResultProxy' = await connection.execute(self.houses.insert().values(**kwargs))
        return (await result.first())[0]

    async def delete(self, connection: 'SAConnection', id: int, **kwargs) -> None:
        await connection.execute(self.houses.delete().where(houses.c.id==id))

    async def update(self, connection: 'SAConnection', id: int, **kwargs) -> None:
        await connection.execute(self.houses.update().where(self.houses.c.id==id).values(**kwargs))

    async def selectById(self, connection: 'SAConnection', id: int, **kwargs) -> 'RowProxy':
        result: 'ResultProxy' = await connection.execute(self.houses.select().where(self.houses.c.id==id))
        return await result.first()

    async def selectAll(self, connection: 'SAConnection', **kwargs) -> 'RowProxy':
        result: 'ResultProxy' = await connection.execute(self.houese.select())
        return await result.fetchall()
