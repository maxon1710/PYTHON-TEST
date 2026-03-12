import pytest

from api.clients.reqres_client import ReqresClient
from api.models.reqres import Color, UnknownResponse

pytestmark = [pytest.mark.api, pytest.mark.external]


def test_unknown_response(reqres_client: ReqresClient):
    response = reqres_client.unknown()

    assert response.status_code == 200

    body = response.json()
    UnknownResponse(**body)
    colors = [Color(**item) for item in body["data"]]
    for color in colors:
        assert color.year >= 2000
        assert color.name != ""
