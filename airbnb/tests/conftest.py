import os
import decimal

import pytest
from aiopg.sa import create_engine

from airbnb.dao import HouseDAO
from airbnb.models.houses import house


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
        port=PORT
    ) as engine:
        async with engine.acquire() as connection:
            transaction = await connection.begin()
            yield connection
            await transaction.rollback()


@pytest.fixture(scope='function')
async def house_object(connection):
    test_house_data = dict(
        description='test_insertttt',
        address='test_insert',
        max_person_number='2',
        price=decimal.Decimal('3.14'),
        latitude=4.346346,
        longitude=3.65243634634,
    )
    house_dbms = HouseDAO()
    test_house_id = await house_dbms.insert(connection, **test_house_data)
    return await house_dbms.selectById(connection, test_house_id)
