import datetime

import pytest


@pytest.mark.asyncio
async def test_insert(order_dao, user_object, house_object):
    data = {
        'book_from': datetime.datetime.utcnow() - datetime.timedelta(days=5),
        'book_to': datetime.datetime.utcnow() + datetime.timedelta(days=10),
        'house_id': house_object.id,
        'user_id': user_object.id,
    }

    order_id = await order_dao.insert(**data)
    select = await order_dao.selectById(order_id)

    assert data['book_from'].astimezone(datetime.timezone.utc) == select[order_dao.table.c.book_from]


@pytest.mark.asyncio
async def test_delete(order_dao, order_object):
    await order_dao.delete(order_object[order_dao.table.c.id])
    select = await order_dao.selectById(order_object[order_dao.table.c.id])

    assert select is None


@pytest.mark.asyncio
async def test_selectById(order_dao, order_object):
    result = await order_dao.selectById(order_object[order_dao.table.c.id])

    assert order_object[order_dao.table.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(order_dao, order_object):
    new_data = {
        '_id': order_object[order_dao.table.c.id],
        'book_from': datetime.datetime.utcnow() - datetime.timedelta(days=8),
    }

    await order_dao.update(**new_data)
    select = await order_dao.selectById(order_object[order_dao.table.c.id])

    book_from = order_dao.table.c.book_from
    assert order_object[book_from].astimezone(datetime.timezone.utc) != select[book_from]


@pytest.mark.asyncio
async def test_selectAll(order_dao, order_object):
    result = await order_dao.selectAll()
    assert len(result) > 0
