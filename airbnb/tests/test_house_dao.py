import decimal

import pytest


@pytest.mark.asyncio
async def test_insert(house_dao, user_object):
    data = {
        'description': 'test_insertttt',
        'address': 'test_insert',
        'max_person_number': 2,
        'price': decimal.Decimal('3.14'),
        'latitude': 4.346346,
        'longitude': 3.65243634634,
        'user_id': user_object.id,
    }

    house_id = await house_dao.insert(**data)
    select = await house_dao.selectById(house_id)

    assert data['description'] == select[house_dao.table.c.description]


@pytest.mark.asyncio
async def test_delete(house_dao, house_object):
    row_count = await house_dao.delete(house_object[house_dao.table.c.id])
    select = await house_dao.selectById(house_object[house_dao.table.c.id])

    assert row_count == 1
    assert select is None


@pytest.mark.asyncio
async def test_selectById(house_dao, house_object):
    result = await house_dao.selectById(house_object[house_dao.table.c.id])

    assert house_object[house_dao.table.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(house_dao, house_object):
    new_data = {
        '_id': house_object[house_dao.table.c.id],
        'description': 'new description for update',
    }

    row_count = await house_dao.update(**new_data)
    select = await house_dao.selectById(house_object[house_dao.table.c.id])

    assert row_count == 1
    assert house_object[house_dao.table.c.description] != select[house_dao.table.c.description]


@pytest.mark.asyncio
async def test_selectAll(house_dao, house_object):
    result = await house_dao.selectAll()
    assert len(result) > 0
