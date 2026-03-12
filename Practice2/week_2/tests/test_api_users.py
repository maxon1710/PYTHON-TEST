
import pytest

pytestmark = [pytest.mark.api, pytest.mark.external]
import requests
from pydantic import BaseModel

class User(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[Data]
    support: Support
    _meta: Meta

class Data(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class Support(BaseModel):
    url: str
    text: str

class Meta(BaseModel):
    powered_by: str
    docs_url: str
    upgrade_url: str
    example_url: str
    variant: str
    message: str
    cta: Cta
    context: str

class Cta(BaseModel):
    label: str
    url: str


def test_users():
    headers = {
        "x-api-key": "reqres_295059538bc34e0c970e90805bc9b0ef"
    }

    response = requests.request(
        method="GET", url="https://reqres.in/api/users?page=2",
        headers=headers
    )

    body = response.json()
    assert response.status_code == 200

    users = User(**body)
    assert len(users.data) == 6
    print([user.id for user in users.data])