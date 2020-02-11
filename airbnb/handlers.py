from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
import decimal

import bcrypt
import tornado
from dateutil import parser


if TYPE_CHECKING:
    from daos import HouseDAO, UserDAO, OrderDAO, DatabaseService


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
        response = {}

        if not _id:
            response['errors'] = 'ID required'

            self.set_status(400)
        else:
            row = await self.user.selectById(_id)

            if row:
                row = dict(row)
                if 'password' in row:
                    row['password'] = row['password'].decode('utf-8')
                if 'birthdate' in row:
                    row['birthdate'] = str(row['birthdate'])
                response['results'] = row

                self.set_status(200)
            else:
                response['errors'] = 'User with that ID does not exist'

                self.set_status(400)

        self.write(response)

    async def patch(self, _id=None) -> None:
        response = {}

        if not _id:
            response['errors'] = 'ID required'

            self.set_status(400)
        else:
            data = tornado.escape.json_decode(self.request.body)
            results = await self.user.update(_id, **data)
            if not results:
                response['errors'] = 'Update error'

                self.set_status(400)
            else:
                row = await self.user.selectById(_id)

                if row:
                    row = dict(row)
                    if 'password' in row:
                        row['password'] = row['password'].decode('utf-8')
                    if 'birthdate' in row:
                        row['birthdate'] = str(row['birthdate'])
                    response['results'] = row

                self.set_status(200)
        self.write(response)


class HouseListHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: HouseDAO, database: DatabaseService) -> None:
        self.house: HouseDAO = DAO(database)

    async def get(self) -> None:
        response = {}
        response_results = []

        results = await self.house.selectAll()
        for row in results:
            item = dict(row)
            if item['price']:
                item['price'] = str(item['price'])
            response_results.append(item)

        response['results'] = response_results
        self.write(response)
        self.set_status(200)

    async def post(self) -> None:
        response = {}
        data = tornado.escape.json_decode(self.request.body)
        data['price'] = decimal.Decimal(data['price'])

        _id = await self.house.insert(**data)
        response['results'] = {'id': _id}

        self.write(response)
        self.set_status(200)


class HouseDetailHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: HouseDAO, database: DatabaseService) -> None:
        self.house: HouseDAO = DAO(database)

    async def get(self, _id=None):
        response = {}

        if not _id:
            response['errors'] = 'ID required'
            self.set_status(400)
        else:
            row = await self.house.selectById(_id)

            if row:
                row = dict(row)
                if 'price' in row:
                    row['price'] = str(row['price'])
                response['results'] = row

            self.set_status(200)

        self.write(response)

    async def patch(self, _id=None) -> None:
        response = {}

        if not _id:
            response['errors'] = 'ID required'

            self.set_status(400)
        else:
            data = tornado.escape.json_decode(self.request.body)
            results = await self.house.update(_id, **data)
            if not results:
                response['errors'] = 'Update error'

                self.set_status(400)
            else:
                row = await self.house.selectById(_id)

                if row:
                    row = dict(row)
                    if 'price' in row:
                        row['price'] = str(row['price'])
                    response['results'] = row

                self.set_status(200)

        self.write(response)


class OrderListHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: OrderDAO, database: DatabaseService) -> None:
        self.order: OrderDAO = DAO(database)

    async def get(self) -> None:
        response = {}
        response_results = []

        results = await self.order.selectAll()
        for row in results:
            item = dict(row)
            if item['book_from']:
                item['book_from'] = item['book_from'].isoformat()
            if item['book_to']:
                item['book_to'] = item['book_to'].isoformat()
            response_results.append(item)

        response['results'] = response_results
        self.write(response)
        self.set_status(200)

    async def post(self) -> None:
        response = {}
        data = tornado.escape.json_decode(self.request.body)
        data['book_from'] = parser.parse(data['book_from'])
        data['book_to'] = parser.parse(data['book_to'])

        _id = await self.order.insert(**data)
        response['results'] = {'id': _id}

        self.write(response)
        self.set_status(200)


class OrderDetailHandler(tornado.web.RequestHandler):
    def initialize(self, DAO: OrderDAO, database: DatabaseService) -> None:
        self.order: OrderDAO = DAO(database)

    async def get(self, _id=None):
        response = {}

        if not _id:
            response['errors'] = 'ID required'
            self.set_status(400)
        else:
            row = await self.order.selectById(_id)

            if row:
                row = dict(row)
                if 'book_from' in row:
                    row['book_from'] = row['book_from'].isoformat()
                if 'book_to' in row:
                    row['book_to'] = row['book_to'].isoformat()
                response['results'] = row

            self.set_status(200)

        self.write(response)

    async def patch(self, _id=None) -> None:
        response = {}

        if not _id:
            response['errors'] = 'ID required'

            self.set_status(400)
        else:
            data = tornado.escape.json_decode(self.request.body)
            if 'book_from' in data:
                data['book_from'] = parser.parse(data['book_from'])
            if 'book_to' in data:
                data['book_to'] = parser.parse(data['book_to'])

            results = await self.order.update(_id, **data)
            if not results:
                response['errors'] = 'Update error'

                self.set_status(400)
            else:
                row = await self.order.selectById(_id)

                if row:
                    row = dict(row)
                    if 'book_from' in row:
                        row['book_from'] = row['book_from'].isoformat()
                    if 'book_to' in row:
                        row['book_to'] = row['book_to'].isoformat()
                    response['results'] = row

                self.set_status(200)

        self.write(response)
