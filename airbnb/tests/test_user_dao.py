import pytest

from daos import UserDAO


@pytest.mark.asyncio
async def test_insert(connection):
    data = {
        'first_name': 'Foo',
        'last_name': 'Bar',
        'email': 'foo@example.com',
        'password': 'qwerty',
        'birthdate': '01/01/1990',
    }
    user = UserDAO()

    user_id = await user.insert(connection, **data)
    select = await user.selectById(connection, user_id)

    assert data['first_name'] == select[user.table.c.first_name]


@pytest.mark.asyncio
async def test_delete(connection, user_object):
    user = UserDAO()

    await user.delete(connection, user_object[user.table.c.id])
    select = await user.selectById(connection, user_object[user.table.c.id])

    assert select is None


@pytest.mark.asyncio
async def test_selectById(connection, user_object):
    user = UserDAO()

    result = await user.selectById(connection, user_object[user.table.c.id])

    assert user_object[user.table.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(connection, user_object):
    user = UserDAO()
    new_data = {
        '_id': user_object[user.table.c.id],
        'last_name': 'Zar',
    }

    await user.update(connection, **new_data)
    select = await user.selectById(connection, user_object[user.table.c.id])

    last_name = user.table.c.last_name
    assert user_object[last_name] != select[last_name]


@pytest.mark.asyncio
async def test_selectAll(connection, user_object):
    user = UserDAO()

    result = await user.selectAll(connection)

    assert len(result) > 0
