#!/usr/bin/env python3
"""
Сгенерировать HTML для 10 самых свежих постов блога (entry_30 … entry_21)
и вставить в site/blog/index.html между маркерами BLOG_INITIAL_ENTRIES.
Остальные 20 подгружаются по скроллу через JS (нужен веб-сервер).
Запускать после обновления постов (save_blog_entries.py).
"""
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MONTHS_RU = (
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
)

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from brand import ru_to_en_brand  # noqa: E402

ENTRIES_DIR = REPO_ROOT / "site" / "blog" / "entries"
INDEX_HTML = REPO_ROOT / "site" / "blog" / "index.html"
EN_INDEX_HTML = REPO_ROOT / "site" / "en" / "blog" / "index.html"
ENTRIES_BASE = "entries/"

# URL в тексте делаем кликабельными
_URL_RE = re.compile(r"https?://[^\s<>\"']+")


def linkify_text(text: str) -> str:
    """Заменить URL в тексте на <a href="..."> с экранированием HTML."""
    result = []
    last = 0
    for m in _URL_RE.finditer(text):
        result.append(html.escape(text[last : m.start()]))
        url = m.group(0)
        result.append(f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(url)}</a>')
        last = m.end()
    result.append(html.escape(text[last:]))
    return "".join(result)


def entry_body_text(data: dict, *, body_locale: str) -> str:
    """Текст записи для разметки: при EN — text_en, иначе русский text."""
    if body_locale == "en":
        te = (data.get("text_en") or "").strip()
        if te:
            return te
    return (data.get("text") or "").strip()


def is_entry_empty(data: dict) -> bool:
    """Репост/пустая запись: нет текста, нет фото, нет видео."""
    text = (data.get("text") or "").strip()
    photos = data.get("photos") or []
    video = data.get("video")
    return not text and not photos and (video is None or not video.get("embed_url"))


def is_entry_file_empty(path: Path) -> bool:
    """Прочитать entry_*.json и вернуть True, если запись пустая (репост)."""
    if not path.exists():
        return True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return is_entry_empty(data)
    except Exception:
        return True


def get_initial_entry_filenames(count: int = 10) -> list[str]:
    """Имена файлов count самых свежих непустых записей (от новых к старым). Репосты не включаются."""
    pattern = re.compile(r"^entry_(\d+)\.json$")
    numbers = []
    for p in ENTRIES_DIR.glob("entry_*.json"):
        m = pattern.match(p.name)
        if m:
            numbers.append(int(m.group(1)))
    numbers.sort(reverse=True)
    result = []
    for n in numbers:
        if len(result) >= count:
            break
        path = ENTRIES_DIR / f"entry_{n}.json"
        if not is_entry_file_empty(path):
            result.append(f"entry_{n}.json")
    return result


def format_date(ts: int, *, locale: str = "ru") -> str:
    d = datetime.fromtimestamp(ts, tz=timezone.utc)
    if locale == "en":
        return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")
    return f"{d.day} {MONTHS_RU[d.month - 1]} {d.year}"


def render_entry(
    data: dict,
    *,
    entry_page_filename: str | None = None,
    date_is_link: bool = True,
    date_locale: str = "ru",
    body_locale: str = "ru",
    entries_base: str | None = None,
) -> str:
    date_ts = data.get("date", 0)
    date_str = format_date(date_ts, locale=date_locale)
    iso_date = datetime.fromtimestamp(date_ts, tz=timezone.utc).strftime("%Y-%m-%d")
    text = entry_body_text(data, body_locale=body_locale)
    text_html = ""
    if text:
        parts = [f'<p class="blog-entry__text">{linkify_text(p)}</p>' for p in text.split("\n")]
        text_html = '<div class="blog-entry__body">' + "".join(parts) + "</div>"
    photos = data.get("photos") or []
    video = (data.get("video") or {}).get("embed_url")
    vk_url = data.get("vk_url") or ""
    has_media = bool(photos or video)
    no_media_class = " blog-entry--no-media" if not has_media else ""

    eb = entries_base if entries_base is not None else ENTRIES_BASE
    media_parts = []
    if photos:
        slides = "".join(
            f'<div><img src="{eb}{html.escape(f)}" alt="" loading="lazy"></div>' for f in photos
        )
        media_parts.append(f'<div class="carousel"><div class="carousel-slides">{slides}</div></div>')
    if video:
        media_parts.append(
            f'<div class="blog-entry__video video-wrap">'
            f'<iframe src="{html.escape(video)}" width="640" height="360" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
            f"</div>"
        )
    media_html = '<div class="product-block__media">' + "".join(media_parts) + "</div>" if has_media else '<div class="product-block__media"></div>'

    if body_locale == "en":
        vk_comment = f' <a class="blog-entry__vk-comment" href="{html.escape(vk_url)}" target="_blank" rel="noopener">comment on VK</a>'
    else:
        vk_comment = f' <a class="blog-entry__vk-comment" href="{html.escape(vk_url)}" target="_blank" rel="noopener">комментировать в VK</a>'
    if not date_is_link:
        date_tag = f'<span class="blog-entry__date"><time datetime="{iso_date}">{html.escape(date_str)}</time></span>'
    elif entry_page_filename:
        date_tag = f'<a class="blog-entry__date" href="{html.escape(entry_page_filename)}"><time datetime="{iso_date}">{html.escape(date_str)}</time></a>'
    else:
        date_tag = f'<a class="blog-entry__date" href="{html.escape(vk_url)}" target="_blank" rel="noopener"><time datetime="{iso_date}">{html.escape(date_str)}</time></a>'

    meta_html = f'<div class="blog-entry__meta">{date_tag}{vk_comment}</div>'

    return (
        f'<article class="blog-entry product-block{no_media_class}">'
        f'<div class="product-block__info">{meta_html}{text_html}</div>'
        f"{media_html}</article>"
    )


