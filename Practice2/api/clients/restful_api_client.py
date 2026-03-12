from __future__ import annotations

from typing import Any

from .base_client import BaseApiClient
from ..endpoints import restful_api as endpoints


class RestfulApiClient(BaseApiClient):
    def create_object(self, payload: dict[str, Any]) -> Any:
        return self.request("POST", endpoints.OBJECTS, json=payload)

    def get_object(self, obj_id: str) -> Any:
        return self.request("GET", f"{endpoints.OBJECTS}/{obj_id}")

    def update_object(self, obj_id: str, payload: dict[str, Any]) -> Any:
        return self.request("PUT", f"{endpoints.OBJECTS}/{obj_id}", json=payload)

    def delete_object(self, obj_id: str) -> Any:
        return self.request("DELETE", f"{endpoints.OBJECTS}/{obj_id}")
