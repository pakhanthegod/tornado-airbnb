import json


async def test_get_list(http_server_client):
    response = await http_server_client.fetch('/orders')
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']


async def test_create(http_server_client, user_object, house_object):
    body = {
        'book_from': '2020-01-11T12:56:46.902Z',
        'book_to': '2020-06-11T12:56:46.902Z',
        'house_id': house_object.id,
        'user_id': user_object.id,
    }
    body = json.dumps(body)

    response = await http_server_client.fetch('/orders', method='POST', body=body)
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']['id']


async def test_get_detail(http_server_client, order_object, order_dao):
    response = await http_server_client.fetch(f'/orders/{order_object[order_dao.table.c.id]}')
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']


async def test_update(http_server_client, order_object, order_dao):
    body = {
        'book_to': '2021-04-11T12:56:46.902Z',
    }
    body = json.dumps(body)

    response = await http_server_client.fetch(
        f'/orders/{order_object[order_dao.table.c.id]}', method='PATCH', body=body,
    )
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']['book_to'] != order_object[order_dao.table.c.book_to]
