import decimal
import asyncio

from sqlalchemy import (
    Table, Column, Integer, String,
    Boolean, Float, Numeric, ForeignKey, MetaData
)
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.sql.ddl import CreateTable
from aiopg.sa import create_engine

from airbnb.models.users import user


metadata = MetaData()


house = Table('houses', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),  # num
    Column('user_id', Integer, ForeignKey(user.c.id)),  # num
    Column('description', TEXT),  # str
    Column('address', TEXT),  # str
    Column('max_person_number', Integer),  # num
    Column('price', Numeric(10,2)),  # num
    Column('is_reviewed', Boolean, default=False),  # bool
    Column('latitude', Float),  # num
    Column('longitude', Float),  # num
)
