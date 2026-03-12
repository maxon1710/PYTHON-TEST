import pytest

from api.clients.reqres_client import ReqresClient
from api.clients.restful_api_client import RestfulApiClient
from config.settings import API_TIMEOUT_SEC, get_env
from config.urls import REQRES_BASE_URL, RESTFUL_API_BASE_URL


@pytest.fixture(scope="session")
def reqres_client():
    api_key = get_env("REQRES_API_KEY")
    if not api_key:
        pytest.skip("REQRES_API_KEY not set in .env")
    headers = {"x-api-key": api_key}
    return ReqresClient(
        base_url=REQRES_BASE_URL,
        headers=headers,
        timeout=API_TIMEOUT_SEC,
    )


@pytest.fixture(scope="session")
def restful_api_client():
    return RestfulApiClient(
        base_url=RESTFUL_API_BASE_URL,
        timeout=API_TIMEOUT_SEC,
    )
