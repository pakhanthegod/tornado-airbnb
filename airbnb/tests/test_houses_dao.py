import decimal

import pytest

from airbnb.dao import HouseDAO
from airbnb.models.houses import house


@pytest.mark.asyncio
async def test_insert(connection):
    data = dict(
        description='test_insertttt',
        address='test_insert',
        max_person_number='2',
        price=decimal.Decimal('3.14'),
        latitude=4.346346,
        longitude=3.65243634634,
    )
    hd = HouseDAO()

    house_id = await hd.insert(connection, **data)
    select = await hd.selectById(connection, house_id)

    assert data['description'] == select[hd.table.c.description]


@pytest.mark.asyncio
async def test_delete(connection, house_object):
    hd = HouseDAO()

    await hd.delete(connection, house_object[hd.table.c.id])
    select = await hd.selectById(connection, house_object[hd.table.c.id])

    assert select is None


@pytest.mark.asyncio
async def test_selectById(connection, house_object):
    hd = HouseDAO()

    result = await hd.selectById(connection, house_object[hd.table.c.id])

    assert house_object[hd.table.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(connection, house_object):
    hd = HouseDAO()
    new_data = dict(id=house_object[hd.table.c.id], description='new description for update')

    await hd.update(connection, **new_data)
    select = await hd.selectById(connection, house_object[hd.table.c.id])

    assert house_object[hd.table.c.description] != select[hd.table.c.description]

@pytest.mark.asyncio
async def test_selectAll(connection, house_object):
    hd = HouseDAO()

    result = await hd.selectAll(connection)

    assert len(result) > 0
