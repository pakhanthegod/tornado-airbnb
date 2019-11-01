import decimal
import asyncio

from aiopg.sa import create_engine

from models.houses import houses
from models.orders import orders
from models.users import users


class DBMS:
    connection = None
    user='pakhan'
    database='airbnb'
    host='0.0.0.0'
    port='54320'
    password='pakhan'

    def __init__(self):
        pass

    async def get_engine(self):
        engine = await create_engine(
            user=self.user, database=self.database, host=self.host,
            port=self.port, password=self.password
        )
        return engine

    async def insert(self):
        pass


class HouseDBMS(DBMS):
    def __init__(self):
        super().__init__()
        self.houses = houses
    
    async def insert(self, **kwargs):
        engine = await self.get_engine()
        async with engine:
            async with engine.acquire() as connection:
                await connection.execute(self.houses.insert().values(**kwargs))

    async def delete(self, id):
        engine = await self.get_engine()
        async with engine:
            async with engine.acquire() as connection:
                await connection.execute(self.houses.delete().where(houses.id==id))

    async def update(self, id, **kwargs):
        engine = await self.get_engine()
        async with engine:
            async with engine.acquire() as connection:
                await connection.execute(self.houses.update().where(houses.id==id).values(**kwargs))


if __name__ == '__main__':
    dbms = DBMS()
    asyncio.run(dbms.insert())