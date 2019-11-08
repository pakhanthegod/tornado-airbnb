import decimal

import pytest

from dbms import HouseDBMS
from models.houses import houses


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
    hd = HouseDBMS()

    house_id = await hd.insert(connection, **data)
    select = await hd.selectById(connection, house_id)

    assert data['description'] == select[hd.houses.c.description]


@pytest.mark.asyncio
async def test_delete(connection, house):
    hd = HouseDBMS()

    await hd.delete(connection, house[hd.houses.c.id])
    select = await hd.selectById(connection, house[hd.houses.c.id])

    assert select is None


@pytest.mark.asyncio
async def test_selectById(connection, house):
    hd = HouseDBMS()

    result = await hd.selectById(connection, house[hd.houses.c.id])

    assert house[hd.houses.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(connection, house):
    hd = HouseDBMS()
    new_data = dict(id=house[hd.houses.c.id], description='new description for update')

    await hd.update(connection, **new_data)
    select = await hd.selectById(connection, house[hd.houses.c.id])

    assert house[hd.houses.c.description] != select[hd.houses.c.description]
