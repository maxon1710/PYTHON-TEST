"""
Smoke-тест формы реплика.рф
Локальный запуск: python replica_script.py
На сервере: добавить прокси (см. PROXIES в конфиге)
"""

import random
import string
import time
import os
from datetime import datetime
import requests
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
try:
    from playwright_stealth import stealth_sync
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False
    print("  ⚠️  playwright-stealth не установлен: pip install playwright-stealth")

# ───────────────────────────── КОНФИГ ─────────────────────────────

SITE_URL = "https://xn--80ajjidxf.xn--p1ai/"  # реплика.рф

# Прокси — пустой список для локального запуска.
# Для сервера добавить webshare прокси в этот список.
PROXIES = [
    # "31.59.20.176:6754",
    # "198.23.239.134:6540",
    # ... добавить когда будем деплоить на сервер
]
PROXY_USER = "uxzmiktd"
PROXY_PASS = "g3ve5urzqszp"

USE_PROXY = len(PROXIES) > 0  # автоматически False если список пустой

HEADLESS = False  # False = видно браузер (для отладки в PyCharm)
SCREENSHOTS_DIR = "screens_replica"

# ───────────────────────── ДАННЫЕ ─────────────────────────────────

MALE_NAMES = [
    "Александр", "Дмитрий", "Максим", "Сергей", "Андрей",
    "Алексей", "Артём", "Илья", "Кирилл", "Михаил",
    "Никита", "Роман", "Павел", "Евгений", "Владимир",
    "Денис", "Иван", "Тимур", "Вадим", "Антон",
    "Игорь", "Олег", "Владислав", "Даниил", "Егор",
    "Глеб", "Степан", "Фёдор", "Лев", "Виктор",
    "Руслан", "Константин", "Борис", "Юрий", "Геннадий",
    "Анатолий", "Валерий", "Пётр", "Николай", "Григорий",
    "Василий", "Леонид", "Станислав", "Ярослав", "Марк",
    "Арсений", "Матвей", "Тихон", "Филипп", "Захар",
    "Семён", "Савва", "Макар", "Лука", "Платон",
    "Виталий", "Эдуард", "Аркадий", "Вячеслав", "Всеволод",
    "Ростислав", "Святослав", "Мирослав", "Богдан", "Родион",
    "Трофим", "Кузьма", "Прохор", "Клим", "Демид",
    "Добрыня", "Радомир", "Велимир", "Звенислав", "Доброслав",
    "Яромир", "Братислав", "Воислав", "Радослав", "Твердислав",
    "Гордей", "Евсей", "Епифан", "Лаврентий", "Мефодий",
    "Нестор", "Осип", "Панкрат", "Потап", "Прокопий",
    "Силантий", "Спиридон", "Терентий", "Тихон", "Фотий",
    "Харитон", "Харлам", "Хрисанф", "Порфирий", "Памфил",
    "Никодим", "Мартын", "Лукьян", "Кондрат", "Карп",
    "Исай", "Зиновий", "Евлампий", "Досифей", "Гурий",
    "Афанасий", "Аверьян", "Авдей", "Агафон", "Акакий",
    "Акила", "Алипий", "Амвросий", "Ананий", "Анисим",
    "Антип", "Аполлон", "Аристарх", "Арсений", "Артамон",
    "Архип", "Аскольд", "Астафий", "Афиноген", "Ахилл",
    "Варлаам", "Варфоломей", "Вениамин", "Викентий", "Вифлеем",
    "Власий", "Владлен", "Гавриил", "Гермоген", "Гласий",
    "Дементий", "Диомид", "Дионисий", "Дорофей", "Дулат",
]

