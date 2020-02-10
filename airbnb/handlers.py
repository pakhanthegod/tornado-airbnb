from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import bcrypt
import tornado


if TYPE_CHECKING:
    from daos import HouseDAO, UserDAO, DatabaseService


class UserListHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: UserDAO, database: DatabaseService) -> None:
        self.user: UserDAO = DAO(database)

    async def get(self) -> None:
        response = {}
        response_results = []

        results = await self.user.selectAll()
        for row in results:
            item = dict(row)
            if item['password']:
                item['password'] = item['password'].decode('utf-8')
            if item['birthdate']:
                item['birthdate'] = str(item['birthdate'])
            response_results.append(item)

        response['results'] = response_results

        self.write(response)
        self.set_status(200)

    async def post(self) -> None:
        response = {}
        data = tornado.escape.json_decode(self.request.body)

        password = data['password']
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes(password, encoding='utf-8'), salt)
        data['password'] = hashed

        date = data['birthdate']
        data['birthdate'] = datetime.datetime.strptime(date, '%d/%m/%Y')

        _id = await self.user.insert(**data)
        response['results'] = {'id': _id}

        self.write(response)
        self.set_status(200)


class UserDetailHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: UserDAO, database: DatabaseService) -> None:
        self.user: UserDAO = DAO(database)

    async def get(self, _id=None):
        print(_id)
        response = {}

        if not _id:
            response['errors'] = 'ID required'

            self.set_status(400)
        else:
            row = await self.user.selectById(_id)

            if row:
                row = dict(row)
                if row['password']:
                    row['password'] = row['password'].decode('utf-8')
                if row['birthdate']:
                    row['birthdate'] = str(row['birthdate'])
                response['results'] = row

                self.set_status(200)
            else:
                response['errors'] = 'User with that ID does not exist'

                self.set_status(400)

        self.write(response)


class HouseListHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: HouseDAO, database: DatabaseService) -> None:
        self.houses: HouseDAO = DAO(database)

    async def get(self) -> None:
        response = {}

        results = await self.houses.selectAll()
        response['results'] = [dict(row) for row in results]

        self.write(response)
        self.set_status(200)

    async def post(self) -> None:
        response = {}
        data = tornado.escape.json_decode(self.request.body)

        _id = await self.houses.insert(**data)
        response['results'] = {'id': _id}

        self.write(response)
        self.set_status(200)


class HouseDetailHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: HouseDAO, database: DatabaseService) -> None:
        self.houses: HouseDAO = DAO(database)

    async def get(self, _id=None):
        response = {}

        if not _id:
            response['errors'] = 'ID required'
            self.set_status(400)
        else:
            results = await self.houses.selectById(_id)
            response['results'] = dict(results)
            self.set_status(200)

        self.write(response)
