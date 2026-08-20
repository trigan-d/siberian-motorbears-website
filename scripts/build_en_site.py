#!/usr/bin/env python3
"""
Собрать английские копии основных страниц в site/en/ (те же пути + префикс /en/).
Запуск из корня репозитория: python3 scripts/build_en_site.py

Маршруты /en/routes/ собираются build_routes_en_manual.py из scripts/routes_en_fragments/ (без API).
Пересборку маршрутов при полной сборке можно отключить: SKIP_ROUTES_MT=1.
Чтобы убрать оставшийся русский в остальных /en/ страницах: python3 scripts/mt_en_site_pages.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
EN = SITE / "en"

from brand import ru_to_en_brand  # noqa: E402
from baribal_en_extra import BARIBAL_EXTRA  # noqa: E402
from baron_en_extra import BARON_EXTRA  # noqa: E402
from examples_en_extra import EXAMPLES_EXTRA  # noqa: E402
from mia_en_extra import MIA_EXTRA  # noqa: E402
from panda_en_extra import PANDA_EXTRA  # noqa: E402

# Общие замены для страниц вида site/<раздел>/index.html → site/en/<раздел>/index.html
UNIVERSAL_DEEP = [
    ('lang="ru"', 'lang="en"'),
    ('"addressLocality":"Кольцово"', '"addressLocality":"Koltsovo"'),
    ('"addressRegion":"Новосибирская область"', '"addressRegion":"Novosibirsk region"'),
    ('"streetAddress":"д. 6А"', '"streetAddress":"6A"'),
    (
        "<!-- Яндекс.Метрика: заменить 66322963 на номер счётчика во всём проекте -->",
        "<!-- Yandex.Metrica: replace 66322963 with your counter id site-wide -->",
    ),
    ("<!-- Яндекс.Метрика -->", "<!-- Yandex.Metrica -->"),
    (
        "<!-- VK Пиксель (Top.Mail.Ru), код 3727349 -->",
        "<!-- VK pixel (Top.Mail.Ru) id 3727349 -->",
    ),
    ('aria-label="Меню"', 'aria-label="Menu"'),
    ('aria-label="Хлебные крошки"', 'aria-label="Breadcrumbs"'),
    ('aria-label="Контакты"', 'aria-label="Contact"'),
    ('aria-label="Вконтакте"', 'aria-label="VK"'),
    ('aria-label="Электронная почта"', 'aria-label="Email"'),
    ('aria-label="Номер телефона"', 'aria-label="Phone"'),
    ('>Главная</a>', '>Home</a>'),
    ('>О нас</a>', '>About</a>'),
    ('>Производство</a>', '>Manufacturing</a>'),
    ('>Кемпер Барибал</a>', '>Baribal camper</a>'),
    ('>Автодом Панда</a>', '>Panda motorhome</a>'),
    ('>Примеры работ</a>', '>Portfolio</a>'),
    ('>Аренда</a>', '>Rental</a>'),
    ('>Барибал Барон</a>', '>Baribal Baron</a>'),
    ('>Панда Мия</a>', '>Panda Mia</a>'),
    ('>Маршруты</a>', '>Trip ideas</a>'),
    ('>Контакты</a>', '>Contact</a>'),
    ('>Телеграм</a>', '>Telegram</a>'),
    ('>Блог</a>', '>Blog</a>'),
    ('>реквизиты</a>', '>Legal</a>'),
    ('<meta property="og:locale" content="ru_RU">', '<meta property="og:locale" content="en_US">'),
]


def apply_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    for a, b in pairs:
        text = text.replace(a, b)
    return text


def fix_deep_en_asset_paths(text: str) -> str:
    """RU-страница в site/foo/ использует ../assets; копия в site/en/foo/ — ../../assets."""
    text = text.replace('href="../assets/', 'href="../../assets/')
    text = text.replace('src="../assets/', 'src="../../assets/')
    text = text.replace('href="../css/', 'href="../../css/')
    text = text.replace('href="../js/', 'href="../../js/')
    text = text.replace('src="../js/', 'src="../../js/')
    return text


PAGE_SEGMENTS = (
    "order",
    "rent",
    "contact",
    "legal",
    "baribal",
    "panda",
    "examples",
    "baron",
    "mia",
    "routes",
    "blog",
)


def fix_page_absolute_urls(text: str) -> str:
    """Canonical, og:url и пункты хлебных крошек → /en/… Без затрагивания /assets/."""
    for seg in PAGE_SEGMENTS:
        text = text.replace(
            f"https://siberian-motorbears.ru/{seg}/",
            f"https://siberian-motorbears.ru/en/{seg}/",
        )
    text = text.replace(
        '"item":"https://siberian-motorbears.ru/"',
        '"item":"https://siberian-motorbears.ru/en/"',
    )
    text = text.replace('"name":"Главная"', '"name":"Home"')
    text = text.replace(
        '"name":"Производство","item":"https://siberian-motorbears.ru/en/order/"',
        '"name":"Manufacturing","item":"https://siberian-motorbears.ru/en/order/"',
    )
    text = text.replace(
        '"name":"Аренда","item":"https://siberian-motorbears.ru/en/rent/"',
        '"name":"Rental","item":"https://siberian-motorbears.ru/en/rent/"',
    )
    text = text.replace(
        '"name":"Кемпер Барибал","item":"https://siberian-motorbears.ru/en/baribal/"',
        '"name":"Baribal camper","item":"https://siberian-motorbears.ru/en/baribal/"',
    )
    text = text.replace(
        '"name":"Автодом Панда","item":"https://siberian-motorbears.ru/en/panda/"',
        '"name":"Panda motorhome","item":"https://siberian-motorbears.ru/en/panda/"',
    )
    text = text.replace(
        '"name":"Примеры работ","item":"https://siberian-motorbears.ru/en/examples/"',
        '"name":"Portfolio","item":"https://siberian-motorbears.ru/en/examples/"',
    )
    text = text.replace(
        '"name":"Барибал Барон","item":"https://siberian-motorbears.ru/en/baron/"',
        '"name":"Baribal Baron","item":"https://siberian-motorbears.ru/en/baron/"',
    )
    text = text.replace(
        '"name":"Панда Мия","item":"https://siberian-motorbears.ru/en/mia/"',
        '"name":"Panda Mia","item":"https://siberian-motorbears.ru/en/mia/"',
    )
    text = text.replace(
        '"name":"Маршруты","item":"https://siberian-motorbears.ru/en/routes/"',
        '"name":"Trip ideas","item":"https://siberian-motorbears.ru/en/routes/"',
    )
    text = text.replace(
        '"name":"Контакты","item":"https://siberian-motorbears.ru/en/contact/"',
        '"name":"Contact","item":"https://siberian-motorbears.ru/en/contact/"',
    )
    text = text.replace(
        '"name":"Реквизиты","item":"https://siberian-motorbears.ru/en/legal/"',
        '"name":"Legal","item":"https://siberian-motorbears.ru/en/legal/"',
    )
    text = text.replace(
        '"url":"https://siberian-motorbears.ru"',
        '"url":"https://siberian-motorbears.ru/en"',
    )
    return text


def build_root_index() -> None:
    src = SITE / "index.html"
    dst = EN / "index.html"
    t = ru_to_en_brand(src.read_text(encoding="utf-8"))
    t = t.replace('lang="ru"', 'lang="en"')
    t = t.replace('href="assets/', 'href="../assets/')
    t = t.replace('src="assets/', 'src="../assets/')
    t = t.replace('href="css/', 'href="../css/')
    t = t.replace('href="js/', 'href="../js/')
    t = t.replace('src="js/', 'src="../js/')
    t = t.replace(
        '<link rel="canonical" href="https://siberian-motorbears.ru/">',
        '<link rel="canonical" href="https://siberian-motorbears.ru/en/">',
    )
    t = t.replace(
        '<meta property="og:url" content="https://siberian-motorbears.ru/">',
        '<meta property="og:url" content="https://siberian-motorbears.ru/en/">',
    )
    t = t.replace(
        '"url":"https://siberian-motorbears.ru"',
        '"url":"https://siberian-motorbears.ru/en"',
    )
    t = t.replace('<meta property="og:locale" content="ru_RU">', '<meta property="og:locale" content="en_US">')
    t = apply_pairs(t, UNIVERSAL_DEEP)
    # мета и контент главной (краткий перевод)
    pairs = [
        (
            "<title>Производство и прокат автодомов | Siberian motorbears</title>",
            "<title>Motorhome manufacturing & rental | Siberian motorbears</title>",
        ),
        (
            'content="Производство и прокат автодомов и кемперов в Новосибирске."',
            'content="Motorhome and camper manufacturing & rental in Novosibirsk."',
        ),
        (
            '<meta name="keywords" content="прокат автодомов, аренда автодомов, автодом, дом на колёсах, кемпер, изготовление кемперов, продажа автодомов, Siberian motorbears, Новосибирск, аренда автодома Алтай, прокат кемпера Байкал">',
            '<meta name="keywords" content="motorhome rental, camper hire, motorhome, caravan, camper van, camper builds, motorhomes for sale, Siberian motorbears, Novosibirsk, Altai motorhome rental, Baikal camper rental">',
        ),
        (
            '<meta property="og:title" content="Производство и прокат автодомов | Siberian motorbears">',
            '<meta property="og:title" content="Motorhome manufacturing & rental | Siberian motorbears">',
        ),
        (
            '<meta property="og:description" content="Производство и аренда автодомов в Новосибирске.">',
            '<meta property="og:description" content="Motorhome manufacturing and rental in Novosibirsk.">',
        ),
        (
            '<meta name="twitter:title" content="Производство и прокат автодомов | Siberian motorbears">',
            '<meta name="twitter:title" content="Motorhome manufacturing & rental | Siberian motorbears">',
        ),
        (
            '<meta name="twitter:description" content="Производство и прокат автодомов.">',
            '<meta name="twitter:description" content="Motorhome manufacturing and rental.">',
        ),
        ('aria-label="Меню"', 'aria-label="Menu"'),
        ('>О нас</a>', '>About</a>'),
        ('>Производство</a>', '>Manufacturing</a>'),
        ('>Кемпер Барибал</a>', '>Baribal camper</a>'),
        ('>Автодом Панда</a>', '>Panda motorhome</a>'),
        ('>Примеры работ</a>', '>Portfolio</a>'),
        ('>Аренда</a>', '>Rental</a>'),
        ('>Барибал Барон</a>', '>Baribal Baron</a>'),
        ('>Панда Мия</a>', '>Panda Mia</a>'),
        ('>Маршруты</a>', '>Trip ideas</a>'),
        ('>Контакты</a>', '>Contact</a>'),
        ('>Сообщество VK</a>', '>VK community</a>'),
        ('>Телеграм</a>', '>Telegram</a>'),
        ('>Блог</a>', '>Blog</a>'),
        ('>реквизиты</a>', '>Legal</a>'),
        ('aria-label="Контакты"', 'aria-label="Contact"'),
        ('aria-label="Вконтакте"', 'aria-label="VK"'),
        ('aria-label="Электронная почта"', 'aria-label="Email"'),
        ('aria-label="Номер телефона"', 'aria-label="Phone"'),
        (
            '<h1 class="mb-0" style="font-size: 1.5rem;">Вас приветствует команда <strong class="brand-name">Siberian motorbears</strong>:<br>производство и прокат автодомов.</h1>',
            '<h1 class="mb-0" style="font-size: 1.5rem;">The <strong class="brand-name">Siberian&nbsp;motorbears</strong> team welcomes you:<br>motorhome manufacturing & rental.</h1>',
        ),
        (
            '<p class="lead" style="margin-top: 1rem; font-weight: 600;">Мы занимаемся автодомами с 2020-го года. У нас вы можете:<br>- купить готовый автодом или кемпер<br>- заказать изготовление автодома по своему вкусу<br>- арендовать автодом и поехать на Алтай, Байкал, по Сибири, или <a href="routes/" class="link--inline">куда угодно!</a></p>',
            '<p class="lead" style="margin-top: 1rem; font-weight: 600;">We have been building and renting motorhomes since 2020. With us you can:<br>- buy a finished motorhome or camper<br>- commission a motorhome built to your taste<br>- rent a motorhome and drive to the Altai, Lake Baikal, across Siberia, or <a href="routes/" class="link--inline">wherever you like!</a></p>',
        ),
        (
            '<div class="hero__img"><img src="../assets/img/80cc22b7-33a2-406d-a13d-413e10475049-3529231.jpeg" alt="Кемпер и автодом Siberian motorbears на природе — производство и прокат в Новосибирске" width="800" height="533"></div>',
            '<div class="hero__img"><img src="../assets/img/80cc22b7-33a2-406d-a13d-413e10475049-3529231.jpeg" alt="Siberian motorbears camper and motorhome outdoors — built and rented in Novosibirsk" width="800" height="533"></div>',
        ),
        (
            '          <p class="text-muted" style="margin-top: 1rem;">\n            Почти сразу мы решили, что обычные автодома нам скучны. Так появились сибирские моторизированные медведи :)<br><br>\n            Они бывают похожи на автодома, прицепы-дачи, кемперы, караваны, кастенвагены и т.д. Иной и не распознает сразу, что перед ним не бездушная машина, а живое существо с горячим сердцем. Но мы-то знаем. Каждый моторизированный медведь обладает своим неповторимым характером, повадками, умениями. Они бывают веселы и рвутся в бой. А иногда хандрят, болеют или капризничают. Некоторые даже шутят. Они меняются с возрастом, учатся новому, обрастают жирком или мышцами, матереют, стареют. Но любой моторизированный медведь всегда готов к путешествиям и приключениям. Ибо это их главная страсть и суть. Проявите к нему уважение, уделите толику внимания, и он будет рад разделить эту страсть с вами.\n          </p>',
            '          <p class="text-muted" style="margin-top: 1rem;">\n            Almost from the start we felt ordinary motorhomes were too dull for us — so Siberian motorbears came to be :)<br><br>\n            They may look like motorhomes, trailer cabins, campers, caravans, camper vans, and so on. Not everyone sees at once that this is not a soulless machine but a living creature with a warm heart — but we do. Every motorbear has its own character, habits, and talents. Some days they are cheerful and raring to go; other times they are moody, under the weather, or picky. Some even joke. They change with age, learn new tricks, put on weight or muscle, grow tougher, grow older. Yet any motorbear is always ready for travel and adventure — that is their passion and their nature. Show yours respect, give it a little attention, and it will gladly share that passion with you.\n          </p>',
        ),
        (
            '<h2 class="section-title">Наши актуальные модели:</h2>',
            '<h2 class="section-title">Our current models:</h2>',
        ),
        (
            '<h3>Внедорожный кемпер «Барибал»</h3>',
            '<h3>Off-road camper «Baribal»</h3>',
        ),
        (
            '<p class="product-block__text">Барибал представляет собой аналог прицепа-капли (teardrop), смонтированный на бортовой платформе грузовика-полуторки.</p>',
            '<p class="product-block__text">Baribal is essentially a teardrop-trailer layout mounted on the flatbed of a light truck.</p>',
        ),
        (
            '<p class="product-block__text">Это маленький и юркий медведь. Он понравится путешественникам, которые любят открывать новые безлюдные маршруты и предпочитают весь день находиться на свежем воздухе, а не в тесном и душном фургоне.</p>',
            '<p class="product-block__text">This is a small, nimble bear. It suits travellers who like to find empty backroads and would rather spend the whole day outdoors than in a cramped, stuffy van body.</p>',
        ),
        ('Заказать от 700 000 ₽', 'Order from 700 000 ₽'),
        ('Арендовать от 11 000 ₽/сут', 'Rent from 11 000 ₽/day'),
        ('<h3>Интегрированный автодом «Панда»</h3>', '<h3>Integrated motorhome «Panda»</h3>'),
        (
            '<p class="product-block__text">Это просторный интегрированный автодом с полноростовым проходом между кабиной и жилым отсеком.</p>',
            '<p class="product-block__text">This is a spacious integrated motorhome with full standing-height walk-through between the cab and the living area.</p>',
        ),
        (
            '<p class="product-block__text">Удачная планировка жилого отсека позволила с комфортом разместить сидячие и спальные места для пяти пассажиров, полноценную кухню и санузел.</p>',
            '<p class="product-block__text">A well-planned living layout comfortably fits seating and sleeping for five passengers, a full kitchen, and a bathroom.</p>',
        ),
        (
            '<p class="product-block__text">И при этом внутри получилось не тесно, а вполне просторно.</p>',
            '<p class="product-block__text">Even so, it does not feel cramped inside — there is plenty of room.</p>',
        ),
        ('Заказать от 1 300 000 ₽', 'Order from 1 300 000 ₽'),
        ('Арендовать от 15 000 ₽/сут', 'Rent from 15 000 ₽/day'),
        ('<h2 class="section-title">Наши друзья и партнёры</h2>', '<h2 class="section-title">Friends & partners</h2>'),
        ('alt="Внедорожный кемпер Барибал — фото"', 'alt="Off-road Baribal camper — photo"'),
        ('alt="Интегрированный автодом Панда — фото"', 'alt="Integrated Panda motorhome — photo"'),
        (
            '<img src="../assets/img/a083377a-b748-4c5a-9010-561d6fc078da-2727884.png" alt="Логотип партнёра — Футбольный центр">',
            '<img src="../assets/img/a083377a-b748-4c5a-9010-561d6fc078da-2727884.png" alt="Partner logo — football centre">',
        ),
        (
            '<img src="../assets/img/1dbb5bd7-12c1-48a1-8137-f14791514ba2-2727883.png" alt="Логотип Camper33 — производство и аренда кемперов">',
            '<img src="../assets/img/1dbb5bd7-12c1-48a1-8137-f14791514ba2-2727883.png" alt="Camper33 logo — camper builds & rental">',
        ),
        (
            '<img src="../assets/img/c220b21c-0378-4eda-b60c-451f6e565652-2727886.png" alt="Логотип партнёра — автосервис в Новосибирске">',
            '<img src="../assets/img/c220b21c-0378-4eda-b60c-451f6e565652-2727886.png" alt="Partner logo — workshop in Novosibirsk">',
        ),
        (
            '<img src="../assets/img/c87752b6-3016-4414-a194-902c21f670db-2727885.png" alt="Логотип Фургон-центр — кузовной ремонт">',
            '<img src="../assets/img/c87752b6-3016-4414-a194-902c21f670db-2727885.png" alt="Furgon-centre logo — body repair">',
        ),
        (
            '<img src="../assets/img/8e46a3ad-b3f7-4d82-b11a-d908ddd7a048-2727888.gif" alt="Логотип партнёра — внедорожная техника">',
            '<img src="../assets/img/8e46a3ad-b3f7-4d82-b11a-d908ddd7a048-2727888.gif" alt="Partner logo — off-road gear">',
        ),
        (
            '<img src="../assets/img/97f55e67-4116-4821-83c6-f78eac0e64e8-2727887.png" alt="Логотип партнёра — мебель для автодомов">',
            '<img src="../assets/img/97f55e67-4116-4821-83c6-f78eac0e64e8-2727887.png" alt="Partner logo — motorhome furniture">',
        ),
        (
            '<img src="../assets/img/ce2aa79a-43b4-4bbe-8b5f-2bd8e6bb5379-14643815.png" alt="Логотип НСК Конфи — матрасы">',
            '<img src="../assets/img/ce2aa79a-43b4-4bbe-8b5f-2bd8e6bb5379-14643815.png" alt="NSK Confy logo — mattresses">',
        ),
        (
            '<img src="../assets/img/8897832d-86ae-4e0d-baac-0a3b6ce7b771-2727889.jpeg" alt="Стать партнёром Siberian motorbears">',
            '<img src="../assets/img/8897832d-86ae-4e0d-baac-0a3b6ce7b771-2727889.jpeg" alt="Become a partner of Siberian motorbears">',
        ),
        (
            '<span class="partner-card__title">Футбольный центр, неравнодушный к медведям</span>',
            '<span class="partner-card__title">A football centre that cares about bears</span>',
        ),
        (
            '<span class="partner-card__title">Заводчик и дрессировщик моторизированных медведей</span>',
            '<span class="partner-card__title">Motorbear breeder & trainer</span>',
        ),
        (
            '<span class="partner-card__title">Ветеринары для моторизированных медведей</span>',
            '<span class="partner-card__title">Vets for motorbears</span>',
        ),
        (
            '<span class="partner-card__title">Если медведю намяли бока</span>',
            '<span class="partner-card__title">If your motorbear took a hit</span>',
        ),
        (
            '<span class="partner-card__title">Если медведю тесно на асфальте</span>',
            '<span class="partner-card__title">If asphalt feels tight</span>',
        ),
        (
            '<span class="partner-card__title">Мебель для медведя</span>',
            '<span class="partner-card__title">Furniture for your motorbear</span>',
        ),
        (
            '<span class="partner-card__title">Матрас для мишкиной кроватки</span>',
            '<span class="partner-card__title">Mattress for the den</span>',
        ),
        (
            '<span class="partner-card__title">Хотите с нами дружить? Напишите нам на siberian.motorbears@gmail.com</span>',
            '<span class="partner-card__title">Want to team up? Email siberian.motorbears@gmail.com</span>',
        ),
        ('aria-label="Назад"', 'aria-label="Previous"'),
        ('aria-label="Вперёд"', 'aria-label="Next"'),
    ]
    for a, b in pairs:
        t = t.replace(a, b)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t, encoding="utf-8")
    print("Wrote", dst.relative_to(REPO))


def copy_translate_deep(rel: str, extra: list[tuple[str, str]] | None = None) -> None:
    src = SITE / rel
    dst = EN / rel
    t = ru_to_en_brand(src.read_text(encoding="utf-8"))
    t = apply_pairs(t, UNIVERSAL_DEEP)
    t = fix_deep_en_asset_paths(t)
    t = fix_page_absolute_urls(t)
    if extra:
        t = apply_pairs(t, extra)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t, encoding="utf-8")
    print("Wrote", dst.relative_to(REPO))


def routes_en() -> None:
    import os
    import subprocess
    import sys

    if os.environ.get("SKIP_ROUTES_MT"):
        print("SKIP_ROUTES_MT set — skipping build_routes_en_manual.py")
        return
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_routes_en_manual.py")],
        cwd=str(REPO),
    )
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def main() -> None:
    EN.mkdir(parents=True, exist_ok=True)
    build_root_index()

    order_extra = [
        (
            "<title>Изготовление автодомов на заказ, мелкосерийное производство | Siberian motorbears</title>",
            "<title>Custom motorhomes & small-batch builds | Siberian motorbears</title>",
        ),
        (
            'content="Изготовление автодомов на заказ, мелкосерийное производство. Внедорожный кемпер Барибал от 700 000 ₽, автодом Панда от 1 300 000 ₽. Новосибирск. Переоборудование фургонов. Срок 2–3 месяца. Узнайте цены."',
            'content="Custom motorhomes and small-batch production. Baribal camper from 700 000 ₽, Panda motorhome from 1 300 000 ₽. Novosibirsk. Van conversions. Lead time about 2–3 months."',
        ),
        (
            '<meta property="og:title" content="Изготовление автодомов на заказ, мелкосерийное производство | Siberian motorbears">',
            '<meta property="og:title" content="Custom motorhomes & small-batch builds | Siberian motorbears">',
        ),
        (
            '<meta property="og:description" content="Изготовление автодомов на заказ, мелкосерийное производство. Кемпер Барибал от 700 000 ₽, автодом Панда от 1 300 000 ₽. Новосибирск. Переоборудование фургонов. Срок 2–3 месяца."',
            '<meta property="og:description" content="Custom motorhomes and small-batch builds. Baribal from 700 000 ₽, Panda from 1 300 000 ₽. Novosibirsk. Van conversions. About 2–3 months lead time."',
        ),
        (
            '<meta name="twitter:title" content="Изготовление автодомов на заказ, мелкосерийное производство | Siberian motorbears">',
            '<meta name="twitter:title" content="Custom motorhomes & small-batch builds | Siberian motorbears">',
        ),
        (
            '<meta name="twitter:description" content="Изготовление автодомов на заказ, мелкосерийное производство. Кемпер Барибал от 700 000 ₽, автодом Панда от 1 300 000 ₽. Новосибирск. Переоборудование фургонов. Срок 2–3 месяца."',
            '<meta name="twitter:description" content="Custom motorhomes and small-batch builds. Baribal from 700 000 ₽, Panda from 1 300 000 ₽. Novosibirsk. Van conversions. About 2–3 months lead time."',
        ),
        ("<span>Производство</span>", "<span>Manufacturing</span>"),
        (
            '<h1 style="font-size: 1.35rem;">Изготовление автодомов на заказ, мелкосерийное производство</h1>',
            '<h1 style="font-size: 1.35rem;">Custom motorhomes & small-batch production</h1>',
        ),
        (
            '<p class="text-muted">Наша команда накопила немалый опыт интенсивной эксплуатации и проката автодомов. Наши машины работают в любую погоду, в самых разных условиях, с большими пробегами и почти без перерыва.</p>',
            '<p class="text-muted">Our team has built up substantial hands-on experience operating motorhomes intensively and renting them out. Our vehicles work in any weather, in all kinds of conditions, with long mileages and almost no downtime.</p>',
        ),
        (
            '<p class="text-muted">Мы потратили много времени и сил на обслуживание, подготовку, доработку, ремонт. Это касается ходовой части, жилых отсеков, мебели, оборудования.</p>',
            '<p class="text-muted">We have invested a great deal of time and effort in servicing, preparation, upgrades, and repairs — for the running gear, living modules, furniture, and equipment.</p>',
        ),
        (
            '<p class="text-muted">Мы успели познакомиться с множеством людей и компаний, которые проектируют, строят, создают, обслуживают, тюнингуют, поставляют автодома и смежные товары.</p>',
            '<p class="text-muted">Along the way we have got to know many people and companies who design, build, create, service, tune, and supply motorhomes and related products.</p>',
        ),
        ('<p class="text-muted">В общем, нам кажется, что мы в этом кое-что понимаем :)</p>', '<p class="text-muted">So we like to think we know the topic reasonably well :)</p>'),
        ('<p class="text-muted">Если вы желаете:</p>', '<p class="text-muted">If you want to:</p>'),
        ('<li>купить один из наших автодомов или заказать похожий,</li>', '<li>buy one of our builds or commission something similar,</li>'),
        ('<li>построить свой собственный проект,</li>', '<li>build your own project,</li>'),
        ('<li>переоборудовать или доработать ваш автодом,</li>', '<li>convert or upgrade your motorhome,</li>'),
        ('<li>да и просто обратиться за советом и консультацией,</li>', '<li>or simply get in touch for advice and a consultation,</li>'),
        ('<p class="mt-1"><a href="../examples/" class="btn btn--secondary">Примеры работ</a></p>', '<p class="mt-1"><a href="../examples/" class="btn btn--secondary">Portfolio</a></p>'),
        ('<h2 class="section-title">Наши актуальные модели:</h2>', '<h2 class="section-title">Our current models:</h2>'),
        ('<h3>Внедорожный кемпер «Барибал»</h3>', '<h3>Off-road camper «Baribal»</h3>'),
        (
            '<p class="product-block__text">Барибал представляет собой аналог прицепа-капли (teardrop), смонтированный на бортовой платформе грузовика-полуторки.</p>',
            '<p class="product-block__text">Baribal is essentially a teardrop-trailer layout mounted on the flatbed of a light truck.</p>',
        ),
        (
            '<p class="product-block__text">Это маленький и юркий медведь. Он понравится путешественникам, которые любят открывать новые безлюдные маршруты и предпочитают весь день находиться на свежем воздухе, а не в тесном и душном фургоне.</p>',
            '<p class="product-block__text">This is a small, nimble bear. It suits travellers who like to find empty backroads and would rather spend the whole day outdoors than in a cramped, stuffy van body.</p>',
        ),
        ('Заказать от 700 000 ₽', 'Order from 700 000 ₽'),
        ('<h3>Интегрированный автодом «Панда»</h3>', '<h3>Integrated motorhome «Panda»</h3>'),
        (
            '<p class="product-block__text">Это просторный интегрированный автодом с полноростовым проходом между кабиной и жилым отсеком.</p>',
            '<p class="product-block__text">This is a spacious integrated motorhome with full standing-height walk-through between the cab and the living area.</p>',
        ),
        (
            '<p class="product-block__text">Удачная планировка жилого отсека позволила с комфортом разместить сидячие и спальные места для пяти пассажиров, полноценную кухню и санузел. И при этом внутри получилось не тесно, а вполне просторно.</p>',
            '<p class="product-block__text">A well-planned living layout comfortably fits seating and sleeping for five passengers, a full kitchen, and a bathroom — and the interior still feels roomy, not cramped.</p>',
        ),
        ('Заказать от 1 300 000 ₽', 'Order from 1 300 000 ₽'),
        (
            '<meta name="keywords" content="изготовление автодомов на заказ, мелкосерийное производство автодомов, кемпер на заказ, Барибал, Панда, Новосибирск, переоборудование фургонов">',
            '<meta name="keywords" content="custom motorhomes, small-batch builds, camper commission, Baribal, Panda, Novosibirsk, van conversion">',
        ),
        (
            '<img src="../../assets/img/0717e98b-432e-4c96-b594-c889a0686f70-15526810.jpeg" alt="Изготовление автодомов на заказ, мелкосерийное производство — Барибал и Панда" width="800" height="533">',
            '<img src="../../assets/img/0717e98b-432e-4c96-b594-c889a0686f70-15526810.jpeg" alt="Custom motorhomes and small-batch builds — Baribal and Panda" width="800" height="533">',
        ),
        ('alt="Кемпер Барибал"', 'alt="Baribal camper"'),
        (
            'alt="Интегрированный автодом Панда — производство на заказ"',
            'alt="Integrated Panda motorhome — built to order"',
        ),
        (
            '<p class="text-muted">позвоните по телефону <a href="tel:+79134602050" class="link--contact">+7 913 460-20-50</a>, напишите на почту <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a>, или в <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a>.</p>',
            '<p class="text-muted">Call <a href="tel:+79134602050" class="link--contact">+7 913 460-20-50</a>, email <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a>, or Telegram <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a>.</p>',
        ),
    ]
    copy_translate_deep("order/index.html", order_extra)

    rent_extra = [
        (
            "<title>Аренда автодомов — Сибирь, Алтай, Байкал | Siberian motorbears</title>",
            "<title>Motorhome rental — Siberia, Altai, Baikal | Siberian motorbears</title>",
        ),
        (
            'content="Прокат автодомов и кемперов из Новосибирска: маршруты по Сибири, Горному Алтаю, Байкалу. Барибал Барон от 11 000 ₽/сутки, Панда Мия от 15 000 ₽/сутки. Полная комплектация. Бронируйте по телефону."',
            'content="Motorhome & camper rental from Novosibirsk: Siberia, Altai, Baikal. Baribal Baron from 11 000 ₽/day, Panda Mia from 15 000 ₽/day. Fully equipped. Book by phone."',
        ),
        (
            '<meta property="og:title" content="Аренда автодомов — Сибирь, Алтай, Байкал | Siberian motorbears">',
            '<meta property="og:title" content="Motorhome rental — Siberia, Altai, Baikal | Siberian motorbears">',
        ),
        (
            '<meta property="og:description" content="Прокат автодомов и кемперов из Новосибирска: маршруты по Сибири, Горному Алтаю, Байкалу. Барибал Барон от 11 000 ₽/сутки, Панда Мия от 15 000 ₽/сутки. Полная комплектация. Бронируйте по телефону."',
            '<meta property="og:description" content="Motorhome & camper rental from Novosibirsk: Siberia, Altai, Baikal. Baribal Baron from 11 000 ₽/day, Panda Mia from 15 000 ₽/day. Fully equipped."',
        ),
        (
            '<meta name="twitter:title" content="Аренда автодомов — Сибирь, Алтай, Байкал | Siberian motorbears">',
            '<meta name="twitter:title" content="Motorhome rental — Siberia, Altai, Baikal | Siberian motorbears">',
        ),
        (
            '<meta name="twitter:description" content="Прокат автодомов и кемперов из Новосибирска: маршруты по Сибири, Горному Алтаю, Байкалу. Барибал Барон от 11 000 ₽/сутки, Панда Мия от 15 000 ₽/сутки. Полная комплектация. Бронируйте по телефону."',
            '<meta name="twitter:description" content="Motorhome & camper rental from Novosibirsk: Siberia, Altai, Baikal. Fully equipped."',
        ),
        (
            '<meta name="keywords" content="прокат автодомов, аренда автодомов, Алтай, Байкал, Сибирь, Новосибирск, Барибал Барон, Панда Мия">',
            '<meta name="keywords" content="motorhome rental, camper hire, Altai, Baikal, Siberia, Novosibirsk, Baribal Baron, Panda Mia">',
        ),
        (
            '  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Как забронировать кемпер или автодом?","acceptedAnswer":{"@type":"Answer","text":"Позвоните по телефону +7 (913) 460-20-50, напишите на siberian.motorbears@gmail.com или в Telegram — мы обсудим даты и условия."}},{"@type":"Question","name":"Что входит в стоимость аренды?","acceptedAnswer":{"@type":"Answer","text":"В стоимость входит полная комплектация: постельное бельё и полотенца, посуда, кухонная утварь, масло, специи, чай, кофе, полные баки топлива и воды. С собой нужны только одежда и еда."}},{"@type":"Question","name":"Куда можно поехать?","acceptedAnswer":{"@type":"Answer","text":"Мы проводим вас в путь по НСО, на Алтай, в Шерегеш, на Байкал или в другое направление по договорённости. Если вы ещё не определились с маршрутом, посмотрите несколько советов от нас: куда можно поехать на автодоме из Новосибирска (на странице Маршруты)."}},{"@type":"Question","name":"Какие права нужны для управления?","acceptedAnswer":{"@type":"Answer","text":"Для управления автодомом или кемпером достаточно прав категории B."}},{"@type":"Question","name":"Какой минимальный срок аренды?","acceptedAnswer":{"@type":"Answer","text":"Минимальный срок аренды уточняйте по телефону +7 (913) 460-20-50 или в переписке — мы подберём удобный вариант."}},{"@type":"Question","name":"Откуда забирать и куда возвращать автодом?","acceptedAnswer":{"@type":"Answer","text":"Выдача и возврат — в Новосибирске (Кольцово). Возможна доставка до аэропорта или ж/д вокзала по согласованию."}}]}</script>',
            '  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How do I book a camper or motorhome?","acceptedAnswer":{"@type":"Answer","text":"Call +7 (913) 460-20-50, email siberian.motorbears@gmail.com or Telegram — we will agree dates and terms."}},{"@type":"Question","name":"What is included in the rental price?","acceptedAnswer":{"@type":"Answer","text":"Full outfitting: bed linen and towels, dishes, kitchenware, oil, spices, tea, coffee, full fuel and water tanks. You only need clothes and food."}},{"@type":"Question","name":"Where can we go?","acceptedAnswer":{"@type":"Answer","text":"Across the region, Altai, Sheregesh, Baikal or elsewhere by arrangement. If you are still choosing a route, see trip ideas from Novosibirsk on our Trip ideas page."}},{"@type":"Question","name":"Which driving licence do I need?","acceptedAnswer":{"@type":"Answer","text":"Category B is enough for our motorhomes and campers."}},{"@type":"Question","name":"What is the minimum rental period?","acceptedAnswer":{"@type":"Answer","text":"Ask by phone +7 (913) 460-20-50 or in messages — we will find what works."}},{"@type":"Question","name":"Where is pick-up and return?","acceptedAnswer":{"@type":"Answer","text":"Handover and return in Novosibirsk (Koltsovo). Airport or rail station delivery possible by arrangement."}}]}</script>',
        ),
        ("<span>Аренда</span>", "<span>Rental</span>"),
        (
            '<h1 style="font-size: 1.35rem;">Аренда автодомов: Сибирь, Алтай, Байкал</h1>',
            '<h1 style="font-size: 1.35rem;">Motorhome rental: Siberia, Altai, Baikal</h1>',
        ),
        (
            '<p class="text-muted">Наши автодома и кемперы доступны для проката с выдачей в Новосибирске.</p>',
            '<p class="text-muted">Our motorhomes and campers are available for rent with handover in Novosibirsk.</p>',
        ),
        (
            '<p class="text-muted">Чтобы поближе познакомиться с сибирским моторизированным медведем и взять его с собой в путешествие, позвоните по телефону <a href="tel:+79134602050" class="link--contact">+7 913 460-20-50</a>, напишите на почту <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a>, или в <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a>.</p>',
            '<p class="text-muted">To meet our motorbears and take one on a trip, call <a href="tel:+79134602050" class="link--contact">+7 913 460-20-50</a>, email <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a>, or Telegram <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a>.</p>',
        ),
        (
            '<p class="text-muted">Если вы понравитесь друг другу, то мы будем рады подготовить всё необходимое для вашего путешествия и проводить вас в путь по НСО, на Алтай, в Шерегеш, на Байкал, или куда ещё вам с медведем захочется поехать. А если вы ещё не решили, куда хотите отправиться — <a href="../routes/" class="link--inline">спросите у нас, и мы подскажем пару идей</a>.</p>',
            '<p class="text-muted">If we are a good match, we will be glad to prepare everything you need for your trip and send you on your way across the Novosibirsk region, to the Altai, Sheregesh, Baikal, or wherever you and your bear feel like going. If you have not chosen a destination yet — <a href="../routes/" class="link--inline">ask us and we will suggest a few ideas</a>.</p>',
        ),
        (
            '<p class="text-muted">Наши медведи всегда выходят в рейс в полной комплектации: чистое постельное бельё и полотенца на всех, посуда и столовые принадлежности, мусорные пакетики, туалетная бумага, кухонная утварь, масло, специи, чай, кофе, сладости, полные баки топлива и воды. С собой вам надо взять только одежду, еду и тягу к приключениям!</p>',
            '<p class="text-muted">Our bears always leave on a trip fully equipped: clean bed linen and towels for everyone, dishes and tableware, bin bags, toilet paper, kitchen tools, oil, spices, tea, coffee, snacks, and full fuel and water tanks. All you need to bring is clothes, food, and a taste for adventure!</p>',
        ),
        ('<p class="mt-1"><a href="../routes/" class="btn btn--secondary">Маршруты</a></p>', '<p class="mt-1"><a href="../routes/" class="btn btn--secondary">Trip ideas</a></p>'),
        (
            'alt="Аренда автодома — путешествие по Сибири, Алтаю и Байкалу"',
            'alt="Motorhome rental — travel across Siberia, Altai, and Baikal"',
        ),
        ('alt="Барибал Барон"', 'alt="Baribal Baron"'),
        ('alt="Автодом Панда Мия в прокате — фото"', 'alt="Panda Mia motorhome — rental photo"'),
        ('<h2 class="section-title">Доступны для проката:</h2>', '<h2 class="section-title">Available for rent:</h2>'),
        ('<h3>Аренда внедорожного кемпера «Барибал Барон»</h3>', '<h3>Off-road camper «Baribal Baron» rental</h3>'),
        (
            '<div class="product-block__text">\n              <p>Барибал представляет собой аналог прицепа-капли (teardrop), смонтированный на бортовой платформе грузовика-полуторки.</p>\n              <p>Это маленький и юркий медведь. Он понравится путешественникам, которые любят открывать новые безлюдные маршруты и предпочитают весь день находиться на свежем воздухе, а не в тесном и душном фургоне.</p>\n            </div>',
            '<div class="product-block__text">\n              <p>Baribal is essentially a teardrop-trailer layout mounted on the flatbed of a light truck.</p>\n              <p>This is a small, nimble bear. It suits travellers who like to find empty backroads and would rather spend the whole day outdoors than in a cramped, stuffy van body.</p>\n            </div>',
        ),
        ('Арендовать от 11 000 ₽/сутки', 'Rent from 11 000 ₽/day'),
        ('<h3>Аренда интегрированного автодома «Панда Мия»</h3>', '<h3>Integrated motorhome «Panda Mia» rental</h3>'),
        (
            '<div class="product-block__text">\n              <p>Это просторный интегрированный автодом с полноростовым проходом между кабиной и жилым отсеком.</p>\n              <p>Удачная планировка жилого отсека позволила с комфортом разместить сидячие и спальные места для пяти пассажиров, полноценную кухню и санузел.</p>\n              <p>И при этом внутри получилось не тесно, а вполне просторно.</p>\n            </div>',
            '<div class="product-block__text">\n              <p>This is a spacious integrated motorhome with full standing-height walk-through between the cab and the living area.</p>\n              <p>A well-planned living layout comfortably fits seating and sleeping for five passengers, a full kitchen, and a bathroom.</p>\n              <p>Even so, it does not feel cramped inside — there is plenty of room.</p>\n            </div>',
        ),
        ('Арендовать от 15 000 ₽/сутки', 'Rent from 15 000 ₽/day'),
        ('title="Видео об аренде автодомов"', 'title="Motorhome rental video"'),
        ('<h2 class="section-title section-title--small">Фотоотчёты с путешествий на автодомах Siberian motorbears</h2>', '<h2 class="section-title section-title--small">Travel photo & video reports — trips in Siberian motorbears motorhomes</h2>'),
        ('<h2 class="section-title" id="faq-title">Частые вопросы об аренде</h2>', '<h2 class="section-title" id="faq-title">Rental FAQ</h2>'),
        ('<h3 class="faq__q">Как забронировать кемпер или автодом?</h3>', '<h3 class="faq__q">How do I book?</h3>'),
        (
            '<p class="faq__a">Позвоните по телефону <a href="tel:+79134602050" class="link--contact">+7 (913) 460-20-50</a>, напишите на <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a> или в <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a> — мы обсудим даты и условия.</p>',
            '<p class="faq__a">Call <a href="tel:+79134602050" class="link--contact">+7 (913) 460-20-50</a>, email <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a>, or Telegram <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a> — we will agree dates and terms.</p>',
        ),
        ('<h3 class="faq__q">Что входит в стоимость аренды?</h3>', '<h3 class="faq__q">What is included?</h3>'),
        (
            '<p class="faq__a">В стоимость входит полная комплектация: постельное бельё и полотенца, посуда, кухонная утварь, масло, специи, чай, кофе, полные баки топлива и воды. С собой нужны только одежда и еда.</p>',
            '<p class="faq__a">The price includes full outfitting: bed linen and towels, dishes, kitchenware, oil, spices, tea, coffee, full fuel and water tanks. You only need to bring clothes and food.</p>',
        ),
        ('<h3 class="faq__q">Куда можно поехать?</h3>', '<h3 class="faq__q">Where can we go?</h3>'),
        (
            '<p class="faq__a">Мы проводим вас в путь по НСО, на Алтай, в Шерегеш, на Байкал или в другое направление по договорённости. Если вы ещё не определились с маршрутом, посмотрите несколько советов от нас: <a href="../routes/" class="link--inline">куда можно поехать на автодоме из Новосибирска</a>.</p>',
            '<p class="faq__a">Across the region, Altai, Sheregesh, Baikal, or elsewhere by arrangement. Need ideas? See <a href="../routes/" class="link--inline">trip ideas from Novosibirsk</a>.</p>',
        ),
        ('<h3 class="faq__q">Какие права нужны для управления?</h3>', '<h3 class="faq__q">Which driving licence?</h3>'),
        ('<p class="faq__a">Для управления автодомом или кемпером достаточно прав категории B.</p>', '<p class="faq__a">Category B is enough for our motorhomes and campers.</p>'),
        ('<h3 class="faq__q">Какой минимальный срок аренды?</h3>', '<h3 class="faq__q">Minimum rental length?</h3>'),
        (
            '<p class="faq__a">Минимальный срок аренды уточняйте по телефону <a href="tel:+79134602050" class="link--contact">+7 (913) 460-20-50</a> или в переписке — мы подберём удобный вариант.</p>',
            '<p class="faq__a">Ask by phone <a href="tel:+79134602050" class="link--contact">+7 (913) 460-20-50</a> or in messages — we will find what works.</p>',
        ),
        ('<h3 class="faq__q">Откуда забирать и куда возвращать автодом?</h3>', '<h3 class="faq__q">Pick-up and return?</h3>'),
        ('<p class="faq__a">Выдача и возврат — в Новосибирске. Возможна доставка до аэропорта или ж/д вокзала по согласованию.</p>', '<p class="faq__a">Handover and return in Novosibirsk. Airport or rail station delivery possible by arrangement.</p>'),
    ]
    copy_translate_deep("rent/index.html", rent_extra)

    contact_extra = [
        (
            "<title>Контакты — адрес, телефон, как заказать автодом или аренду | Siberian motorbears</title>",
            "<title>Contacts — address, phone, book a build or rental | Siberian motorbears</title>",
        ),
        (
            'content="Контактная информация Siberian motorbears: адрес в Кольцово (Новосибирская область), телефон +7 (913) 460-20-50, email, VK, Telegram. Закажите производство кемпера или бронь аренды."',
            'content="Siberian motorbears: address in Koltsovo (Novosibirsk region), phone +7 (913) 460-20-50, email, VK, Telegram. Book manufacturing or rental."',
        ),
        (
            '<meta property="og:title" content="Контакты — адрес, телефон, как заказать автодом или аренду | Siberian motorbears">',
            '<meta property="og:title" content="Contacts — address, phone, book a build or rental | Siberian motorbears">',
        ),
        (
            '<meta property="og:description" content="Контактная информация Siberian motorbears: адрес в Кольцово (Новосибирская область), телефон +7 (913) 460-20-50, email, VK, Telegram. Закажите производство кемпера или бронь аренды."',
            '<meta property="og:description" content="Address in Koltsovo, phone +7 (913) 460-20-50, email, VK, Telegram."',
        ),
        (
            '<meta name="twitter:title" content="Контакты — адрес, телефон, как заказать автодом или аренду | Siberian motorbears">',
            '<meta name="twitter:title" content="Contacts — address, phone | Siberian motorbears">',
        ),
        (
            '<meta name="twitter:description" content="Контактная информация Siberian motorbears: адрес в Кольцово (Новосибирская область), телефон +7 (913) 460-20-50, email, VK, Telegram. Закажите производство кемпера или бронь аренды."',
            '<meta name="twitter:description" content="Koltsovo address, phone, email, VK, Telegram."',
        ),
        ("<span>Контакты</span>", "<span>Contact</span>"),
        ('<h1 style="font-size: 1.35rem;">Контакты</h1>', '<h1 style="font-size: 1.35rem;">Contact</h1>'),
        ('title="Карта: Кольцово, 6А"', 'title="Map: Koltsovo, 6A"'),
        ('<strong>Адрес</strong>', '<strong>Address</strong>'),
        ('<strong>Электропочта</strong>', '<strong>Email</strong>'),
        ('<strong>Телефон</strong>', '<strong>Phone</strong>'),
        ('<strong>Телеграм</strong>', '<strong>Telegram</strong>'),
        ('<strong>Сообщество VK</strong>', '<strong>VK community</strong>'),
        ("Новосибирская область, р.п. Кольцово, д. 6А", "Novosibirsk region, Koltsovo, 6A"),
    ]
    copy_translate_deep("contact/index.html", contact_extra)

    legal_extra = [
        (
            "<title>Реквизиты ИП Соловьев Д.А. — для договоров и оплаты | Siberian motorbears</title>",
            "<title>Legal details — IE Solovyov D.A. | Siberian motorbears</title>",
        ),
        (
            'content="Юридические реквизиты и информация Siberian motorbears: ИП Соловьев Д.А. Для заключения договора на производство автодома или аренду кемпера."',
            'content="Legal information for Siberian motorbears (IE Solovyov D.A.) — contracts and payments."',
        ),
        (
            '<meta property="og:title" content="Реквизиты ИП Соловьев Д.А. — для договоров и оплаты | Siberian motorbears">',
            '<meta property="og:title" content="Legal details — IE Solovyov D.A. | Siberian motorbears">',
        ),
        (
            '<meta property="og:description" content="Юридические реквизиты и информация Siberian motorbears: ИП Соловьев Д.А. Для заключения договора на производство автодома или аренду кемпера."',
            '<meta property="og:description" content="Legal information for contracts and payments."',
        ),
        (
            '<meta name="twitter:title" content="Реквизиты ИП Соловьев Д.А. — для договоров и оплаты | Siberian motorbears">',
            '<meta name="twitter:title" content="Legal details — IE Solovyov D.A. | Siberian motorbears">',
        ),
        (
            '<meta name="twitter:description" content="Юридические реквизиты и информация Siberian motorbears: ИП Соловьев Д.А. Для заключения договора на производство автодома или аренду кемпера."',
            '<meta name="twitter:description" content="Legal information for contracts and payments."',
        ),
        (
            '<meta name="keywords" content="реквизиты ИП, Siberian motorbears, договор аренды, договор на производство">',
            '<meta name="keywords" content="legal details, Siberian motorbears, rental contract, manufacturing contract">',
        ),
        (
            '<h1 class="legal-title">ИП СОЛОВЬЕВ ДМИТРИЙ АЛЕКСАНДРОВИЧ</h1>',
            '<h1 class="legal-title">IE SOLOVYOV DMITRY ALEKSANDROVICH</h1>',
        ),
        (
            '<div class="legal-row__data">630510, РОССИЯ, ОБЛ. НОВОСИБИРСКАЯ, Р-Н НОВОСИБИРСКИЙ, РП КОЛЬЦОВО, Д. 6А, КВ. 2</div>',
            '<div class="legal-row__data">630510, Russia, Novosibirsk region, Novosibirsk district, Koltsovo urban settlement, building 6A, apt. 2</div>',
        ),
        ('<div class="legal-row__label">ИНН</div>', '<div class="legal-row__label">TIN (tax ID)</div>'),
        ('<div class="legal-row__label">ОГРН</div>', '<div class="legal-row__label">OGRN</div>'),
        ('<div class="legal-row__label">БИК банка</div>', '<div class="legal-row__label">Bank BIC</div>'),
        ('<div class="legal-row__label">Банк</div>', '<div class="legal-row__label">Bank name</div>'),
        ('<div class="legal-row__data">АО «ТБанк»</div>', '<div class="legal-row__data">TBank JSC</div>'),
        ('<div class="legal-row__label">Юридический адрес банка</div>', '<div class="legal-row__label">Bank registered address</div>'),
        (
            '<div class="legal-row__data">Москва, 123060, 1-й Волоколамский проезд, д. 10, стр. 1</div>',
            '<div class="legal-row__data">Moscow, 123060, 1st Volokolamsky passage, bldg. 10, structure 1</div>',
        ),
        ('<div class="legal-row__label">ИНН банка</div>', '<div class="legal-row__label">Bank TIN</div>'),
        ("<span>Реквизиты</span>", "<span>Legal</span>"),
        ('<div class="legal-row__label">Юридический адрес организации</div>', '<div class="legal-row__label">Registered address</div>'),
        ('<div class="legal-row__label">Расчетный счет</div>', '<div class="legal-row__label">Bank account</div>'),
        ('<div class="legal-row__label">Корр.счет банка</div>', '<div class="legal-row__label">Correspondent account</div>'),
    ]
    copy_translate_deep("legal/index.html", legal_extra)

    copy_translate_deep("examples/index.html", EXAMPLES_EXTRA)

    copy_translate_deep("baribal/index.html", BARIBAL_EXTRA)

    copy_translate_deep("panda/index.html", PANDA_EXTRA)
    copy_translate_deep("baron/index.html", BARON_EXTRA)
    copy_translate_deep("mia/index.html", MIA_EXTRA)

    routes_en()
    print(
        "Tip: python3 scripts/mt_en_site_pages.py  # translate remaining Russian in /en/ pages"
    )


if __name__ == "__main__":
    main()
