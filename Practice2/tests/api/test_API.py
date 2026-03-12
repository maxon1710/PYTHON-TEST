import pytest

from api.clients.restful_api_client import RestfulApiClient

pytestmark = [pytest.mark.api, pytest.mark.external]


@pytest.fixture()
def obj_id(restful_api_client: RestfulApiClient):
    payload = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB",
        },
    }
    response = restful_api_client.create_object(payload)
    body = response.json()
    yield body["id"]
    restful_api_client.delete_object(body["id"])


def test_create_object(restful_api_client: RestfulApiClient):
    payload = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB",
        },
    }

    response = restful_api_client.create_object(payload)
    body = response.json()
    assert body["name"] == payload["name"] == "Apple MacBook Pro 16"


def test_get_object(restful_api_client: RestfulApiClient, obj_id: str):
    response = restful_api_client.get_object(obj_id)
    json_object = response.json()
    assert json_object["id"] == obj_id


def test_put_object(restful_api_client: RestfulApiClient, obj_id: str):
    payload = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2025,
            "price": 3333.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB",
            "color": "silver",
        },
    }

    fix_body = restful_api_client.update_object(obj_id, payload).json()
    obj_price = fix_body["data"]["price"]
    assert fix_body["data"]["price"] == obj_price


def test_delete_object(restful_api_client: RestfulApiClient, obj_id: str):
    obj_delete = restful_api_client.delete_object(obj_id)
    assert obj_delete.status_code == 200
    response = restful_api_client.get_object(obj_id)
    assert response.status_code == 404
