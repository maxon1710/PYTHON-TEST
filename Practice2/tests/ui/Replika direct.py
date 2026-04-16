"""
Прямая отправка формы реплика.рф через requests (без браузера)
Запуск: python REPLIKA_direct.py
"""

import random
import time
import requests
from urllib.parse import urlencode
from datetime import datetime

# ───────────────────── ПРОКСИ ─────────────────────────────────────
# Каждая попытка через новый IP — меньше капчи

PROXY_USER = "uxzmiktd"
PROXY_PASS = "g3ve5urzqszp"

PROXIES_LIST = [
    "31.59.20.176:6754",
    "198.23.239.134:6540",
    "45.38.107.97:6014",
    "107.172.163.27:6543",
    "198.105.121.200:6462",
    "216.10.27.159:6837",
    "142.111.67.146:5611",
    "191.96.254.138:6185",
    "31.58.9.4:6077",
    "198.46.161.42:5092",
]

USE_PROXY = True  # False = без прокси

# ───────────────────── ДАННЫЕ ─────────────────────────────────────

MALE_NAMES = [
    "Александр", "Дмитрий", "Максим", "Сергей", "Андрей",
    "Алексей", "Артём", "Илья", "Кирилл", "Михаил",
    "Никита", "Роман", "Павел", "Евгений", "Владимир",
    "Денис", "Иван", "Тимур", "Вадим", "Антон",
    "Игорь", "Олег", "Владислав", "Даниил", "Егор",
    "Руслан", "Константин", "Борис", "Юрий", "Станислав",
]
FEMALE_NAMES = [
    "Анастасия", "Екатерина", "Мария", "Анна", "Ольга",
    "Татьяна", "Наталья", "Елена", "Юлия", "Дарья",
    "Ирина", "Виктория", "Ксения", "Валерия", "Алина",
    "Марина", "Светлана", "Алёна", "Вера", "Надежда",
    "Полина", "Диана", "Яна", "Арина", "Елизавета",
    "Ульяна", "Варвара", "Кристина", "Карина", "Регина",
]
LAST_NAMES_M = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев",
    "Петров", "Соколов", "Михайлов", "Новиков", "Фёдоров",
    "Морозов", "Волков", "Алексеев", "Лебедев", "Семёнов",
    "Орлов", "Андреев", "Макаров", "Никитин", "Захаров",
]
LAST_NAMES_F = [n + "а" if not n.endswith("ых") and not n.endswith("их") else n
                for n in LAST_NAMES_M]

PAINTINGS = [
    "Звёздная ночь — Ван Гог",
    "Мона Лиза — Леонардо да Винчи",
    "Девятый вал — Айвазовский",
    "Три богатыря — Васнецов",
    "Утро в сосновом лесу — Шишкин",
    "Золотая осень — Левитан",
    "Бурлаки на Волге — Репин",
    "Охотники на привале — Перов",
    "Московский дворик — Поленов",
    "Поцелуй — Климт",
    "Юдифь — Климт",
    "Водяные лилии — Моне",
    "Подсолнухи — Ван Гог",
    "Девушка с жемчужной серёжкой — Вермер",
    "Ночной дозор — Рембрандт",
    "Гималаи — Рерих",
    "Девочка с персиками — Серов",
    "Купчиха за чаем — Кустодиев",
    "Корабль в бурном море — Айвазовский",
    "Над вечным покоем — Левитан",
]

PHONE_CODES = [
    "900", "901", "902", "903", "904", "905", "906",
    "910", "911", "912", "913", "914", "915", "916",
    "917", "918", "919", "920", "921", "922", "923",
    "925", "926", "927", "928", "929", "930", "931",
    "950", "951", "952", "960", "961", "962", "963",
    "964", "965", "966", "977", "980", "981", "982",
    "985", "986", "987", "988", "989", "991", "999",
]

EMAIL_DOMAINS = [
    "gmail.com", "yandex.ru", "mail.ru", "rambler.ru",
    "bk.ru", "list.ru", "ya.ru", "inbox.ru",
    "outlook.com", "hotmail.com",
]

