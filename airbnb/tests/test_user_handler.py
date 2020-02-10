import json
import asynctest
import pytest


async def test_get_list(http_server_client):
    response = await http_server_client.fetch('/users')
    assert response.code == 200

    body = json.loads(response.body)
    assert body['results']


async def test_create_item(http_server_client, mocker, connection):
    mock_dao_get_engine = mocker.patch('daos.UserDAO.get_engine')
    mock_dao_insert = mocker.patch('daos.UserDAO.insert')
    engine = asynctest.MagicMock()
    mock_dao_get_engine.return_value = engine
    _id = 1
    mock_dao_insert.return_value = _id
    response_body = {'id': _id}
    response_body = bytes(json.dumps(response_body), encoding='utf-8')
    body = {
        'first_name': 'Bob',
        'last_name': 'Doe',
        'email': 'bob@example.com',
        'password': 'qwe',
        'birthdate': '02/02/1990',
    }
    body = json.dumps(body)

    response = await http_server_client.fetch('/users', method='POST', body=body)

    assert response.code == 200
    assert response.body == response_body
    assert mock_dao_insert.called
    assert mock_dao_get_engine.called


async def test_create_item_async(http_server_client, mocker, connection):
    get_engine = mocker.patch('daos.UserDAO.get_engine')
    context = asynctest.MagicMock()
    context.__aenter__.return_value = connection
    engine = asynctest.MagicMock()
    engine.acquire.return_value = context
    get_engine.return_value = engine

    body = {
        'first_name': 'Bob',
        'last_name': 'Doe',
        'email': 'bob@example.com',
        'password': 'qwe',
        'birthdate': '02/02/1990',
    }
    body = json.dumps(body)

    response = await http_server_client.fetch('/users', method='POST', body=body)

    assert response.code == 200