_PROTECTED_RE = re.compile(
    r"(<!-- BLOG_INITIAL_ENTRIES -->.*?<!-- /BLOG_INITIAL_ENTRIES -->"
    r"|<!-- BLOG_ARCHIVE_LIST -->.*?<!-- /BLOG_ARCHIVE_LIST -->)",
    re.DOTALL,
)


def _brand_outside_entries(html: str) -> str:
    """Латинизировать бренд только в обвязке страницы.

    Между маркерами лежат тексты и заголовки записей. Там «Сибмотобэр» —
    слово из поста (например, в записи про само переименование), а не
    название в шапке, и заменять его нельзя.
    """
    parts = _PROTECTED_RE.split(html)
    return "".join(part if i % 2 else ru_to_en_brand(part)
                   for i, part in enumerate(parts))


def ru_blog_index_to_en(html: str) -> str:
    """Собрать английский blog/index.html из русского (пути /en/blog/, медиа из ../../blog/entries/)."""
    t = _brand_outside_entries(html)
    pairs = [
        ('lang="ru"', 'lang="en"'),
        ('href="../assets/', 'href="../../assets/'),
        ('src="../assets/', 'src="../../assets/'),
        ('href="../css/', 'href="../../css/'),
        ('href="../js/', 'href="../../js/'),
        ('src="../js/', 'src="../../js/'),
        ('src="entries/', 'src="../../blog/entries/'),
        ('href="entries/', 'href="../../blog/entries/'),
        ("var entriesBase = 'entries/';", "var entriesBase = '../../blog/entries/';"),
        ("toLocaleDateString('ru-RU'", "toLocaleDateString('en-US'"),
        ('комментировать в VK', 'comment on VK'),
        ('Загрузка…', 'Loading…'),
        ('Читать дальше', 'Load more'),
        ('Записи закончились.', 'No more posts.'),
        ('aria-label="Меню"', 'aria-label="Menu"'),
        ('aria-label="Хлебные крошки"', 'aria-label="Breadcrumbs"'),
        ('>Главная</a>', '>Home</a>'),
        ('>Блог</span>', '>Blog</span>'),
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
        ('aria-label="Контакты"', 'aria-label="Contact"'),
        ('aria-label="Вконтакте"', 'aria-label="VK"'),
        ('aria-label="Электронная почта"', 'aria-label="Email"'),
        ('aria-label="Номер телефона"', 'aria-label="Phone"'),
        ('<title>Блог о производстве и прокате автодомов | Siberian motorbears</title>',
         '<title>Motorhome manufacturing & rental blog | Siberian motorbears</title>'),
        ('content="Новости и посты сообщества Siberian motorbears: кемперы, путешествия, аренда."',
         'content="News from Siberian motorbears: campers, road trips, rentals."'),
        ('content="блог автодомов, Siberian motorbears', 'content="motorhome blog, Siberian motorbears'),
        ('<meta property="og:locale" content="ru_RU">', '<meta property="og:locale" content="en_US">'),
        ('https://siberian-motorbears.ru/blog/"', 'https://siberian-motorbears.ru/en/blog/"'),
        ('<meta property="og:title" content="Блог о производстве и прокате автодомов | Siberian motorbears">',
         '<meta property="og:title" content="Motorhome manufacturing & rental blog | Siberian motorbears">'),
        ('<meta property="og:description" content="Новости и посты сообщества Siberian motorbears: кемперы, путешествия, аренда."',
         '<meta property="og:description" content="News from Siberian motorbears: campers, road trips, rentals."'),
        ('<meta name="twitter:title" content="Блог о производстве и прокате автодомов | Siberian motorbears">',
         '<meta name="twitter:title" content="Motorhome manufacturing & rental blog | Siberian motorbears">'),
        ('<meta name="twitter:description" content="Новости и посты сообщества Siberian motorbears: кемперы, путешествия, аренда."',
         '<meta name="twitter:description" content="News from Siberian motorbears: campers, road trips, rentals."'),
        ('<h1 style="font-size: 1.35rem;">Блог о производстве и прокате автодомов</h1>',
         '<h1 style="font-size: 1.35rem;">Motorhome manufacturing & rental blog</h1>'),
        ('Сообщество VK', 'VK community'),
        ("Не удалось загрузить записи.", "Could not load posts."),
        (
            "<!-- Яндекс.Метрика: заменить 66322963 на номер счётчика во всём проекте -->",
            "<!-- Yandex.Metrica: replace 66322963 with your counter id site-wide -->",
        ),
        ("<!-- Яндекс.Метрика -->", "<!-- Yandex.Metrica -->"),
        (
            "<!-- VK Пиксель (Top.Mail.Ru), код 3727349 -->",
            "<!-- VK pixel (Top.Mail.Ru) id 3727349 -->",
        ),
        (
            "// Записи, подгружаемые по кнопке «Load more» (первые 10 уже встроены в HTML)",
            "// Entries loaded via «Load more» (first 10 are inlined in HTML)",
        ),
        (
            "var text = (data.text || '').trim();",
            "var text = ((data.text_en != null && String(data.text_en).trim() !== '') ? data.text_en : data.text || '').trim();",
        ),
    ]
    for a, b in pairs:
        t = t.replace(a, b)
    t = t.replace('<script src="/js/locale-redirect.js"></script>\n', '')
    t = re.sub(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"BreadcrumbList","itemListElement":\[[^\]]+\]\}</script>',
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://siberian-motorbears.ru/en/"},{"@type":"ListItem","position":2,"name":"Blog","item":"https://siberian-motorbears.ru/en/blog/"}]}</script>',
        t,
        count=1,
    )
    t = t.replace(
        '<meta name="keywords" content="motorhome blog, Siberian motorbears, кемперы, прокат автодомов, производство кемперов, Новосибирск">',
        '<meta name="keywords" content="motorhome blog, Siberian motorbears, campers, rental, manufacturing, Novosibirsk">',
    )
    t = t.replace(
        '<div id="blog-error" class="blog-error" hidden>Could not load posts. Откройте страницу через веб‑сервер (не file://), например: в папке <code>site</code> выполните <code>python3 -m http.server 8000</code> и откройте <a href="http://localhost:8000/blog/">http://localhost:8000/blog/</a>.</div>',
        '<div id="blog-error" class="blog-error" hidden>Could not load posts. Serve the site over HTTP (not file://), e.g. run <code>python3 -m http.server 8000</code> in the <code>site</code> folder and open <a href="http://localhost:8000/en/blog/">http://localhost:8000/en/blog/</a>.</div>',
    )
    return t