# ───────────────────── ГЕНЕРАТОРЫ ─────────────────────────────────

TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
    'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
    'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def translit(text):
    return ''.join(TRANSLIT.get(c, c) for c in text.lower())


def gen_person():
    gender = random.choice(["m", "f"])
    first = random.choice(MALE_NAMES if gender == "m" else FEMALE_NAMES)
    last = random.choice(LAST_NAMES_M if gender == "m" else LAST_NAMES_F)
    return first, last


def gen_phone():
    code = random.choice(PHONE_CODES)
    n = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"+7 ({code}) {n[:3]}-{n[3:5]}-{n[5:7]}"


def gen_phone_parts(phone):
    """Разбить телефон на части для Tilda"""
    digits = ''.join(c for c in phone if c.isdigit())[1:]  # убираем 7
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"


def gen_email(first, last):
    fn = translit(first)
    ln = translit(last)
    domain = random.choice(EMAIL_DOMAINS)
    suffix = random.randint(1, 99)
    templates = [
        f"{fn}.{ln}@{domain}",
        f"{fn}{ln}{suffix}@{domain}",
        f"{fn[0]}{ln}@{domain}",
        f"{fn}_{suffix}@{domain}",
        f"{ln}.{fn[0]}@{domain}",
    ]
    return random.choice(templates)


def gen_painting():
    return random.choice(PAINTINGS)


# ───────────────────── FINGERPRINT ────────────────────────────────

def gen_fp():
    """
    Генерирует tildaspec-fp похожий на настоящий.
    Формат из перехваченного запроса:
    st{float}w{int}h{int}ft{float}{float}
    """
    # Берём реальные значения из перехваченного запроса как базу
    # и немного рандомизируем
    screen_w = random.choice([1366, 1440, 1536, 1920, 2560])
    screen_h = random.choice([768, 900, 864, 1080, 1440])
    scroll_t = round(random.uniform(400, 800), 5)
    scroll2 = round(random.uniform(400, 800), 5)
    scroll3 = round(random.uniform(400, 800), 5)

    # Из реального запроса: st4526.39990234375w838h1067ft484.52499389648444526.39990234375
    # Это кодировка: scrollTop, windowWidth, windowHeight, fromTop, fromTop2
    fp = f"st{scroll_t}w{screen_w}h{screen_h}ft{scroll2}{scroll3}"
    return fp


def gen_cookie_ts():
    """Генерирует tildaspec-cookie с ddg значениями"""
    ts = int(time.time())
    ddg9 = f"83.149.{random.randint(1,255)}.{random.randint(1,255)}"
    ddg8 = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=16))
    ddg10 = str(ts - random.randint(0, 3600))
    return f"__ddg9_={ddg9}; __ddg8_={ddg8}; __ddg10_={ddg10}"


# ───────────────────── ОСНОВНАЯ ФУНКЦИЯ ───────────────────────────

