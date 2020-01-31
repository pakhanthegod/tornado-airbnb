from __future__ import annotations

import decimal
import asyncio
import os
import datetime
from abc import ABC
from typing import TYPE_CHECKING

from aiopg.sa import create_engine
from sqlalchemy import Table
from sqlalchemy.sql.ddl import CreateTable, _CreateDropBase
from sqlalchemy.dialects.postgresql import dialect
from psycopg2.errors import DuplicateTable, DuplicateObject

from models.houses import house
from models.orders import order
from models.users import user, user_role


if TYPE_CHECKING:
    from aiopg.sa.connection import SAConnection
    from aiopg.sa.result import ResultProxy, RowProxy
    from aiopg.utils import _PoolContextManager


class DAO(ABC):
    """
    Data access object allows access to data of database
    """
    table: Table
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    database = os.environ.get('DB_NAME')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')

    async def get_engine(self) -> _PoolContextManager:
        engine: _PoolContextManager = await create_engine(
            user=self.user, database=self.database, host=self.host,
            port=self.port, password=self.password,
        )
        return engine

    async def create_table(self, connection: SAConnection):
        try:
            CreateTable(self.table).compile(dialect=dialect())
            await connection.execute(CreateTable(self.table))
        except DuplicateTable:
            print('>>> Diplicate table')  # TODO: logging

    async def insert(self, connection: SAConnection, **kwargs) -> int:
        result: ResultProxy = await connection.execute(
            self.table
            .insert()
            .values(**kwargs),
        )
        return (await result.first())[0]

    async def delete(self, connection: SAConnection, _id: int) -> None:
        await connection.execute(
            self.table
            .delete()
            .where(self.table.c.id == _id),
        )

    async def update(
        self, connection: SAConnection, _id: int, **kwargs,
    ) -> None:
        await connection.execute(
            self.table
            .update()
            .where(self.table.c.id == _id)
            .values(**kwargs),
        )

    async def selectById(self, connection: SAConnection, _id: int) -> RowProxy:
        result: ResultProxy = await connection.execute(
            self.table
            .select()
            .where(self.table.c.id == _id),
        )
        return await result.first()

    async def selectAll(self, connection: SAConnection) -> RowProxy:
        result: ResultProxy = await connection.execute(
            self.table
            .select(),
        )
        return await result.fetchall()


class HouseDAO(DAO):
    table = house

    async def insert(
        self,
        connection: SAConnection,
        user_id: int,
        description: str,
        address: str,
        max_person_number: int,
        price: decimal.Decimal,
        latitude: float = None,
        longitude: float = None,
    ):
        kwargs = {
            'user_id': user_id,
            'description': description,
            'address': address,
            'max_person_number': max_person_number,
            'price': price,
            'latitude': latitude,
            'longitude': longitude,
        }
        return await super().insert(connection, **kwargs)

    async def update(
        self,
        connection: SAConnection,
        _id: int,
        user_id: int = None,
        description: str = None,
        address: str = None,
        price: decimal.Decimal = None,
        latitude: float = None,
        longitude: float = None,
    ):
        kwargs = {
            'user_id': user_id,
            'description': description,
            'address': address,
            'price': price,
            'latitude': latitude,
            'longitude': longitude,
        }
        kwargs = {key: value for key, value in kwargs.items() if value}
        if any(kwargs.values()):
            await super().update(connection, _id, **kwargs)


class OrderDAO(DAO):
    table = order

    async def insert(
        self,
        connection: SAConnection,
        book_from: datetime.datetime,
        book_to: datetime.datetime,
        house_id: int,
        user_id: int,
        rating: int = None,
    ):
        kwargs = {
            'book_from': book_from,
            'book_to': book_to,
            'house_id': house_id,
            'rating': rating,
            'user_id': user_id,
        }
        return await super().insert(connection, **kwargs)

    async def update(
        self,
        connection: SAConnection,
        _id: int,
        book_from: datetime.datetime = None,
        book_to: datetime.datetime = None,
        rating: int = None,
        house_id: int = None,
        user_id: int = None,
    ):
        kwargs = {
            'book_from': book_from,
            'book_to': book_to,
            'rating': rating,
            'house_id': house_id,
            'user_id': user_id,
        }
        kwargs = {key: value for key, value in kwargs.items() if value}
        if any(kwargs.values()):
            await super().update(connection, _id, **kwargs)


class UserDAO(DAO):
    table = user

    async def insert(
        self,
        connection: SAConnection,
        first_name: str,
        last_name: str,
        email: str,
        password: bytes,
        birthdate: datetime.date,
        avatar: str = None,
    ):
        kwargs = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'avatar': avatar,
            'birthdate': birthdate,
        }
        return await super().insert(connection, **kwargs)

    async def update(
        self,
        connection: SAConnection,
        _id: int,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        password: bytes = None,
        avatar: str = None,
        birthday: datetime.date = None,
        role: str = None,
    ):
        kwargs = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'avatar': avatar,
            'birthday': birthday,
            'role': role,
        }
        kwargs = {key: value for key, value in kwargs.items() if value}
        if any(kwargs.values()):
            await super().update(connection, _id, **kwargs)


if __name__ == '__main__':
    class CreateEnumType(_CreateDropBase):
        """
        Helper class to create Enum type in database
        aiopg doesn't create it on its own.
        """
        __visit_name__ = 'create_enum_type'

    tasks = []

    async def create_tables():
        # CreateTable doesn't create type for Enum
        # so it need to be created manually
        try:
            house = HouseDAO()
            order = OrderDAO()
            user = UserDAO()
            engine = await user.get_engine()
            async with engine.acquire() as connection:
                await connection.execute(CreateEnumType(user_role))
        except DuplicateObject:
            print('>>> Duplicate enum type')  # TODO: change to logging
        for dao in (house, order, user):
            engine = await dao.get_engine()
            async with engine.acquire() as connection:
                await dao.create_table(connection)
    asyncio.run(create_tables())