FEMALE_NAMES = [
    "Анастасия", "Екатерина", "Мария", "Анна", "Ольга",
    "Татьяна", "Наталья", "Елена", "Юлия", "Дарья",
    "Ирина", "Виктория", "Ксения", "Валерия", "Алина",
    "Марина", "Светлана", "Алёна", "Вера", "Надежда",
    "Любовь", "Галина", "Людмила", "Нина", "Тамара",
    "Лариса", "Наталия", "Элина", "Кристина", "Полина",
    "Диана", "Яна", "Снежана", "Камила", "Арина",
    "Елизавета", "Маргарита", "Оксана", "Лидия", "Зинаида",
    "Антонина", "Валентина", "Вероника", "Жанна", "Инна",
    "Карина", "Лиана", "Милана", "Нелли", "Оля",
    "Регина", "Сабина", "Ульяна", "Фатима", "Христина",
    "Цветана", "Эвелина", "Эмилия", "Юлиана", "Аделина",
    "Аксинья", "Алевтина", "Александра", "Алла", "Альбина",
    "Анфиса", "Аполлинария", "Арсения", "Варвара", "Василиса",
    "Вероника", "Глафира", "Глория", "Дина", "Домна",
    "Евгения", "Евдокия", "Елизавета", "Зоя", "Злата",
    "Изольда", "Илона", "Капитолина", "Клавдия", "Клара",
    "Клеопатра", "Кира", "Лада", "Лейла", "Лукерья",
    "Майя", "Марфа", "Матрёна", "Милена", "Мира",
    "Мирослава", "Нонна", "Октябрина", "Параскева", "Пелагея",
    "Прасковья", "Раиса", "Римма", "Роза", "Рогнеда",
    "Руфина", "Серафима", "Сима", "Таисия", "Тамила",
    "Ульяна", "Устинья", "Фаина", "Федосья", "Феодосия",
    "Фёкла", "Харитина", "Христина", "Эльвира", "Эмма",
    "Юлия", "Ядвига", "Ярослава", "Аглая", "Агния",
    "Агрипина", "Аграфена", "Аида", "Аксана", "Акулина",
    "Алла", "Амина", "Ангелина", "Анжелика", "Аникита",
    "Аниса", "Анисья", "Антонида", "Аполлония", "Апрель",
    "Ариадна", "Аримея", "Арина", "Аркадия", "Арлета",
    "Арсенья", "Артемида", "Аселя", "Аскольда", "Астрид",
]

LAST_NAMES_MALE = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев",
    "Петров", "Соколов", "Михайлов", "Новиков", "Фёдоров",
    "Морозов", "Волков", "Алексеев", "Лебедев", "Семёнов",
    "Егоров", "Павлов", "Козлов", "Степанов", "Николаев",
    "Орлов", "Андреев", "Макаров", "Никитин", "Захаров",
    "Зайцев", "Соловьёв", "Борисов", "Яковлев", "Григорьев",
    "Романов", "Воробьёв", "Сергеев", "Кузьмин", "Фролов",
    "Александров", "Дмитриев", "Королёв", "Гусев", "Тихонов",
    "Ильин", "Медведев", "Никифоров", "Беляев", "Комаров",
]

