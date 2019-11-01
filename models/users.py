import enum

from sqlalchemy import (
    Table, Column, Integer, String,
    Boolean, Float, ForeignKey, Date,
    Enum, MetaData
)
from sqlalchemy.sql.ddl import CreateTable

from aiopg.sa import create_engine


metaData = MetaData()


class UserRole(enum.Enum):
    user = 'USER'
    staff = 'STAFF'


users = Table('users', metaData,
    Column('id', Integer, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('avatar', String),
    Column('date', Date),
    Column('role', Enum(UserRole)),
)


async def create_table(connection):
    await connection.execute('DROP TABLE IF EXISTS users')
    await connection.execute(CreateTable(users))
