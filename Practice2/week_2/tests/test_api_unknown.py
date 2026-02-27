import requests
from pydantic import BaseModel

class UnknownResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[Color]

class Color(BaseModel):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str

class Support(BaseModel):
    url: str
    text: str


def test_unknown_response():
    headers = {
        "x-api-key": "reqres_295059538bc34e0c970e90805bc9b0ef"
    }

    response = requests.request(
        method="GET",
    url="https://reqres.in/api/unknow",
    headers=headers,)

    assert response.status_code == 200
    print(response)

    body = response.json()
    colors = [Color(**item) for item in body["data"]]
    for color in colors:
        assert color.year >= 2000
        assert color.name != ""
        print(color.year)
        print(color.name)
