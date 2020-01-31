from sqlalchemy import (
    Column, ForeignKey, Integer,
    MetaData, TIMESTAMP, Table,
)

from models.houses import house
from models.users import user


metaData = MetaData()

order = Table(
    'orders',
    metaData,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_from', TIMESTAMP(timezone=True), nullable=False),
    Column('book_to', TIMESTAMP(timezone=True), nullable=False),
    Column('rating', Integer),
    Column('house_id', Integer, ForeignKey(house.c.id), nullable=False),
    Column('user_id', Integer, ForeignKey(user.c.id), nullable=False),
)
