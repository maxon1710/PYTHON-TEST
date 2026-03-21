import random
import time
from playwright.sync_api import sync_playwright

# ─────────────────────────────────────────────
# ТАБЛИЦА ТРАНСЛИТЕРАЦИИ
# Используется для перевода русских имён в латиницу при генерации email
# Пример: "Екатерина" → "ekaterina", "Романова" → "romanova"
# ─────────────────────────────────────────────
TRANSLIT = {
    'а': 'a',  'б': 'b',  'в': 'v',  'г': 'g',  'д': 'd',
    'е': 'e',  'ё': 'e',  'ж': 'zh', 'з': 'z',  'и': 'i',
    'й': 'y',  'к': 'k',  'л': 'l',  'м': 'm',  'н': 'n',
    'о': 'o',  'п': 'p',  'р': 'r',  'с': 's',  'т': 't',
    'у': 'u',  'ф': 'f',  'х': 'kh', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'sch','ъ': '',   'ы': 'y',  'ь': '',
    'э': 'e',  'ю': 'yu', 'я': 'ya',
}

# ─────────────────────────────────────────────
# ПУЛ ИМЁН — 100 штук
# ─────────────────────────────────────────────
NAMES = [
    # Мужские
    "Александр Петров",   "Дмитрий Иванов",    "Сергей Смирнов",    "Андрей Кузнецов",
    "Михаил Попов",       "Алексей Соколов",   "Николай Лебедев",   "Владимир Козлов",
    "Артём Новиков",      "Павел Морозов",      "Иван Волков",       "Денис Зайцев",
    "Евгений Соловьёв",   "Максим Васильев",   "Антон Павлов",      "Роман Семёнов",
    "Кирилл Голубев",     "Илья Виноградов",   "Олег Богданов",     "Виктор Орлов",
    "Тимур Абрамов",      "Руслан Григорьев",  "Станислав Фролов",  "Вячеслав Осипов",
    "Константин Беляев",  "Геннадий Медведев", "Борис Никифоров",   "Леонид Тихонов",
    "Валентин Сидоров",   "Игорь Макаров",     "Анатолий Щербаков", "Юрий Захаров",
    "Фёдор Калинин",      "Глеб Миронов",      "Даниил Коновалов",  "Матвей Лазарев",
    "Степан Ершов",       "Егор Никитин",      "Тихон Воробьёв",    "Лев Громов",
    "Марк Ковалёв",       "Вадим Куликов",     "Эдуард Соловьёв",   "Виталий Крылов",
    "Пётр Зиновьев",      "Ярослав Панфилов",  "Савелий Рыбаков",   "Арсений Комаров",
    "Богдан Устинов",     "Захар Королёв",
    # Женские
    "Анна Михайлова",     "Елена Фёдорова",    "Наталья Морозова",  "Ольга Алексеева",
    "Татьяна Лебедева",   "Марина Степанова",  "Ирина Яковлева",    "Светлана Андреева",
    "Юлия Сергеева",      "Екатерина Романова","Людмила Захарова",  "Надежда Ильина",
    "Валерия Орлова",     "Дарья Соловьёва",   "Вера Кузьмина",     "Полина Никитина",
    "Оксана Титова",      "Галина Фомина",      "Зинаида Жукова",    "Тамара Зайцева",
    "Алина Воронова",     "Кристина Исакова",  "Виктория Панова",   "Диана Сорокина",
    "Карина Белова",      "Ксения Гусева",     "Снежана Фёдорова",  "Регина Тарасова",
    "Маргарита Кириллова","Лариса Борисова",   "Нина Савельева",    "Валентина Логинова",
    "Тамара Никитина",    "Жанна Крылова",     "Антонина Лобанова", "Людмила Соколова",
    "Ангелина Мельникова","Евгения Воробьёва", "Василиса Куликова", "Таисия Громова",
    "Злата Панфилова",    "Милана Рыбакова",   "Варвара Комарова",  "Есения Устинова",
    "Аделина Королёва",   "Злата Зиновьева",   "Лилия Ершова",      "Элина Коновалова",
    "Инна Мироновая",     "Рита Калинина",
]

