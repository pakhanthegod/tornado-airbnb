import json
import decimal


async def test_get_list(http_server_client):
    response = await http_server_client.fetch('/houses')
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']


async def test_create(http_server_client, user_object):
    body = {
        'description': 'A cool house',
        'address': 'USA, some st.',
        'max_person_number': 2,
        'price': str(decimal.Decimal('3.14')),
        'latitude': 55.721696,
        'longitude': 37.579362,
        'user_id': user_object.id,
    }
    body = json.dumps(body)

    response = await http_server_client.fetch('/houses', method='POST', body=body)
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']['id']


async def test_get_detail(http_server_client, house_object, house_dao):
    response = await http_server_client.fetch(f'/houses/{house_object[house_dao.table.c.id]}')
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']


async def test_update(http_server_client, house_object, house_dao):
    body = {
        'description': 'Test',
        'address': 'Address',
    }
    body = json.dumps(body)

    response = await http_server_client.fetch(
        f'/houses/{house_object[house_dao.table.c.id]}', method='PATCH', body=body,
    )
    response_body = json.loads(response.body)

    assert response.code == 200
    assert response_body['results']['description'] != house_object[house_dao.table.c.description]
    assert response_body['results']['address'] != house_object[house_dao.table.c.address]