LAST_NAMES_FEMALE = [
    "Иванова", "Смирнова", "Кузнецова", "Попова", "Васильева",
    "Петрова", "Соколова", "Михайлова", "Новикова", "Фёдорова",
    "Морозова", "Волкова", "Алексеева", "Лебедева", "Семёнова",
    "Егорова", "Павлова", "Козлова", "Степанова", "Николаева",
    "Орлова", "Андреева", "Макарова", "Никитина", "Захарова",
    "Зайцева", "Соловьёва", "Борисова", "Яковлева", "Григорьева",
    "Романова", "Воробьёва", "Сергеева", "Кузьмина", "Фролова",
    "Александрова", "Дмитриева", "Королёва", "Гусева", "Тихонова",
    "Ильина", "Медведева", "Никифорова", "Беляева", "Комарова",
]

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
    "Грачи прилетели — Саврасов",
    "Явление Христа народу — Иванов",
    "Последний день Помпеи — Брюллов",
    "Купание красного коня — Петров-Водкин",
    "Апофеоз войны — Верещагин",
    "Боярыня Морозова — Суриков",
    "Покорение Сибири Ермаком — Суриков",
    "Утро стрелецкой казни — Суриков",
    "Меншиков в Берёзове — Суриков",
    "Над вечным покоем — Левитан",
    "Владимирка — Левитан",
    "Март — Левитан",
    "Весна. Большая вода — Левитан",
    "У омута — Левитан",
    "Вечерний звон — Левитан",
    "Берёзовая роща — Левитан",
    "Лесные дали — Шишкин",
    "Рожь — Шишкин",
    "Дубовая роща — Шишкин",
    "Сосны, освещённые солнцем — Шишкин",
    "На севере диком — Шишкин",
    "Лунная ночь на Днепре — Куинджи",
    "Берёзовая роща — Куинджи",
    "После дождя — Куинджи",
    "Море. Коктебель — Волошин",
    "Корабль в бурном море — Айвазовский",
    "Лунная ночь на море — Айвазовский",
    "Чёрное море — Айвазовский",
    "Волна — Айвазовский",
    "Радуга — Айвазовский",
    "Буря у мыса Айя — Айвазовский",
    "Поцелуй — Климт",
    "Юдифь — Климт",
    "Дерево жизни — Климт",
    "Три возраста женщины — Климт",
    "Мать и дитя — Климт",
    "Водяные лилии — Моне",
    "Стог сена — Моне",
    "Руанский собор — Моне",
    "Завтрак на траве — Мане",
    "Олимпия — Мане",
    "Танцовщицы — Дега",
    "Голубые танцовщицы — Дега",
    "Абсент — Дега",
    "Бал в Мулен де ла Галетт — Ренуар",
    "Зонтики — Ренуар",
    "Портрет актрисы Жанны Самари — Ренуар",
    "Подсолнухи — Ван Гог",
    "Ирисы — Ван Гог",
    "Ночное кафе — Ван Гог",
    "Пшеничное поле с воронами — Ван Гог",
    "Сеятель — Ван Гог",
    "Спальня в Арле — Ван Гог",
    "Девушка с жемчужной серёжкой — Вермер",
    "Молочница — Вермер",
    "Урок музыки — Вермер",
    "Ночной дозор — Рембрандт",
    "Автопортрет — Рембрандт",
    "Возвращение блудного сына — Рембрандт",
    "Урок анатомии — Рембрандт",
    "Синдики — Рембрандт",
    "Рождение Венеры — Боттичелли",
    "Весна — Боттичелли",
    "Сикстинская мадонна — Рафаэль",
    "Афинская школа — Рафаэль",
    "Тайная вечеря — Леонардо да Винчи",
    "Витрувианский человек — Леонардо да Винчи",
    "Сотворение Адама — Микеланджело",
    "Страшный суд — Микеланджело",
    "Давид — Микеланджело",
    "Венера Урбинская — Тициан",
    "Портрет Карла V — Тициан",
    "Вакх — Тициан",
    "Сдача Бреды — Веласкес",
    "Менины — Веласкес",
    "Портрет Иннокентия X — Веласкес",
    "Сатурн, пожирающий своего сына — Гойя",
    "Маха обнажённая — Гойя",
    "Расстрел повстанцев — Гойя",
    "Свобода на баррикадах — Делакруа",
    "Резня на Хиосе — Делакруа",
    "Большие купальщицы — Сезанн",
    "Яблоки и апельсины — Сезанн",
    "Персиковое дерево в цвету — Сезанн",
    "Танец — Матисс",
    "Музыка — Матисс",
    "Красная комната — Матисс",
    "Авиньонские девицы — Пикассо",
    "Герника — Пикассо",
    "Девочка на шаре — Пикассо",
    "Гималаи — Рерих",
    "Заморские гости — Рерих",
    "Поход Игоря — Рерих",
    "Синий натюрморт — Ларионова",
    "Чёрный квадрат — Малевич",
    "Купание красного коня — Петров-Водкин",
    "Новая планета — Юон",
    "Портрет Льва Толстого — Репин",
    "Не ждали — Репин",
    "Иван Грозный убивает сына — Репин",
    "Запорожцы пишут письмо — Репин",
    "Садко — Репин",
    "Крёстный ход в Курской губернии — Репин",
    "Царевна Несмеяна — Васнецов",
    "Алёнушка — Васнецов",
    "Иван Царевич на сером волке — Васнецов",
    "Снегурочка — Васнецов",
    "После побоища — Васнецов",
    "Витязь на распутье — Васнецов",
    "Богатырский скок — Васнецов",
    "Девочка с персиками — Серов",
    "Девушка, освещённая солнцем — Серов",
    "Пётр I — Серов",
    "Портрет Иды Рубинштейн — Серов",
    "Похищение Европы — Серов",
    "Купчиха за чаем — Кустодиев",
    "Масленица — Кустодиев",
    "Красавица — Кустодиев",
    "Ярмарка — Кустодиев",
    "Сирень — Кончаловский",
    "Натюрморт с маками — Кончаловский",
    "Рождественские розы — Моне вольная копия",
    "Эверест на рассвете — авторская",
    "Белые ночи Петербурга — авторская",
    "Осень в Подмосковье — авторская",
    "Закат над морем — авторская",
    "Зимний лес — авторская",
    "Полевые цветы — авторская",
    "Натюрморт с яблоками — авторская",
    "Деревенский пейзаж — авторская",
    "Горный ручей — авторская",
    "Цветущий луг — авторская",
    "Тихая гавань — авторская",
    "Старая мельница — авторская",
]

