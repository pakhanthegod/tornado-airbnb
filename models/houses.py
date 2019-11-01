import decimal
import asyncio

from sqlalchemy import (
    Table, Column, Integer, String,
    Boolean, Float, Numeric, ForeignKey, MetaData
)
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.sql.ddl import CreateTable

from aiopg.sa import create_engine


metadata = MetaData()


houses = Table('houses', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),  # num
    # Column('user_id', Integer, ForeignKey('users.id')),  # num
    Column('description', TEXT),  # str
    Column('address', TEXT),  # str
    Column('max_person_number', Integer),  # num
    Column('price', Numeric(10,2)),  # num
    Column('is_reviewed', Boolean, default=False),  # bool
    Column('latitude', Float),  # num
    Column('longitude', Float),  # num
)


async def create_table(connection):
    await connection.execute('DROP TABLE IF EXISTS houses')
    await connection.execute(CreateTable(houses))


# async def insert_data(connection, **kwargs):
#     await connection.execute(houses.insert().values(**kwargs))
#     row = await (await connection.execute(houses.select())).first()

#     for name, val in kwargs.items():
#         print(row[name], val)
#         assert row[name] == val
