#!/usr/bin/env python3
"""
Перевести site/routes/index.html → site/en/routes/index.html (MyMemory + кеш).

Запуск из корня: python3 scripts/machine_translate_routes.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mt_html_lib import (  # noqa: E402
    REPO,
    fix_motor_terms,
    finalize_routes_from_ru,
    load_cache,
    save_cache,
    translate_ld_json_scripts,
    translate_navigable_strings,
    translate_route_info_js,
)

SRC = REPO / "site" / "routes" / "index.html"
DST = REPO / "site" / "en" / "routes" / "index.html"


def main() -> None:
    cache = load_cache()
    raw = SRC.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")

    translate_navigable_strings(soup, cache)
    translate_ld_json_scripts(soup, cache)

    html = str(soup)
    html = translate_route_info_js(html, cache)
    html = fix_motor_terms(html)
    html = finalize_routes_from_ru(html)

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(html, encoding="utf-8")
    save_cache(cache)
    print("Wrote", DST.relative_to(REPO), "cache entries:", len(cache))


if __name__ == "__main__":
    main()