def _load_titles(locale: str) -> dict:
    name = "entry_titles_en.json" if locale == "en" else "entry_titles.json"
    path = ENTRIES_DIR.parent / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def render_archive_list(*, locale: str, manifest: dict) -> str:
    """Полный список всех записей блога ссылками на отдельные страницы.

    Нужен, чтобы поисковики обнаружили все entry_*.html через статичный HTML,
    а не через клик по «Читать дальше» (JS).
    """
    titles = _load_titles(locale)
    pattern = re.compile(r"^entry_(\d+)\.json$")
    items = []
    for p in ENTRIES_DIR.glob("entry_*.json"):
        m = pattern.match(p.name)
        if not m:
            continue
        n = int(m.group(1))
        page = manifest.get(str(n))
        if not page:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if is_entry_empty(data):
            continue
        ts = data.get("date", 0)
        title = titles.get(str(n)) or ""
        if not title:
            text = entry_body_text(data, body_locale=locale)
            first_line = text.split("\n", 1)[0] if text else ""
            title = first_line[:80].rstrip() + ("…" if len(first_line) > 80 else "")
        iso = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        short_date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%d.%m.%y")
        items.append((n, ts, page, title, iso, short_date))
    items.sort(key=lambda r: r[1], reverse=True)
    lis = [
        f'<li><a href="{html.escape(page)}">'
        f'<time class="blog-archive__date" datetime="{iso}">{short_date}</time> '
        f'<span class="blog-archive__title">{html.escape(title)}</span>'
        f'</a></li>'
        for _, _, page, title, iso, short_date in items
    ]
    heading = "All posts" if locale == "en" else "Все записи"
    return (
        f'<nav class="blog-archive" aria-label="{heading}">'
        f'<h2 class="blog-archive__title-h">{heading}</h2>'
        f'<ul class="blog-archive__list">' + "".join(lis) + "</ul></nav>"
    )


