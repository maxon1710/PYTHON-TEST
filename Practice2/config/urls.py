from __future__ import annotations

from .settings import get_env


# UI base URLs
GITHUB_BASE_URL = get_env("GITHUB_BASE_URL", "https://github.com/")
GITHUB_ABOUT_URL = get_env("GITHUB_ABOUT_URL", "https://github.com/about")
GITHUB_LOGIN_URL = get_env("GITHUB_LOGIN_URL", "https://github.com/login")
GITHUB_CAREERS_URL = get_env("GITHUB_CAREERS_URL", "https://github.careers/")
GITHUB_CICD_URL = get_env(
    "GITHUB_CICD_URL", "https://github.com/solutions/use-case/ci-cd"
)
GITHUB_RESOURCES_URL = get_env(
    "GITHUB_RESOURCES_URL", "https://resources.github.com/"
)

THE_INTERNET_LOGIN_URL = get_env(
    "THE_INTERNET_LOGIN_URL",
    "https://the-internet.herokuapp.com/login",
)

DUCKDUCKGO_URL = get_env("DUCKDUCKGO_URL", "https://duckduckgo.com/")

WIKI_MAIN_URL = get_env("WIKI_MAIN_URL", "https://ru.wikipedia.org/")
WIKI_MAIN_PAGE_URL = get_env(
    "WIKI_MAIN_PAGE_URL",
    "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0",
)
YANDEX_WEATHER_URL = get_env(
    "YANDEX_WEATHER_URL", "https://yandex.ru/pogoda/ru/saint-petersburg"
)

# API base URLs
RESTFUL_API_BASE_URL = get_env(
    "RESTFUL_API_BASE_URL", "https://api.restful-api.dev"
)
REQRES_BASE_URL = get_env("REQRES_BASE_URL", "https://reqres.in")
