from sqlalchemy import (
    Table, Column, Integer, String,
    Boolean, Float, DateTime, ForeignKey, MetaData
)
from sqlalchemy.sql.ddl import CreateTable

from aiopg.sa import create_engine


metaData = MetaData()

orders = Table('orders', metaData,
    Column('id', Integer, primary_key=True),
    Column('house_id', Integer, ForeignKey('houses.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('date_from', DateTime, nullable=False),
    Column('date_to', DateTime, nullable=False),
    Column('rating', Integer),
)


async def create_table(connection):
    await connection.execute('DROP TABLE IF EXISTS orders')
    await connection.execute(CreateTable(orders))