# ─────────────────────────────────────────────
# КОДЫ ОПЕРАТОРОВ РФ
# МТС: 910-919 | Мегафон: 920-929 | Билайн: 960-969
# Теле2: 900-908 | Ростелеком: 950-953 | Yota: 977-979
# ─────────────────────────────────────────────
OPERATOR_CODES = [
    "910", "911", "912", "913", "914", "915", "916", "917", "918", "919",
    "920", "921", "922", "923", "924", "925", "926", "927", "928", "929",
    "960", "961", "962", "963", "964", "965", "966", "967", "968", "969",
    "900", "901", "902", "904", "905", "906", "908",
    "950", "951", "952", "953",
    "977", "978", "979",
]

# ─────────────────────────────────────────────
# ДОМЕНЫ EMAIL
# ─────────────────────────────────────────────
DOMAINS = ["gmail.com", "yandex.ru", "mail.ru"]

# ─────────────────────────────────────────────
# ШАБЛОНЫ EMAIL
# fn = имя на латинице, ln = фамилия на латинице
# ─────────────────────────────────────────────
EMAIL_TEMPLATES = [
    lambda fn, ln: f"{ln}.{fn[:3]}",
    lambda fn, ln: f"{fn[:4]}{ln[:4]}",
    lambda fn, ln: f"{fn}.{ln}",
    lambda fn, ln: f"{ln}{random.randint(1970, 2000)}",
    lambda fn, ln: f"{fn[:2]}{ln}",
    lambda fn, ln: f"{fn}_{ln[:5]}",
]

# ─────────────────────────────────────────────
# КАРТИНЫ — база данных "автор" + "название"
# Из них генерируется случайный формат запроса
# ─────────────────────────────────────────────
PICTURES_DATA = [
    # Импрессионизм
    ("Моне", "Кувшинки"),
    ("Моне", "Впечатление. Восходящее солнце"),
    ("Ренуар", "Бал в Мулен де ла Галетт"),
    ("Дега", "Голубые танцовщицы"),
    ("Дега", "Репетиция балета"),
    ("Писсарро", "Бульвар Монмартр"),
    # Постимпрессионизм
    ("Ван Гог", "Звёздная ночь"),
    ("Ван Гог", "Подсолнухи"),
    ("Ван Гог", "Ирисы"),
    ("Гоген", "Откуда мы пришли"),
    ("Сезанн", "Большие купальщицы"),
    ("Климт", "Поцелуй"),
    ("Климт", "Юдифь"),
    # Русская живопись
    ("Айвазовский", "Девятый вал"),
    ("Айвазовский", "Чёрное море"),
    ("Шишкин", "Утро в сосновом лесу"),
    ("Шишкин", "Рожь"),
    ("Левитан", "Золотая осень"),
    ("Левитан", "Над вечным покоем"),
    ("Репин", "Бурлаки на Волге"),
    ("Репин", "Иван Грозный и сын его Иван"),
    ("Суриков", "Боярыня Морозова"),
    ("Суриков", "Утро стрелецкой казни"),
    ("Врубель", "Демон сидящий"),
    ("Серов", "Девочка с персиками"),
    ("Куинджи", "Лунная ночь на Днепре"),
    ("Васнецов", "Богатыри"),
    ("Крамской", "Неизвестная"),
    ("Перов", "Охотники на привале"),
    ("Саврасов", "Грачи прилетели"),
    ("Брюллов", "Последний день Помпеи"),
    ("Брюллов", "Всадница"),
    ("Кустодиев", "Купчиха за чаем"),
    ("Поленов", "Московский дворик"),
    # Старые мастера
    ("Рембрандт", "Ночной дозор"),
    ("Рембрандт", "Возвращение блудного сына"),
    ("Вермеер", "Девушка с жемчужной серёжкой"),
    ("Рафаэль", "Сикстинская Мадонна"),
    ("Леонардо да Винчи", "Мона Лиза"),
    ("Боттичелли", "Рождение Венеры"),
    ("Веласкес", "Менины"),
    ("Рубенс", "Три грации"),
    ("Брейгель", "Охотники на снегу"),
    # Модернизм
    ("Дали", "Постоянство памяти"),
    ("Магритт", "Сын человеческий"),
    ("Мунк", "Крик"),
    ("Матисс", "Танец"),
    ("Кандинский", "Композиция VIII"),
    ("Пикассо", "Герника"),
]