def main() -> None:
    if not ENTRIES_DIR.exists():
        print("Папка entries не найдена:", ENTRIES_DIR, file=sys.stderr)
        sys.exit(1)
    if not INDEX_HTML.exists():
        print("Файл index.html не найден:", INDEX_HTML, file=sys.stderr)
        sys.exit(1)

    manifest = {}
    manifest_path = INDEX_HTML.parent / "entry_pages_manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    initial_filenames = get_initial_entry_filenames(10)
    html_parts = []
    html_parts_en = []
    for filename in initial_filenames:
        path = ENTRIES_DIR / filename
        if not path.exists():
            print("Пропуск (нет файла):", filename, file=sys.stderr)
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if is_entry_empty(data):
                continue
            m = re.match(r"^entry_(\d+)\.json$", filename)
            entry_num = int(m.group(1)) if m else None
            entry_page = manifest.get(str(entry_num)) if entry_num else None
            html_parts.append(
                render_entry(data, entry_page_filename=entry_page, date_is_link=True)
            )
            html_parts_en.append(
                render_entry(
                    data,
                    entry_page_filename=entry_page,
                    date_is_link=True,
                    date_locale="en",
                    body_locale="en",
                )
            )
        except Exception as e:
            print("Ошибка при разборе", filename, e, file=sys.stderr)

    content = "\n".join(html_parts)
    content_en = "\n".join(html_parts_en)
    marker_start = "<!-- BLOG_INITIAL_ENTRIES -->"
    marker_end = "<!-- /BLOG_INITIAL_ENTRIES -->"
    pattern = re.compile(re.escape(marker_start) + r".*?" + re.escape(marker_end), re.DOTALL)

    archive_marker_start = "<!-- BLOG_ARCHIVE_LIST -->"
    archive_marker_end = "<!-- /BLOG_ARCHIVE_LIST -->"
    archive_pattern = re.compile(
        re.escape(archive_marker_start) + r".*?" + re.escape(archive_marker_end), re.DOTALL
    )
    archive_ru = render_archive_list(locale="ru", manifest=manifest)
    archive_en = render_archive_list(locale="en", manifest=manifest)

    index_text = INDEX_HTML.read_text(encoding="utf-8")
    if marker_start not in index_text or marker_end not in index_text:
        print("В index.html не найдены маркеры BLOG_INITIAL_ENTRIES.", file=sys.stderr)
        sys.exit(1)

    new_block = f"{marker_start}\n{content}\n        {marker_end}"
    new_index = pattern.sub(new_block, index_text, count=1)
    if archive_marker_start in new_index:
        new_index = archive_pattern.sub(
            f"{archive_marker_start}\n{archive_ru}\n        {archive_marker_end}", new_index, count=1
        )
    INDEX_HTML.write_text(new_index, encoding="utf-8")
    print("Вставлено постов:", len(html_parts))

    EN_INDEX_HTML.parent.mkdir(parents=True, exist_ok=True)
    en_block = f"{marker_start}\n{content_en}\n        {marker_end}"
    new_index_en_src = pattern.sub(en_block, index_text, count=1)
    if archive_marker_start in new_index_en_src:
        new_index_en_src = archive_pattern.sub(
            f"{archive_marker_start}\n{archive_en}\n        {archive_marker_end}",
            new_index_en_src,
            count=1,
        )
    EN_INDEX_HTML.write_text(ru_blog_index_to_en(new_index_en_src), encoding="utf-8")
    print("Обновлён английский индекс блога:", EN_INDEX_HTML)


if __name__ == "__main__":
    main()
