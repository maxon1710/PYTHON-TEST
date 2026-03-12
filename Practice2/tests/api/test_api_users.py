import pytest

from api.clients.reqres_client import ReqresClient
from api.models.reqres import User

pytestmark = [pytest.mark.api, pytest.mark.external]


def test_users(reqres_client: ReqresClient):
    response = reqres_client.users(page=2)
    body = response.json()
    assert response.status_code == 200

    users = User(**body)
    assert len(users.data) == 6
