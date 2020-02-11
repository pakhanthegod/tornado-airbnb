import os
import datetime
import decimal
import asyncio

import pytest

from app import make_app
from daos import HouseDAO, UserDAO, OrderDAO, AiopgService
from handlers import (
    HouseDetailHandler,
    HouseListHandler,
    UserDetailHandler,
    UserListHandler,
    OrderListHandler,
    OrderDetailHandler,
)


USER = os.environ.get('TEST_DB_USER')
PASSWORD = os.environ.get('TEST_DB_PASSWORD')
DATABASE = os.environ.get('TEST_DB_NAME')
HOST = os.environ.get('TEST_DB_HOST')
PORT = os.environ.get('TEST_DB_PORT')


@pytest.yield_fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class AiopgTestService(AiopgService):
    user = USER
    password = PASSWORD
    database = DATABASE
    host = HOST
    port = PORT


urls = [
    (r'/houses', HouseListHandler, {'DAO': HouseDAO, 'database': AiopgTestService}),
    (r'/houses/(?P<_id>\w+)', HouseDetailHandler, {'DAO': HouseDAO, 'database': AiopgTestService}),
    (r'/users', UserListHandler, {'DAO': UserDAO, 'database': AiopgTestService}),
    (r'/users/(?P<_id>\w+)', UserDetailHandler, {'DAO': UserDAO, 'database': AiopgTestService}),
    (r'/orders', OrderListHandler, {'DAO': OrderDAO, 'database': AiopgTestService}),
    (r'/orders/(?P<_id>\w+)', OrderDetailHandler, {'DAO': OrderDAO, 'database': AiopgTestService}),
]


@pytest.fixture
def app():
    return make_app(urls)


@pytest.fixture()
async def user_dao():
    return UserDAO(AiopgTestService)


@pytest.fixture()
async def order_dao():
    return OrderDAO(AiopgTestService)


@pytest.fixture()
async def house_dao():
    return HouseDAO(AiopgTestService)


@pytest.fixture(scope='function')
async def user_object(user_dao):
    test_user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'qwe',
        'birthdate': '01/01/1990',
    }
    test_user_id = await user_dao.insert(**test_user_data)
    return await user_dao.selectById(test_user_id)


@pytest.fixture(scope='function')
async def house_object(house_dao, user_object):
    test_house_data = {
        'description': 'A cool house',
        'address': 'USA, some st.',
        'max_person_number': 2,
        'price': decimal.Decimal('3.14'),
        'latitude': 55.721696,
        'longitude': 37.579362,
        'user_id': user_object.id,
    }
    test_house_id = await house_dao.insert(**test_house_data)
    return await house_dao.selectById(test_house_id)


@pytest.fixture(scope='function')
async def order_object(order_dao, user_object, house_object):
    test_order_data = {
        'book_from': datetime.datetime.utcnow() - datetime.timedelta(days=5),
        'book_to': datetime.datetime.utcnow() + datetime.timedelta(days=10),
        'house_id': house_object.id,
        'user_id': user_object.id,
    }
    test_order_id = await order_dao.insert(**test_order_data)
    return await order_dao.selectById(test_order_id)