# Шаблоны — как реальный человек напишет запрос
# author = "Моне", title = "Кувшинки"
PICTURE_TEMPLATES = [
    lambda a, t: f"{a} - {t}",                          # Моне - Кувшинки
    lambda a, t: f"{a} «{t}»",                          # Моне «Кувшинки»
    lambda a, t: f"{t} ({a})",                          # Кувшинки (Моне)
    lambda a, t: f"{t}",                                # Кувшинки
    lambda a, t: f"копия картины {a} {t}",              # копия картины Моне Кувшинки
    lambda a, t: f"{a}, {t}",                           # Моне, Кувшинки
    lambda a, t: f"картина {t} художника {a}",          # картина Кувшинки художника Моне
    lambda a, t: f'"{t}" {a}',                          # "Кувшинки" Моне
    lambda a, t: f"{a} / {t}",                          # Моне / Кувшинки
    lambda a, t: f"хочу копию {t}",                     # хочу копию Кувшинки
]


# ─────────────────────────────────────────────
# ПРОФИЛИ БРАУЗЕРА
# Каждый запуск выбирает случайный профиль — разный агент, экран, ОС
# Примеры:
#   Chrome 134 / Windows / 1920x1080
#   Firefox 124 / Mac    / 1440x900
#   Safari      / Mac    / 1366x768
#   Edge        / Windows / 2560x1440
# ─────────────────────────────────────────────
BROWSER_PROFILES = [
    {
        "name": "Chrome 134 / Windows / Full HD",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "viewport": {"width": 1920, "height": 1080},
        "device_scale_factor": 1,
    },
    {
        "name": "Chrome 133 / Windows / HD",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "viewport": {"width": 1366, "height": 768},
        "device_scale_factor": 1,
    },
    {
        "name": "Chrome 134 / Mac / 1440x900",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "viewport": {"width": 1440, "height": 900},
        "device_scale_factor": 2,  # Retina дисплей Mac
    },
    {
        "name": "Chrome 133 / Mac / 1280x800",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "viewport": {"width": 1280, "height": 800},
        "device_scale_factor": 2,
    },
    {
        "name": "Firefox 124 / Windows / Full HD",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "viewport": {"width": 1920, "height": 1080},
        "device_scale_factor": 1,
    },
    {
        "name": "Firefox 124 / Mac / 1440x900",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
        "viewport": {"width": 1440, "height": 900},
        "device_scale_factor": 2,
    },
    {
        "name": "Edge / Windows / 2K",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "viewport": {"width": 2560, "height": 1440},
        "device_scale_factor": 1,
    },
    {
        "name": "Safari / Mac / 1680x1050",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        "viewport": {"width": 1680, "height": 1050},
        "device_scale_factor": 2,
    },
]

# ─────────────────────────────────────────────
# ЛОКАЛИ И ВРЕМЕННЫЕ ЗОНЫ
# Имитируем пользователей из разных городов России
# Пример: ("ru-RU", "Europe/Moscow") → Москва
# ─────────────────────────────────────────────
LOCALES_TZ = [
    ("ru-RU", "Europe/Moscow"),        # Москва / МСК
    ("ru-RU", "Europe/Amsterdam"),     # Калининград (UTC+2, как Амстердам)
    ("ru-RU", "Asia/Yekaterinburg"),   # Екатеринбург
    ("ru-RU", "Asia/Novosibirsk"),     # Новосибирск
    ("ru-RU", "Asia/Krasnoyarsk"),     # Красноярск
    ("ru-RU", "Europe/Samara"),        # Самара
]

# ─────────────────────────────────────────────
# COLOR SCHEME
# 90% light (как большинство пользователей), 10% dark
# ─────────────────────────────────────────────
COLOR_SCHEMES = ["light", "light", "light", "light", "light",
                 "light", "light", "light", "light", "dark"]


# ─────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────

def translit(text):
    """
    Переводит русский текст в латиницу по таблице TRANSLIT.
    Пример: translit("Екатерина") → "ekaterina"
    """
    return ''.join(TRANSLIT.get(ch.lower(), ch) for ch in text)


def random_name():
    """
    Возвращает случайное полное имя из пула NAMES.
    Пример: "Екатерина Романова"
    """
    return random.choice(NAMES)


def random_phone():
    """
    Генерирует номер с реальным кодом оператора РФ.
    Примеры: "+79211234567", "8 921 123 45 67", "+7 (921) 123-45-67"
    """
    code = random.choice(OPERATOR_CODES)
    number = random.randint(1000000, 9999999)
    n = str(number)
    formats = [
        f"+7{code}{n}",
        f"8{code}{n}",
        f"+7 ({code}) {n[:3]}-{n[3:5]}-{n[5:]}",
        f"8 {code} {n[:3]} {n[3:5]} {n[5:]}",
    ]
    return random.choice(formats)


