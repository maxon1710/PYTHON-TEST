import requests
from dataclasses import dataclass
import pytest

@dataclass
class Meta:
    powered_by: str
    docs_url:str
    upgrade_url: str
    example_url:str
    variant: str
    message: str
    cta: Cta
    context: str

@dataclass
class LoginResponse:
    token: str
    _meta: Meta

@dataclass
class Cta:
    label: str
    url: str

@pytest.mark.api
@pytest.mark.external
def test_login():
    headers = {
        "x-api-key": "reqres_295059538bc34e0c970e90805bc9b0ef"
    }

    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    response = requests.post(
        "https://reqres.in/api/login",
        json=payload,
        headers=headers
    )

    assert response.status_code == 200
    print()
    print(response)

    body = response.json()
    login = LoginResponse(**body)
    cta = Cta(**body["_meta"]["cta"])

    assert login.token == "QpwL5tke4Pnpja7X4"
    print(login.token)
    assert cta.label == "See example app"
    print(cta.label)