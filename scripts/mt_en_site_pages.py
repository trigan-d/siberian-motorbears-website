#!/usr/bin/env python3
"""
Машинный перевод оставшегося русского текста в HTML под site/en/ (не используйте для основных страниц: routes — build_routes_en_manual.py; examples и др. — build_en_site.py с ручными парами).

Запуск после build_en_site.py:
  python3 scripts/mt_en_site_pages.py

Опции:
  --with-blog-entries   также переводить полные тексты записей блога (долго, много запросов к API).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bs4 import BeautifulSoup

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mt_html_lib import (  # noqa: E402
    CYR,
    REPO,
    fix_motor_terms,
    load_cache,
    save_cache,
    translate_ld_json_scripts,
    translate_navigable_strings,
)

SITE_EN = REPO / "site" / "en"


def should_skip(path: Path, skip_blog_entries: bool) -> bool:
    rel = path.relative_to(SITE_EN)
    if rel.parts == ("routes", "index.html"):
        return True
    # Built by build_en_site.py with curated pairs — skip BS4 rewrite (avoids partial MT / formatting drift).
    if rel in (
        Path("rent/index.html"),
        Path("legal/index.html"),
        Path("contact/index.html"),
        Path("examples/index.html"),
    ):
        return True
    if skip_blog_entries and len(rel.parts) >= 2 and rel.parts[0] == "blog":
        if rel.name.startswith("entry_") and rel.suffix == ".html":
            return True
    return False


def process_file(path: Path, cache: dict[str, str]) -> bool:
    raw = path.read_text(encoding="utf-8")
    if not CYR.search(raw):
        return False
    soup = BeautifulSoup(raw, "html.parser")
    translate_navigable_strings(soup, cache)
    translate_ld_json_scripts(soup, cache)
    html = fix_motor_terms(str(soup))
    path.write_text(html, encoding="utf-8")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--with-blog-entries",
        action="store_true",
        help="Translate full blog post bodies (many API calls).",
    )
    args = ap.parse_args()
    skip_entries = not args.with_blog_entries

    cache = load_cache()
    done = 0
    for path in sorted(SITE_EN.rglob("*.html")):
        if should_skip(path, skip_entries):
            continue
        print("Processing", path.relative_to(REPO), flush=True)
        if process_file(path, cache):
            print("Translated", path.relative_to(REPO), flush=True)
            done += 1
    save_cache(cache)
    print("Done. Files updated:", done, "| cache size:", len(cache), flush=True)


if __name__ == "__main__":
    main()