# 15 профилей браузера
BROWSER_PROFILES = [
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "viewport": {"width": 1366, "height": 768},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "viewport": {"width": 1440, "height": 900},
        "locale": "ru-RU",
        "timezone": "Europe/Samara",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "viewport": {"width": 1280, "height": 800},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "viewport": {"width": 1600, "height": 900},
        "locale": "ru-RU",
        "timezone": "Asia/Yekaterinburg",
        "color_scheme": "dark",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "viewport": {"width": 1440, "height": 900},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "MacIntel",
    },
    {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "viewport": {"width": 1512, "height": 982},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "MacIntel",
    },
    {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
        "viewport": {"width": 1280, "height": 800},
        "locale": "ru-RU",
        "timezone": "Europe/Kaliningrad",
        "color_scheme": "dark",
        "platform": "MacIntel",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
        "timezone": "Asia/Novosibirsk",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0",
        "viewport": {"width": 1366, "height": 768},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "Linux x86_64",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "viewport": {"width": 1680, "height": 1050},
        "locale": "ru-RU",
        "timezone": "Europe/Volgograd",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 YaBrowser/24.1.0.0",
        "viewport": {"width": 1366, "height": 768},
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "color_scheme": "light",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "viewport": {"width": 2560, "height": 1440},
        "locale": "ru-RU",
        "timezone": "Asia/Krasnoyarsk",
        "color_scheme": "dark",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "viewport": {"width": 1024, "height": 768},
        "locale": "ru-RU",
        "timezone": "Europe/Ulyanovsk",
        "color_scheme": "light",
        "platform": "Win32",
    },
]

# Реальные коды операторов РФ
PHONE_CODES = [
    "900", "901", "902", "903", "904", "905", "906",
    "908", "909", "910", "911", "912", "913", "914",
    "915", "916", "917", "918", "919", "920", "921",
    "922", "923", "924", "925", "926", "927", "928",
    "929", "930", "931", "932", "933", "934", "936",
    "937", "938", "939", "950", "951", "952", "953",
    "954", "955", "956", "958", "960", "961", "962",
    "963", "964", "965", "966", "967", "968", "969",
    "977", "978", "980", "981", "982", "983", "984",
    "985", "986", "987", "988", "989", "991", "992",
    "993", "994", "995", "996", "997", "999",
]

EMAIL_DOMAINS = [
    "gmail.com", "yandex.ru", "mail.ru", "rambler.ru",
    "bk.ru", "list.ru", "inbox.ru", "ya.ru",
    "outlook.com", "hotmail.com",
]

# ───────────────────────── ГЕНЕРАТОРЫ ─────────────────────────────

def gen_name():
    """Возвращает кортеж (имя, фамилия, пол)"""
    gender = random.choice(["male", "female"])
    if gender == "male":
        first = random.choice(MALE_NAMES)
        last = random.choice(LAST_NAMES_MALE)
    else:
        first = random.choice(FEMALE_NAMES)
        last = random.choice(LAST_NAMES_FEMALE)
    return first, last, gender


def gen_phone():
    """Генерирует номер в формате (9XX) XXX-XX-XX для ввода в маску Tilda"""
    code = random.choice(PHONE_CODES)
    part1 = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    part2 = ''.join([str(random.randint(0, 9)) for _ in range(2)])
    part3 = ''.join([str(random.randint(0, 9)) for _ in range(2)])
    return f"({code}) {part1}-{part2}-{part3}"


def gen_email(first_name, last_name):
    """Генерирует правдоподобный email на основе имени"""
    transliterate = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }

    def translit(text):
        result = ''
        for char in text.lower():
            result += transliterate.get(char, char)
        return result

    fn = translit(first_name)
    ln = translit(last_name)
    domain = random.choice(EMAIL_DOMAINS)
    suffix = random.randint(1, 99)

    templates = [
        f"{fn}.{ln}@{domain}",
        f"{fn}{ln}{suffix}@{domain}",
        f"{fn[0]}{ln}@{domain}",
        f"{fn}_{ln[0]}{suffix}@{domain}",
        f"{ln}.{fn[0]}@{domain}",
        f"{fn}{suffix}@{domain}",
    ]
    return random.choice(templates)


