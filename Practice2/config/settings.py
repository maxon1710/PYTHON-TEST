from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


def get_env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


ENV = get_env("ENV", "local")

HEADLESS = get_env("HEADLESS", "false").lower() == "true"

UI_TIMEOUT_MS = int(get_env("UI_TIMEOUT_MS", "7000"))
API_TIMEOUT_SEC = int(get_env("API_TIMEOUT_SEC", "10"))
