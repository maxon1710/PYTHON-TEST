from __future__ import annotations

from typing import Any

from .base_client import BaseApiClient
from ..endpoints import reqres as endpoints


class ReqresClient(BaseApiClient):
    def login(self, email: str, password: str) -> Any:
        payload = {"email": email, "password": password}
        return self.request("POST", endpoints.LOGIN, json=payload)

    def users(self, page: int = 2) -> Any:
        return self.request("GET", endpoints.USERS, params={"page": page})

    def unknown(self) -> Any:
        return self.request("GET", endpoints.UNKNOWN)
