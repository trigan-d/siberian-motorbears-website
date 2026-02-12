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
ENTRIES_DIR = REPO_ROOT / "site" / "blog" / "entries"
INDEX_HTML = REPO_ROOT / "site" / "blog" / "index.html"
ENTRIES_BASE = "entries/"


def get_initial_entry_filenames(count: int = 10) -> list[str]:
    """Имена файлов 10 (или count) самых свежих записей по номерам (от новых к старым)."""
    import re
    pattern = re.compile(r"^entry_(\d+)\.json$")
    numbers = []
    for p in ENTRIES_DIR.glob("entry_*.json"):
        m = pattern.match(p.name)
        if m:
            numbers.append(int(m.group(1)))
    numbers.sort(reverse=True)
    return [f"entry_{n}.json" for n in numbers[:count]]


def format_date(ts: int) -> str:
    d = datetime.fromtimestamp(ts, tz=timezone.utc)
    return f"{d.day} {MONTHS_RU[d.month - 1]} {d.year}"


def render_entry(data: dict) -> str:
    date_ts = data.get("date", 0)
    date_str = format_date(date_ts)
    iso_date = datetime.fromtimestamp(date_ts, tz=timezone.utc).strftime("%Y-%m-%d")
    text = (data.get("text") or "").strip()
    text_html = ""
    if text:
        parts = [f'<p class="blog-entry__text">{html.escape(p)}</p>' for p in text.split("\n")]
        text_html = '<div class="blog-entry__body">' + "".join(parts) + "</div>"
    photos = data.get("photos") or []
    video = (data.get("video") or {}).get("embed_url")
    vk_url = data.get("vk_url") or ""
    has_media = bool(photos or video)
    no_media_class = " blog-entry--no-media" if not has_media else ""

    media_parts = []
    if photos:
        slides = "".join(
            f'<div><img src="{ENTRIES_BASE}{html.escape(f)}" alt="" loading="lazy"></div>' for f in photos
        )
        media_parts.append(f'<div class="carousel"><div class="carousel-slides">{slides}</div></div>')
    if video:
        media_parts.append(
            f'<div class="blog-entry__video video-wrap">'
            f'<iframe src="{html.escape(video)}" width="640" height="360" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
            f"</div>"
        )
    media_html = '<div class="product-block__media">' + "".join(media_parts) + "</div>" if has_media else '<div class="product-block__media"></div>'

    date_tag = f'<a class="blog-entry__date" href="{html.escape(vk_url)}" target="_blank" rel="noopener"><time datetime="{iso_date}">{html.escape(date_str)}</time></a>'

    return (
        f'<article class="blog-entry product-block{no_media_class}">'
        f'<div class="product-block__info">{date_tag}{text_html}</div>'
        f"{media_html}</article>"
    )


def main() -> None:
    if not ENTRIES_DIR.exists():
        print("Папка entries не найдена:", ENTRIES_DIR, file=sys.stderr)
        sys.exit(1)
    if not INDEX_HTML.exists():
        print("Файл index.html не найден:", INDEX_HTML, file=sys.stderr)
        sys.exit(1)

    initial_filenames = get_initial_entry_filenames(10)
    html_parts = []
    for filename in initial_filenames:
        path = ENTRIES_DIR / filename
        if not path.exists():
            print("Пропуск (нет файла):", filename, file=sys.stderr)
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            html_parts.append(render_entry(data))
        except Exception as e:
            print("Ошибка при разборе", filename, e, file=sys.stderr)

    content = "\n".join(html_parts)
    marker_start = "<!-- BLOG_INITIAL_ENTRIES -->"
    marker_end = "<!-- /BLOG_INITIAL_ENTRIES -->"
    pattern = re.compile(re.escape(marker_start) + r".*?" + re.escape(marker_end), re.DOTALL)

    index_text = INDEX_HTML.read_text(encoding="utf-8")
    if marker_start not in index_text or marker_end not in index_text:
        print("В index.html не найдены маркеры BLOG_INITIAL_ENTRIES.", file=sys.stderr)
        sys.exit(1)

    new_block = f"{marker_start}\n{content}\n        {marker_end}"
    new_index = pattern.sub(new_block, index_text, count=1)
    INDEX_HTML.write_text(new_index, encoding="utf-8")
    print("Вставлено постов:", len(html_parts))


if __name__ == "__main__":
    main()