def gen_painting():
    return random.choice(PAINTINGS)


# ───────────────────────── БРАУЗЕР ────────────────────────────────

def get_proxy():
    """Возвращает прокси конфиг или None"""
    if not USE_PROXY:
        return None
    proxy_addr = random.choice(PROXIES)
    host, port = proxy_addr.split(":")
    return {
        "server": f"http://{host}:{port}",
        "username": PROXY_USER,
        "password": PROXY_PASS,
    }


def get_profile():
    return random.choice(BROWSER_PROFILES)


# ───────────────────────── ПОВЕДЕНИЕ ──────────────────────────────

def human_delay(min_ms=80, max_ms=220):
    """Случайная задержка имитирующая человека"""
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


def slow_type(page, selector, text):
    """
    Вводит текст посимвольно с реалистичными задержками.
    Перед вводом: скролл к элементу, наведение мыши, клик.
    """
    element = page.locator(selector)
    element.scroll_into_view_if_needed()
    human_delay(200, 500)

    # Наводим мышь на центр элемента
    box = element.bounding_box()
    if box:
        x = box["x"] + box["width"] / 2 + random.uniform(-10, 10)
        y = box["y"] + box["height"] / 2 + random.uniform(-3, 3)
        page.mouse.move(x, y, steps=random.randint(8, 20))
        human_delay(100, 300)

    element.click()
    human_delay(150, 400)

    # Посимвольный ввод с паузами
    for char in text:
        element.type(char, delay=random.randint(60, 180))
        # Иногда чуть длиннее пауза (задумался)
        if random.random() < 0.08:
            human_delay(300, 700)

    human_delay(200, 500)


def random_scroll(page):
    """Случайный скролл вниз и немного вверх — как живой пользователь"""
    total_height = page.evaluate("document.body.scrollHeight")
    current = page.evaluate("window.scrollY")

    # Скролл вниз несколькими шагами
    steps = random.randint(3, 7)
    for _ in range(steps):
        scroll_by = random.randint(150, 400)
        page.evaluate(f"window.scrollBy(0, {scroll_by})")
        human_delay(300, 800)

    # Иногда чуть скроллим обратно вверх
    if random.random() < 0.4:
        page.evaluate(f"window.scrollBy(0, -{random.randint(100, 300)})")
        human_delay(400, 900)


def random_mouse_moves(page, count=None):
    """Хаотичные движения мыши"""
    if count is None:
        count = random.randint(3, 8)
    vp = page.viewport_size or {"width": 1366, "height": 768}
    for _ in range(count):
        x = random.randint(100, vp["width"] - 100)
        y = random.randint(100, vp["height"] - 100)
        steps = random.randint(10, 30)
        page.mouse.move(x, y, steps=steps)
        human_delay(100, 400)


# ───────────────────────── ОСНОВНАЯ ЛОГИКА ────────────────────────