def random_email(full_name):
    """
    Строит email из переданного русского имени через транслитерацию.
    Пример: "Екатерина Романова" → "romanova.eka47@yandex.ru"
    """
    first, last = full_name.split()
    fn = translit(first)
    ln = translit(last)
    template = random.choice(EMAIL_TEMPLATES)
    local = template(fn, ln)
    if random.random() > 0.6:
        local += str(random.randint(1, 99))
    return f"{local}@{random.choice(DOMAINS)}"


def random_picture():
    """
    Выбирает случайную картину и случайный формат записи.
    Примеры результата:
      Моне - Кувшинки
      картина Звёздная ночь художника Ван Гог
      хочу копию Богатыри
      "Девятый вал" Айвазовский
    """
    author, title = random.choice(PICTURES_DATA)
    template = random.choice(PICTURE_TEMPLATES)
    return template(author, title)


def human_type(locator, text):
    """
    Печатает текст посимвольно с задержкой 90-200ms.
    Иногда (15% символов) делает паузу 0.3-0.8s — имитация раздумья.
    """
    for char in text:
        locator.type(char, delay=random.randint(90, 200))
        if random.random() > 0.85:
            time.sleep(random.uniform(0.3, 0.8))


# ─────────────────────────────────────────────
# ОСНОВНОЙ СКРИПТ
# ─────────────────────────────────────────────

