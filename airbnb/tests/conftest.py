import os
import datetime
import decimal

import pytest
from aiopg.sa import create_engine

from daos import HouseDAO, UserDAO, OrderDAO


USER = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE = os.environ.get('DB_NAME')
HOST = os.environ.get('DB_HOST')
PORT = os.environ.get('DB_PORT')


@pytest.fixture(scope='function')
async def connection():
    async with create_engine(
        user=USER, password=PASSWORD,
        database=DATABASE, host=HOST,
        port=PORT,
    ) as engine:
        async with engine.acquire() as connection:
            transaction = await connection.begin()
            yield connection
            await transaction.rollback()


@pytest.fixture(scope='function')
async def user_object(connection):
    test_user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'qwe',
        'birthdate': '01/01/1990',
    }
    user_dao = UserDAO()
    test_user_id = await user_dao.insert(connection, **test_user_data)
    return await user_dao.selectById(connection, test_user_id)


@pytest.fixture(scope='function')
async def house_object(connection, user_object):
    test_house_data = {
        'description': 'A cool house',
        'address': 'USA, some st.',
        'max_person_number': 2,
        'price': decimal.Decimal('3.14'),
        'latitude': 55.721696,
        'longitude': 37.579362,
        'user_id': user_object.id,
    }
    house_dao = HouseDAO()
    test_house_id = await house_dao.insert(connection, **test_house_data)
    return await house_dao.selectById(connection, test_house_id)


@pytest.fixture(scope='function')
async def order_object(connection, user_object, house_object):
    test_order_data = {
        'book_from': datetime.datetime.utcnow() - datetime.timedelta(days=5),
        'book_to': datetime.datetime.utcnow() + datetime.timedelta(days=10),
        'house_id': house_object.id,
        'user_id': user_object.id,
    }
    order_dao = OrderDAO()
    test_order_id = await order_dao.insert(connection, **test_order_data)
    return await order_dao.selectById(connection, test_order_id)
