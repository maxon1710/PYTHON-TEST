import requests
import pytest

pytestmark = [pytest.mark.api, pytest.mark.external]

@pytest.fixture()
def obj_id():
   payload = {
      "name": "Apple MacBook Pro 16",
      "data": {
         "year": 2019,
         "price": 1849.99,
         "CPU model": "Intel Core i9",
         "Hard disk size": "1 TB"
      }
   }
   response = requests.post("https://api.restful-api.dev/objects", json=payload).json()
   yield response['id']
   requests.delete(f"https://api.restful-api.dev/objects/{response['id']}")


def test_create_object():
   payload = {
      "name": "Apple MacBook Pro 16",
      "data": {
         "year": 2019,
         "price": 1849.99,
         "CPU model": "Intel Core i9",
         "Hard disk size": "1 TB"
      }
   }

   response = requests.post("https://api.restful-api.dev/objects", json=payload).json()
   assert response["name"] == payload["name"] == "Apple MacBook Pro 16"
   print()
   print(response)
   print(response["name"])

def test_get_object(obj_id):
   response = requests.get(f"https://api.restful-api.dev/objects/{obj_id}")
   json_object = response.json()
   assert json_object["id"] == obj_id
   print()
   print(json_object)
   print(f"Запрошенный ID =" , json_object['id'])



def test_put_object(obj_id):
   payload = {
      "name": "Apple MacBook Pro 16",
      "data": {
         "year": 2025,
         "price": 3333.99,
         "CPU model": "Intel Core i9",
         "Hard disk size": "1 TB",
         "color": "silver"
      }
   }

   fix_body = requests.put(f"https://api.restful-api.dev/objects/{obj_id}", json=payload).json()
   obj_price = fix_body["data"]["price"]
   assert fix_body['data']["price"] == obj_price
   print()
   print(f'ID измененного объекта: ',obj_id)
   print(f"Измененная цена = ",fix_body['data']['price'])

def test_delete_object(obj_id):
   obj_delete = requests.delete(f"https://api.restful-api.dev/objects/{obj_id}")
   assert obj_delete.status_code == 200
   response = requests.get(f"https://api.restful-api.dev/objects/{obj_id}")
   assert response.status_code == 404
   print()

   print(f"Ваш обьект был удален: {obj_id}")