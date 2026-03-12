from __future__ import annotations

from pydantic import BaseModel


class Cta(BaseModel):
    label: str
    url: str


class Meta(BaseModel):
    powered_by: str
    docs_url: str
    upgrade_url: str
    example_url: str
    variant: str
    message: str
    cta: Cta
    context: str


class LoginResponse(BaseModel):
    token: str
    _meta: Meta


class Data(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class Support(BaseModel):
    url: str
    text: str


class User(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[Data]
    support: Support
    _meta: Meta | None = None


class Color(BaseModel):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str


class UnknownResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[Color]
