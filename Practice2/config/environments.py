from __future__ import annotations

from .settings import ENV


def current_environment() -> str:
    return ENV
