from sqlalchemy import (
    Boolean, Table, Column, Integer, 
    Float, Numeric, ForeignKey,
    MetaData, TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import TEXT

from models.users import user


metadata = MetaData()


house = Table(
    'houses',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),  # num
    Column('description', TEXT, nullable=False),  # str
    Column('address', TEXT, nullable=False),  # str
    Column('max_person_number', Integer, nullable=False),  # num
    Column('price', Numeric(10, 2), nullable=False),  # num
    Column('is_reviewed', Boolean, default=False, nullable=False),  # bool
    Column('reviewed', TIMESTAMP(timezone=True)),
    Column('latitude', Float),  # num
    Column('longitude', Float),  # num
    Column('rating', Integer, default=0, nullable=False),
    Column('user_id', Integer, ForeignKey(user.c.id)),  # num
)