def run_test():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    first_name, last_name, gender = gen_name()
    full_name = f"{first_name} {last_name}"
    phone = gen_phone()
    email = gen_email(first_name, last_name)
    painting = gen_painting()
    profile = get_profile()
    proxy = get_proxy()

    print(f"[{run_id}] Запуск теста")
    print(f"  Имя:     {full_name}")
    print(f"  Телефон: {phone}")
    print(f"  Email:   {email}")
    print(f"  Картина: {painting}")
    print(f"  Профиль: {profile['user_agent'][:60]}...")
    print(f"  Прокси:  {'включён' if proxy else 'выключен (локальный запуск)'}")
    print(f"  Тема:    {profile['color_scheme']}")

    with sync_playwright() as p:
        launch_args = {
            "headless": HEADLESS,
            "channel": "chrome",  # реальный Chrome — меньше детектируется
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
                "--window-size=1366,768",
                f"--lang={profile['locale']}",
            ],
        }
        if proxy:
            launch_args["proxy"] = proxy

        # Если Chrome не установлен — fallback на Chromium
        try:
            browser = p.chromium.launch(**launch_args)
        except Exception:
            print("  ⚠️  Chrome не найден, используем Playwright Chromium")
            launch_args.pop("channel", None)
            browser = p.chromium.launch(**launch_args)

        context_args = {
            "user_agent": profile["user_agent"],
            "viewport": profile["viewport"],
            "locale": profile["locale"],
            "timezone_id": profile["timezone"],
            "color_scheme": profile["color_scheme"],
            "java_script_enabled": True,
            "accept_downloads": False,
            "extra_http_headers": {
                "Accept-Language": f"{profile['locale']},ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "DNT": "1",
            },
            # Скрываем webdriver
            "ignore_https_errors": True,
        }
        if proxy:
            context_args["proxy"] = proxy

        context = browser.new_context(**context_args)

        # Скрываем navigator.webdriver
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ru-RU', 'ru', 'en-US', 'en'],
            });
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
        """)

        page = context.new_page()
        page.set_default_timeout(30000)

        # Stealth — патчим fingerprint
        if HAS_STEALTH:
            stealth_sync(page)
            print("  🥷 Stealth активирован")

        crash_screen = os.path.join(SCREENSHOTS_DIR, f"{run_id}_CRASH.png")
        result = None

        try:
            # ── Открываем сайт ──
            print(f"  Открываем {SITE_URL}...")
            page.goto(SITE_URL, wait_until="domcontentloaded", timeout=30000)
            human_delay(1500, 3000)

            # ── Читаем страницу как человек ──
            random_mouse_moves(page, count=random.randint(3, 6))
            random_scroll(page)
            human_delay(1000, 2500)

            # Скролл обратно к форме
            page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.6)")
            human_delay(800, 1500)

            # ── Заполняем форму ──
            print("  ✍️  Заполняем форму...")

            # Имя
            slow_type(page, "#input_9618025321510", full_name)
            print(f"     Имя → {full_name}")

            # Email
            slow_type(page, "#input_9618025321511", email)
            print(f"     Email → {email}")

            # Телефон — поле маски Tilda, вводим только цифры (маска уже содержит +7)
            phone_input = page.locator("#input_9618025321512")
            phone_input.scroll_into_view_if_needed()
            human_delay(300, 600)
            box = phone_input.bounding_box()
            if box:
                page.mouse.move(
                    box["x"] + box["width"] / 2,
                    box["y"] + box["height"] / 2,
                    steps=random.randint(10, 20)
                )
            phone_input.click()
            human_delay(200, 500)
            page.keyboard.press("Control+a")
            page.keyboard.press("Delete")
            human_delay(100, 300)
            for char in phone:
                if char.isdigit():
                    page.keyboard.type(char, delay=random.randint(80, 160))
            human_delay(200, 500)
            print(f"     Телефон → +7 {phone}")

            # Картина/автор
            slow_type(page, "#input_9618025321513", painting)
            print(f"     Картина → {painting}")

            # Пауза перед отправкой — читаем форму как человек
            random_mouse_moves(page, count=random.randint(2, 4))
            human_delay(800, 1500)

            # ── Перехватываем реальный POST запрос от Tilda ──
            # Сохраняем тело запроса и заголовки чтобы повторить без капчи
            captured_request_body = None
            captured_request_headers = None

            def handle_request(request):
                nonlocal captured_request_body, captured_request_headers
                if "forms.tildaapi.com/procces/" in request.url and "captcha" not in request.url:
                    captured_request_body = request.post_data
                    captured_request_headers = dict(request.headers)

            page.on("request", handle_request)

            # Также слушаем ответы
            tilda_ok = False
            captcha_needed = False
            network_log = []

            def handle_response(response):
                nonlocal tilda_ok, captcha_needed
                url = response.url
                if "tildaapi.com" not in url:
                    return
                status = response.status
                try:
                    body = response.json()
                    body_str = str(body)[:100]
                except Exception:
                    body_str = "(не JSON)"
                short_url = url.split("tildaapi.com")[1][:60]
                network_log.append(f"  [{status}] {short_url}  →  {body_str}")
                if "procces/" in url and "captcha" not in url:
                    if isinstance(body, dict):
                        if body.get("message") == "OK":
                            tilda_ok = True
                        if body.get("needcaptcha"):
                            captcha_needed = True

            page.on("response", handle_response)

            # ── Скрин заполненной формы (перед отправкой) ──
            submit_btn = page.locator("#rec1802547881 .t-submit")
            submit_btn.scroll_into_view_if_needed()
            human_delay(600, 1000)
            before_screen = os.path.join(SCREENSHOTS_DIR, f"{run_id}_before.png")
            page.screenshot(path=before_screen, full_page=False)
            print(f"  📸 Скрин заполненной формы: {before_screen}")

            # ── Нажимаем кнопку ──
            box = submit_btn.bounding_box()
            if box:
                page.mouse.move(
                    box["x"] + box["width"] / 2 + random.uniform(-5, 5),
                    box["y"] + box["height"] / 2 + random.uniform(-3, 3),
                    steps=random.randint(12, 25)
                )
                human_delay(300, 600)
            submit_btn.click()
            print("  🖱  Кнопка «Отправить» нажата — ждём ответ Tilda...")

            # ── Ждём ответ от /procces/ (до 6 сек) ──
            for _ in range(60):
                time.sleep(0.1)
                if tilda_ok or captcha_needed:
                    break

            print()
            print("  📡 Первый ответ Tilda API:")
            for entry in network_log:
                print(entry)
            if not network_log:
                print("  (нет запросов — возможно форма не отправилась)")
            print()

            # ── Стратегия А: форма прошла без капчи ──
            if tilda_ok:
                print("  🎉 Форма принята без капчи!")

            # ── Стратегия Б: нужна капча — повторяем запрос через requests ──
            elif captcha_needed and captured_request_body:
                print("  🤖 Tilda требует капчу (needcaptcha=1)")
                print("  ♻️  Пробуем повторить POST запрос напрямую через requests...")
                print("     (обходим капчу — браузерный fingerprint уже в cookie)")

                # Берём cookies из браузера — они содержат __ddg* от DDoS-Guard
                browser_cookies = context.cookies()
                cookie_header = "; ".join([
                    f"{c['name']}={c['value']}"
                    for c in browser_cookies
                    if "tildaapi" in c.get("domain", "") or "xn--" in c.get("domain", "")
                ])

                # Заголовки — копируем из перехваченного запроса
                headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://xn--80ajjidxf.xn--p1ai",
                    "Referer": "https://xn--80ajjidxf.xn--p1ai/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "User-Agent": profile["user_agent"],
                    "sec-ch-ua": '"Chromium";v="120", "Not-A.Brand";v="24"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                }
                if cookie_header:
                    headers["Cookie"] = cookie_header
                    print(f"     Cookie: {cookie_header[:80]}...")

                try:
                    resp = requests.post(
                        "https://forms.tildaapi.com/procces/",
                        data=captured_request_body,
                        headers=headers,
                        timeout=15
                    )
                    resp_json = resp.json()
                    print(f"  📨 Ответ requests: {resp.status_code} → {resp_json}")

                    if resp_json.get("message") == "OK":
                        tilda_ok = True
                        print("  ✅ Форма отправлена через прямой запрос!")
                    elif resp_json.get("needcaptcha"):
                        print("  ⚠️  Прямой запрос тоже требует капчу")
                        print("  🔍 Пробуем кликнуть чекбокс в браузере...")

                        # Пробуем кликнуть капчу в браузере как запасной вариант
                        checkbox_iframe = page.locator("[data-testid='checkbox-iframe']")
                        try:
                            checkbox_iframe.wait_for(state="visible", timeout=10000)
                            human_delay(1500, 2500)
                            frame = checkbox_iframe.content_frame()
                            if frame:
                                btn = frame.locator("#js-button")
                                btn.wait_for(state="visible", timeout=8000)
                                human_delay(700, 1200)
                                box = checkbox_iframe.bounding_box()
                                if box:
                                    page.mouse.move(
                                        box["x"] + 25 + random.uniform(0, 8),
                                        box["y"] + box["height"] / 2,
                                        steps=random.randint(15, 25)
                                    )
                                    human_delay(400, 700)
                                btn.click()
                                print("  ✅ Кликнули «Я не робот»")
                                # Ждём OK
                                for _ in range(100):
                                    time.sleep(0.1)
                                    if tilda_ok:
                                        break
                                if tilda_ok:
                                    print("  🎉 Капча пройдена!")
                                else:
                                    print("  ⏸  Капча не пройдена, браузер открыт 60 сек")
                                    time.sleep(60)
                        except Exception as ce:
                            print(f"  ❌ Iframe: {str(ce)[:60]}")
                            time.sleep(30)
                    else:
                        print(f"  ❓ Неожиданный ответ: {resp_json}")

                except Exception as re:
                    print(f"  ❌ requests ошибка: {str(re)[:80]}")

            elif captcha_needed and not captured_request_body:
                print("  ⚠️  captcha_needed но тело запроса не перехвачено")
                print("  🔍 Пробуем кликнуть капчу напрямую...")
                checkbox_iframe = page.locator("[data-testid='checkbox-iframe']")
                try:
                    checkbox_iframe.wait_for(state="visible", timeout=10000)
                    human_delay(1500, 2500)
                    frame = checkbox_iframe.content_frame()
                    if frame:
                        btn = frame.locator("#js-button")
                        btn.wait_for(state="visible", timeout=8000)
                        human_delay(700, 1200)
                        btn.click()
                        print("  ✅ Кликнули чекбокс")
                        for _ in range(100):
                            time.sleep(0.1)
                            if tilda_ok:
                                break
                except Exception:
                    pass
                time.sleep(30)

            else:
                print("  ❓ Нет ответа от Tilda API")
                print("  ⏸  Браузер открыт 30 сек")
                time.sleep(30)

            # ── Финальный лог ──
            print()
            print("  📡 Все запросы к Tilda:")
            for entry in network_log:
                print(entry)
            print(f"  Капча требовалась: {'ДА' if captcha_needed else 'НЕТ'}")
            print(f"  Форма отправлена:  {'ДА ✅' if tilda_ok else 'НЕТ ❌'}")
            print(f"  Тело запроса перехвачено: {'ДА' if captured_request_body else 'НЕТ'}")

            # ── Скрин финального состояния ──
            after_screen = os.path.join(SCREENSHOTS_DIR, f"{run_id}_after.png")
            page.screenshot(path=after_screen, full_page=False)
            print(f"  📸 Скрин: {after_screen}")

            if tilda_ok:
                result = (
                    f"✅ Заявка отправлена!\n\n"
                    f"👤 Имя: {full_name}\n"
                    f"📞 Телефон: +7 {phone}\n"
                    f"📧 Email: {email}\n"
                    f"🎨 Картина: {painting}\n"
                    f"🌐 Сайт: реплика.рф\n"
                    f"🤖 Капча: {'была' if captcha_needed else 'не требовалась'}"
                )
                time.sleep(3)
            elif captcha_needed:
                result = (
                    f"🤖 Капча не пройдена\n"
                    f"   Тело запроса перехвачено: {'да' if captured_request_body else 'нет'}\n"
                    f"   Прямой запрос: не помог"
                )
            else:
                result = (
                    f"❓ Форма не отправлена — нет ответов от API\n"
                    f"   Проверь скрин before — заполнилась ли форма"
                )

        except PlaywrightTimeoutError as e:
            try:
                page.screenshot(path=crash_screen)
                print(f"  📸 Скрин краша: {crash_screen}")
            except Exception:
                pass
            short_err = str(e).split("\n")[0][:150]
            result = f"❌ Timeout: {short_err}"
            print(f"\n  ❌ TIMEOUT — форма не ответила за 20 сек.")
            print(f"     Причина: {short_err}")
            print(f"\n  🔍 Браузер открыт 30 сек — посмотри Network/элементы...")
            time.sleep(30)

        except Exception as e:
            try:
                page.screenshot(path=crash_screen)
                print(f"  📸 Скрин краша: {crash_screen}")
            except Exception:
                pass
            short_err = str(e).split("\n")[0][:150]
            result = f"❌ Ошибка: {short_err}"
            print(f"\n  ❌ УПАЛО С ОШИБКОЙ:")
            print(f"     {short_err}")
            print(f"\n  🔍 Браузер открыт 30 сек — посмотри что на экране...")
            time.sleep(30)

        finally:
            try:
                context.close()
                browser.close()
            except Exception:
                pass

    print(f"\n{'='*50}")
    print("РЕЗУЛЬТАТ:")
    print(result)
    print(f"{'='*50}")
    return result


# ───────────────────────── ЗАПУСК ─────────────────────────────────

if __name__ == "__main__":
    run_test()