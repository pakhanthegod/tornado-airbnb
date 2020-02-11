import json


async def test_get_list(http_server_client):
    response = await http_server_client.fetch('/users')
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']


async def test_create(http_server_client):
    body = {
        'first_name': 'Bob',
        'last_name': 'Doe',
        'email': 'bob@example.com',
        'password': 'qwe',
        'birthdate': '02/02/1990',
    }
    body = json.dumps(body)

    response = await http_server_client.fetch('/users', method='POST', body=body)
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']['id']


async def test_get_detail(http_server_client, user_object, user_dao):
    response = await http_server_client.fetch(f'/users/{user_object[user_dao.table.c.id]}')
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']


async def test_update(http_server_client, user_object, user_dao):
    body = {
        'first_name': 'Test',
        'last_name': 'Update',
    }
    body = json.dumps(body)

    response = await http_server_client.fetch(
        f'/users/{user_object[user_dao.table.c.id]}', method='PATCH', body=body,
    )
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']['first_name'] != user_object[user_dao.table.c.first_name]
    assert response_body['results']['last_name'] != user_object[user_dao.table.c.last_name]
