from sqlalchemy import (
    Table, Column, Integer, String,
    Boolean, Float, DateTime, ForeignKey, MetaData
)
from sqlalchemy.sql.ddl import CreateTable
from aiopg.sa import create_engine

from airbnb.models.houses import house
from airbnb.models.users import user


metaData = MetaData()

order = Table('orders', metaData,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('house_id', Integer, ForeignKey(house.c.id), nullable=False),
    Column('user_id', Integer, ForeignKey(user.c.id), nullable=False),
    Column('date_from', DateTime(timezone=True), nullable=False),
    Column('date_to', DateTime(timezone=True), nullable=False),
    Column('rating', Integer),
)
