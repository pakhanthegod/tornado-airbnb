import pytest


@pytest.mark.asyncio
async def test_insert(user_dao):
    data = {
        'first_name': 'Foo',
        'last_name': 'Bar',
        'email': 'foo@example.com',
        'password': 'qwerty',
        'birthdate': '01/01/1990',
    }

    user_id = await user_dao.insert(**data)
    select = await user_dao.selectById(user_id)

    assert data['first_name'] == select[user_dao.table.c.first_name]


@pytest.mark.asyncio
async def test_delete(user_dao, user_object):
    await user_dao.delete(user_object[user_dao.table.c.id])
    select = await user_dao.selectById(user_object[user_dao.table.c.id])

    assert select is None


@pytest.mark.asyncio
async def test_selectById(user_dao, user_object):
    result = await user_dao.selectById(user_object[user_dao.table.c.id])

    assert user_object[user_dao.table.c.id] == result[0]


@pytest.mark.asyncio
async def test_update(user_dao, user_object):
    new_data = {
        '_id': user_object[user_dao.table.c.id],
        'last_name': 'Zar',
    }

    await user_dao.update(**new_data)
    select = await user_dao.selectById(user_object[user_dao.table.c.id])

    last_name = user_dao.table.c.last_name
    assert user_object[last_name] != select[last_name]


@pytest.mark.asyncio
async def test_selectAll(user_dao, user_object):
    result = await user_dao.selectAll()
    assert len(result) > 0
