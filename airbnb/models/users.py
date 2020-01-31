from sqlalchemy import (
    Table, Column, Integer, String,
    Date, MetaData,
)
from sqlalchemy.dialects.postgresql import ENUM, BYTEA


metaData = MetaData()

user_role = ENUM(
    'customer', 'staff', create_type=True, name='user_role', metadata=metaData,
)

user = Table(
    'users',
    metaData,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('password', BYTEA, nullable=False),
    Column('avatar', String),
    Column('birthdate', Date, nullable=False),
    Column('role', user_role, default=user_role.enums[0], nullable=False),
)
