import pytest

from api.clients.reqres_client import ReqresClient
from api.models.reqres import Cta, LoginResponse


@pytest.mark.api
@pytest.mark.external
def test_login(reqres_client: ReqresClient, reqres_creds: dict[str, str]):
    response = reqres_client.login(reqres_creds["email"], reqres_creds["password"])

    assert response.status_code == 200

    body = response.json()
    login = LoginResponse(**body)
    cta = Cta(**body["_meta"]["cta"])

    assert login.token == "QpwL5tke4Pnpja7X4"
    assert cta.label == "See example app"
