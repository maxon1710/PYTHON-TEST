import pytest

from config.settings import get_env


def _require_env(name: str) -> str:
    value = get_env(name)
    if not value:
        pytest.skip(f"{name} not set in .env")
    return value


@pytest.fixture(scope="session")
def github_creds():
    user = _require_env("GH_USER")
    password = _require_env("GH_PASS")
    return {"user": user, "password": password}


@pytest.fixture(scope="session")
def testsite_creds():
    user = _require_env("TEST_USER")
    password = _require_env("TEST_PASS")
    return {"user": user, "password": password}


@pytest.fixture(scope="session")
def reqres_creds():
    email = _require_env("REQRES_EMAIL")
    password = _require_env("REQRES_PASSWORD")
    return {"email": email, "password": password}
