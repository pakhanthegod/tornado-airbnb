import datetime

import pytest

from daos import OrderDAO


@pytest.mark.asyncio
async def test_insert(connection, user_object, house_object):
    data = {
        'book_from': datetime.datetime.utcnow() - datetime.timedelta(days=5),
        'book_to': datetime.datetime.utcnow() + datetime.timedelta(days=10),
        'house_id': house_object.id,
        'user_id': user_object.id,
    }
    order = OrderDAO()

    order_id = await order.insert(connection, **data)
    select = await order.selectById(connection, order_id)

    assert data['book_from'].astimezone(datetime.timezone.utc) == select[order.table.c.book_from]


@pytest.mark.asyncio
async def test_delete(connection, order_object):
    order = OrderDAO()

    await order.delete(connection, order_object[order.table.c.id])
    select = await order.selectById(connection, order_object[order.table.c.id])

    assert select is None


@pytest.mark.asyncio
async def test_selectById(connection, order_object):
    order = OrderDAO()

    result = await order.selectById(connection, order_object[order.table.c.id])

    assert order_object[order.table.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(connection, order_object):
    order = OrderDAO()
    new_data = {
        '_id': order_object[order.table.c.id],
        'book_from': datetime.datetime.utcnow() - datetime.timedelta(days=8),
    }

    await order.update(connection, **new_data)
    select = await order.selectById(connection, order_object[order.table.c.id])

    assert order_object[order.table.c.book_from].astimezone(datetime.timezone.utc) != select[order.table.c.book_from]


@pytest.mark.asyncio
async def test_selectAll(connection, order_object):
    order = OrderDAO()

    result = await order.selectAll(connection)

    assert len(result) > 0
