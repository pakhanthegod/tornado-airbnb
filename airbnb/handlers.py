from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import bcrypt
import tornado


if TYPE_CHECKING:
    from daos import HouseDAO, UserDAO


class HouseListHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: HouseDAO) -> None:
        self.houses = DAO()

    async def get(self) -> None:
        response = {}
        engine = await self.houses.get_engine()
        async with engine.acquire() as connection:
            results = await self.houses.selectAll(connection)
            response['results'] = [dict(row) for row in results]
        self.write(response)
        self.set_status(200)

    async def post(self) -> None:
        data = tornado.escape.json_decode(self.request.body)
        engine = await self.houses.get_engine()
        async with engine.acquire() as connection:
            await self.houses.insert(connection, **data)


class UserListHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: UserDAO) -> None:
        self.user = DAO()

    async def get(self) -> None:
        response = {}
        engine = await self.user.get_engine()
        async with engine.acquire() as connection:
            results = await self.user.selectAll(connection)
            response['results'] = []
            for row in results:
                item = dict(row)
                if item['password']:
                    item['password'] = item['password'].decode('utf-8')
                if item['birthdate']:
                    item['birthdate'] = str(item['birthdate'])
                response['results'].append(item)
        self.write(response)
        self.set_status(200)

    async def post(self) -> None:
        data = tornado.escape.json_decode(self.request.body)
        engine = await self.user.get_engine()
        async with engine.acquire() as connection:
            password = data['password']
            date = data['birthdate']
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(bytes(password, encoding='utf-8'), salt)
            data['password'] = hashed
            data['birthdate'] = datetime.datetime.strptime(date, '%d/%m/%Y')
            await self.user.insert(connection, **data)


class HouseDetailHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: HouseDAO) -> None:
        self.houses = DAO()

    async def get(self, id=None):
        response = {}
        if not id:
            response['errors'] = 'ID required'
        else:
            engine = await self.houses.get_engine()
            async with engine.acquire() as connection:
                results = await self.houses.selectById(connection, id)
                response['results'] = dict(results)
        self.write(response)
        self.set_status(200)
