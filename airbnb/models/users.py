from sqlalchemy import (
    Table, Column, Integer, String,
    Boolean, Float, ForeignKey, Date,
    Enum, MetaData
)
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.dialects.postgresql import ENUM

from aiopg.sa import create_engine


metaData = MetaData()

user_role = ENUM('user', 'staff', create_type=True, name='user_role', metadata=metaData)

user = Table('users', metaData,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('avatar', String),
    Column('date', Date),
    Column('role', user_role, default=user_role.enums[0], nullable=False),
)
