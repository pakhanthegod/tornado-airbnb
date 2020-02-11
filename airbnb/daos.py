from __future__ import annotations

import decimal
import os
import datetime
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from aiopg.sa import create_engine
from sqlalchemy import Table

from models.houses import house
from models.orders import order
from models.users import user


if TYPE_CHECKING:
    from annotations import List
    from aiopg.sa.connection import SAConnection
    from aiopg.sa.result import RowProxy
    from aiopg.sa.engine import Engine


class DatabaseService(ABC):
    @abstractmethod
    def get_connection(self):
        pass


class AiopgService(DatabaseService):
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    database = os.environ.get('DB_NAME')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    _engine = None

    async def get_engine(self) -> Engine:
        if not self._engine:
            self._engine = await create_engine(
                user=self.user, database=self.database, host=self.host,
                port=self.port, password=self.password,
            )
        return self._engine

    async def get_connection(self) -> SAConnection:
        engine = await self.get_engine()
        connection = await engine.acquire()
        return connection


class DAO(ABC):
    """
    Data access object allows access to data of database
    """
    table: Table

    def __init__(self, database: DatabaseService) -> None:
        self.db = database()

    async def insert(self, **kwargs) -> int:
        connection = await self.db.get_connection()
        result = await connection.execute(
            self.table
            .insert()
            .values(**kwargs)  # noqa
        )
        row = await result.first()
        await connection.close()
        return row['id']

    async def delete(self, _id: int) -> int:
        connection = await self.db.get_connection()
        result = await connection.execute(
            self.table
            .delete()
            .where(self.table.c.id == _id)  # noqa
        )
        row_count = result.rowcount
        await connection.close()
        return row_count

    async def update(self, _id: int, **kwargs) -> int:
        connection = await self.db.get_connection()
        result = await connection.execute(
            self.table
            .update()
            .where(self.table.c.id == _id)
            .values(**kwargs)  # noqa
        )
        row_count = result.rowcount
        await connection.close()
        return row_count

    async def selectById(self, _id: int) -> RowProxy:
        connection = await self.db.get_connection()
        result = await connection.execute(
            self.table
            .select()
            .where(self.table.c.id == _id),
        )
        row = await result.first()
        await connection.close()
        return row

    async def selectAll(self) -> List[RowProxy]:
        connection = await self.db.get_connection()
        result = await connection.execute(
            self.table
            .select(),
        )
        rows = await result.fetchall()
        await connection.close()
        return rows


class HouseDAO(DAO):
    table = house

    async def insert(
        self,
        user_id: int,
        description: str,
        address: str,
        max_person_number: int,
        price: decimal.Decimal,
        latitude: float = None,
        longitude: float = None,
    ) -> int:
        kwargs = {
            'user_id': user_id,
            'description': description,
            'address': address,
            'max_person_number': max_person_number,
            'price': price,
            'latitude': latitude,
            'longitude': longitude,
        }
        return await super().insert(**kwargs)

    async def update(
        self,
        _id: int,
        user_id: int = None,
        description: str = None,
        address: str = None,
        price: decimal.Decimal = None,
        latitude: float = None,
        longitude: float = None,
    ) -> int:
        kwargs = {
            'user_id': user_id,
            'description': description,
            'address': address,
            'price': price,
            'latitude': latitude,
            'longitude': longitude,
        }
        kwargs = {key: value for key, value in kwargs.items() if value}
        if kwargs:
            return await super().update(_id, **kwargs)


class OrderDAO(DAO):
    table = order

    async def insert(
        self,
        book_from: datetime.datetime,
        book_to: datetime.datetime,
        house_id: int,
        user_id: int,
        rating: int = None,
    ) -> int:
        kwargs = {
            'book_from': book_from,
            'book_to': book_to,
            'house_id': house_id,
            'rating': rating,
            'user_id': user_id,
        }
        return await super().insert(**kwargs)

    async def update(
        self,
        _id: int,
        book_from: datetime.datetime = None,
        book_to: datetime.datetime = None,
        rating: int = None,
        house_id: int = None,
        user_id: int = None,
    ) -> int:
        kwargs = {
            'book_from': book_from,
            'book_to': book_to,
            'rating': rating,
            'house_id': house_id,
            'user_id': user_id,
        }
        kwargs = {key: value for key, value in kwargs.items() if value}
        if kwargs:
            return await super().update(_id, **kwargs)


class UserDAO(DAO):
    table = user

    async def insert(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: bytes,
        birthdate: datetime.date,
        avatar: str = None,
    ) -> int:
        kwargs = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'avatar': avatar,
            'birthdate': birthdate,
        }
        return await super().insert(**kwargs)

    async def update(
        self,
        _id: int,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        password: bytes = None,
        avatar: str = None,
        birthday: datetime.date = None,
        role: str = None,
    ) -> int:
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
        if kwargs:
            return await super().update(_id, **kwargs)
