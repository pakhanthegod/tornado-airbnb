import decimal

import pytest

from daos import HouseDAO


@pytest.mark.asyncio
async def test_insert(connection, user_object):
    data = {
        'description': 'test_insertttt',
        'address': 'test_insert',
        'max_person_number': 2,
        'price': decimal.Decimal('3.14'),
        'latitude': 4.346346,
        'longitude': 3.65243634634,
        'user_id': user_object.id,
    }
    house = HouseDAO()

    house_id = await house.insert(connection, **data)
    select = await house.selectById(connection, house_id)

    assert data['description'] == select[house.table.c.description]


@pytest.mark.asyncio
async def test_delete(connection, house_object):
    house = HouseDAO()

    await house.delete(connection, house_object[house.table.c.id])
    select = await house.selectById(connection, house_object[house.table.c.id])

    assert select is None


@pytest.mark.asyncio
async def test_selectById(connection, house_object):
    house = HouseDAO()

    result = await house.selectById(connection, house_object[house.table.c.id])

    assert house_object[house.table.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(connection, house_object):
    house = HouseDAO()
    new_data = {
        '_id': house_object[house.table.c.id],
        'description': 'new description for update',
    }

    await house.update(connection, **new_data)
    select = await house.selectById(connection, house_object[house.table.c.id])

    assert house_object[house.table.c.description] != select[house.table.c.description]


@pytest.mark.asyncio
async def test_selectAll(connection, house_object):
    house = HouseDAO()

    result = await house.selectAll(connection)

    assert len(result) > 0