with sync_playwright() as p:

    # ── ВЫБОР СЛУЧАЙНОГО ПРОФИЛЯ ─────────────────────────────────────────
    # Каждый запуск = новый случайный профиль браузера
    profile     = random.choice(BROWSER_PROFILES)
    locale, tz  = random.choice(LOCALES_TZ)
    color_scheme = random.choice(COLOR_SCHEMES)

    print("🚀 Запуск браузера...")
    print("\n🎭 ПРОФИЛЬ ЭТОГО ЗАПУСКА:")
    print(f"   Браузер:    {profile['name']}")
    print(f"   Viewport:   {profile['viewport']['width']}x{profile['viewport']['height']}")
    print(f"   Scale:      {profile['device_scale_factor']}x {'(Retina)' if profile['device_scale_factor'] == 2 else ''}")
    print(f"   Локаль/TZ:  {locale} / {tz}")
    print(f"   Тема:       {color_scheme}")
    print(f"   UA:         {profile['user_agent'][:65]}...")

    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        viewport=profile["viewport"],
        user_agent=profile["user_agent"],
        device_scale_factor=profile["device_scale_factor"],
        locale=locale,
        timezone_id=tz,
        color_scheme=color_scheme,
    )
    page = context.new_page()

    captured_request = {}


    def handle_request(request):
        if "price-order.php" in request.url:
            captured_request["url"] = request.url
            captured_request["post_data"] = request.post_data


    def handle_response(response):
        if "price-order.php" in response.url:
            captured_request["status"] = response.status
            try:
                captured_request["response"] = response.json()
            except:
                captured_request["response"] = response.text()


    page.on("request", handle_request)
    page.on("response", handle_response)


    # Скрываем признаки автоматизации:
    # navigator.webdriver = undefined → у обычного Chrome это false/undefined
    # chrome.runtime = {}             → у Playwright этого объекта нет по умолчанию
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.navigator.chrome = { runtime: {} };
    """)

    print("\n🌐 Открываем сайт...")
    page.goto("https://theheritage.ru/", wait_until="domcontentloaded")

    # ── АВТОМАТИЧЕСКИЙ КЛИК ПО КАПЧЕ ────────────────────────────────────
    # Antibot Cloud — внешняя капча до сайта.
    # Находим единственную видимую кнопку — все кнопки зелёные,
    # но только одна не имеет display:none, её и кликаем.
    print("🤖 Ждём появления капчи Antibot Cloud...")
    page.wait_for_selector("#content", timeout=10_000)

    # Пауза — имитируем что человек читает страницу перед кликом
    time.sleep(random.uniform(1.5, 3.5))

    # Находим видимую кнопку и кликаем с движением мыши
    captcha_btn = page.locator("#content div:visible").last
    box = captcha_btn.bounding_box()
    page.mouse.move(
        box["x"] + box["width"] / 2,
        box["y"] + box["height"] / 2
    )
    time.sleep(random.uniform(0.3, 0.7))
    captcha_btn.click()
    print("✅ Капча нажата, ждём загрузки сайта...")

    # Ждём пока капча исчезнет и загрузится реальный сайт
    page.wait_for_selector("form.order_f1", timeout=15_000)
    print("✅ Форма найдена, начинаем заполнение...")

    # Пауза — имитируем что человек читает страницу перед заполнением
    pause = random.uniform(2.5, 5.0)
    print(f"⏳ Пауза {pause:.1f}s (имитация чтения страницы)...")
    time.sleep(pause)

    # ── ГЕНЕРАЦИЯ ДАННЫХ ─────────────────────────────────────────────────
    # Имя генерируется первым — email строится на его основе
    # чтобы имя и email были связаны между собой
    name    = random_name()
    phone   = random_phone()
    email   = random_email(name)
    picture = random_picture()

    print("\n" + "=" * 50)
    print("📋 ДАННЫЕ ДЛЯ ОТПРАВКИ:")
    print(f"   Имя:     {name}")
    print(f"   Телефон: {phone}")
    print(f"   Email:   {email}")
    print(f"   Картина: {picture}")
    print("=" * 50 + "\n")

    # Берём первую форму — класс order_f1 только у неё
    # На странице 3 одинаковые формы, order_f1 — самая верхняя
    form = page.locator("form.order_f1")

    # ── ЗАПОЛНЕНИЕ ПОЛЕЙ ─────────────────────────────────────────────────
    print("✍️  Печатаем имя...")
    human_type(form.locator(".js-price-order-name"), name)
    time.sleep(random.uniform(0.5, 1.2))

    print("✍️  Печатаем телефон...")
    human_type(form.locator(".js-price-order-phone"), phone)
    time.sleep(random.uniform(0.4, 1.0))

    print("✍️  Печатаем email...")
    human_type(form.locator(".js-price-order-mail"), email)
    time.sleep(random.uniform(0.5, 1.5))

    print("✍️  Печатаем название картины...")
    human_type(form.locator(".js-price-order-picture"), picture)

    # Пауза перед сабмитом — человек "перечитывает" заполненную форму
    pause = random.uniform(1.5, 3.5)
    print(f"\n⏳ Пауза {pause:.1f}s перед отправкой (имитация проверки данных)...")
    time.sleep(pause)

    # ── СКРИНШОТ ДО ОТПРАВКИ ─────────────────────────────────────────────
    # Скроллим к форме чтобы она попала в кадр
    form.locator(".js-price-order-name").scroll_into_view_if_needed()
    print("📸 Скриншот заполненной формы (до отправки)...")
    page.screenshot(path="before_submit.png")
    print("   → Сохранён: before_submit.png")

    # ── ОТПРАВКА ─────────────────────────────────────────────────────────
    print("\n🖱️  Кликаем Submit...")
    form.locator('input[type="submit"]').click()

    # reCAPTCHA v3 (invisible) срабатывает в фоне автоматически —
    # Google анализирует поведение браузера и выдаёт токен без виджета.
    # Ждём зелёного текста "Спасибо! Ваша заявка отправлена."
    print("⏳ Ждём подтверждения от сервера (до 15 сек)...")
    success = form.locator(".js-price-order-thanks")
    success.wait_for(state="visible", timeout=15_000)

    # ── ИТОГОВЫЙ ЛОГ ─────────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("✅ ЗАЯВКА УСПЕШНО ОТПРАВЛЕНА!")
    print(f"   Имя:     {name}")
    print(f"   Телефон: {phone}")
    print(f"   Email:   {email}")
    print(f"   Картина: {picture}")
    print("-" * 50)
    print(f"   Браузер: {profile['name']}")
    print(f"   TZ:      {tz}")
    print("=" * 50)

    # Финальный скриншот — зелёное сообщение об успехе
    print("📸 Скриншот с подтверждением (после отправки)...")
    page.screenshot(path="after_submit.png")
    print("   → Сохранён: after_submit.png\n")

    print("🏁 Тест завершён. Браузер закроется через 40 сек (или закрой сам)...")

    import json

    print("\n📡 ПЕРЕХВАЧЕННЫЙ ЗАПРОС:")
    print(json.dumps(captured_request, ensure_ascii=False, indent=2))

    browser.close()
    print("🏁 Браузер закрыт.")