def send_form(attempt_index=0):
    """attempt_index используется для выбора прокси (разный IP на каждую попытку)"""
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    first, last = gen_person()
    full_name = f"{first} {last}"
    phone_full = gen_phone()
    phone_parts = gen_phone_parts(phone_full)
    email = gen_email(first, last)
    painting = gen_painting()

    print(f"[{run_id}] Отправляем заявку")
    print(f"  👤 Имя:     {full_name}")
    print(f"  📞 Телефон: {phone_full}")
    print(f"  📧 Email:   {email}")
    print(f"  🎨 Картина: {painting}")

    # ── Тело запроса — точная копия из Network ──
    ts = str(int(time.time() * 1000))
    data = {
        "formservices[]": [
            "f1f0107c2fd9bde6d93e8ea779cf63ca",
            "2b84f03ea8d221968f781b9efbda5e1e",
        ],
        "tildaspec-formname": "Главная_верхняя",
        "Name": full_name,
        "Email": email,
        "tildaspec-phone-part[]-iso": "+7",
        "tildaspec-phone-part[]": phone_parts,
        "Phone": phone_full,
        "Input": painting,
        "form-spec-comments": "",
        "tildaspec-cookie": gen_cookie_ts(),
        "tildaspec-referer": "https://xn--80ajjidxf.xn--p1ai/",
        "tildaspec-formid": "form1802547881",
        "tildaspec-formskey": "8812ee68b335992a5ba27c7211848109",
        "tildaspec-version-lib": "02.001",
        "tildaspec-pageid": "110749096",
        "tildaspec-projectid": "11848109",
        "tildaspec-lang": "RU",
        "tildaspec-fp": gen_fp(),
    }

    # Кодируем вручную (списки → несколько одинаковых ключей)
    encoded_parts = []
    for key, val in data.items():
        if isinstance(val, list):
            for item in val:
                encoded_parts.append((key, item))
        else:
            encoded_parts.append((key, val))

    body = urlencode(encoded_parts)

    # ── Заголовки — точная копия из Network ──
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://xn--80ajjidxf.xn--p1ai",
        "Referer": "https://xn--80ajjidxf.xn--p1ai/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "sec-ch-ua": '"Chromium";v="120", "Not-A.Brand";v="24", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    # ── Выбираем прокси для этой попытки ──
    proxy_cfg = None
    proxy_label = "без прокси"
    if USE_PROXY and PROXIES_LIST:
        proxy_addr = PROXIES_LIST[attempt_index % len(PROXIES_LIST)]
        proxy_cfg = {
            "http": f"http://{PROXY_USER}:{PROXY_PASS}@{proxy_addr}",
            "https": f"http://{PROXY_USER}:{PROXY_PASS}@{proxy_addr}",
        }
        proxy_label = proxy_addr

    print(f"\n  📤 Отправляем через {proxy_label}...")

    try:
        resp = requests.post(
            "https://forms.tildaapi.com/procces/",
            data=body,
            headers=headers,
            proxies=proxy_cfg,
            timeout=15,
        )
        result = resp.json()
        print(f"  📨 Статус: {resp.status_code}")
        print(f"  📨 Ответ:  {result}")
        print()

        if result.get("message") == "OK":
            print("  ✅ ЗАЯВКА ОТПРАВЛЕНА! Капча не потребовалась!")
            return True, full_name, phone_full, email, painting
        elif result.get("needcaptcha"):
            print("  🤖 Сервер требует капчу — нужна 2captcha")
            return False, full_name, phone_full, email, painting
        else:
            print(f"  ❓ Неожиданный ответ: {result}")
            return False, full_name, phone_full, email, painting

    except Exception as e:
        print(f"  ❌ Ошибка запроса: {e}")
        return False, full_name, phone_full, email, painting


# ───────────────────── ОДНА ЗАЯВКА С RETRY ──────────────────────

def send_one_application(max_retries=5):
    """
    Отправляет одну заявку с повторами до успеха.
    Tilda rate-limit по IP — обычно 2-3 попытка проходит.
    """
    for attempt in range(1, max_retries + 1):
        print(f"── Попытка {attempt}/{max_retries} ──")
        ok, name, phone, email, painting = send_form(attempt_index=attempt - 1)
        if ok:
            print(f"  🎉 Успех с попытки {attempt}!")
            return True, name, phone, email, painting
        # Пауза перед следующей попыткой — имитируем человека
        if attempt < max_retries:
            delay = random.uniform(4, 10)
            print(f"  ⏳ needcaptcha — пауза {delay:.1f} сек, следующая попытка...")
            time.sleep(delay)

    print(f"  ❌ Все {max_retries} попыток вернули needcaptcha")
    return False, None, None, None, None


# ───────────────────── ЗАПУСК ─────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  Прямая отправка формы реплика.рф (без браузера)")
    print("=" * 55)
    print()

    ok, name, phone, email, painting = send_one_application(max_retries=5)

    print()
    print("=" * 55)
    if ok:
        print("✅ ЗАЯВКА ОТПРАВЛЕНА!")
        print(f"   👤 {name}")
        print(f"   📞 {phone}")
        print(f"   📧 {email}")
        print(f"   🎨 {painting}")
    else:
        print("🤖 Не удалось обойти капчу за 5 попыток")
        print("   → Переходим к 2captcha интеграции")
    print("=" * 55)