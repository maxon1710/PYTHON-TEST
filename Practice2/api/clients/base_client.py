from __future__ import annotations

from typing import Any

import requests


class BaseApiClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout: int | float = 10,
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        merged_headers = {**self.headers, **headers}
        return requests.request(
            method=method,
            url=url,
            headers=merged_headers,
            timeout=self.timeout,
            **kwargs,
        )
