#!/usr/bin/env python3
"""
Собрать site/en/routes/index.html из site/routes/index.html без API:
универсальные замены + routes_en_shell + фрагменты статей из scripts/routes_en_fragments/.
Запуск из корня: python3 scripts/build_routes_en_manual.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
SRC = SITE / "routes" / "index.html"
DST = SITE / "en" / "routes" / "index.html"
FRAGMENTS_DIR = REPO / "scripts" / "routes_en_fragments"

_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from brand import ru_to_en_brand  # noqa: E402
from build_en_site import (  # noqa: E402
    UNIVERSAL_DEEP,
    apply_pairs,
    fix_deep_en_asset_paths,
    fix_page_absolute_urls,
)
from routes_en_shell import ROUTES_SHELL_PAIRS  # noqa: E402


def replace_articles(html: str) -> str:
    paths = sorted(FRAGMENTS_DIR.glob("*.html"))
    if not paths:
        raise SystemExit(f"No fragments in {FRAGMENTS_DIR}")
    for path in paths:
        article_id = path.stem
        en_article = path.read_text(encoding="utf-8").strip()
        if not en_article.startswith("<article"):
            raise SystemExit(f"{path}: expected content starting with <article")
        pattern = (
            r'<article class="route-card" id="' + re.escape(article_id) + r'">[\s\S]*?</article>'
        )
        html, n = re.subn(pattern, en_article, html, count=1)
        if n != 1:
            raise SystemExit(f"Replace failed for {article_id} (matches={n})")
    return html


def main() -> None:
    raw = ru_to_en_brand(SRC.read_text(encoding="utf-8"))
    t = apply_pairs(raw, UNIVERSAL_DEEP)
    t = fix_deep_en_asset_paths(t)
    t = fix_page_absolute_urls(t)
    t = apply_pairs(t, ROUTES_SHELL_PAIRS)
    t = replace_articles(t)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(t, encoding="utf-8")
    print("Wrote", DST.relative_to(REPO))


if __name__ == "__main__":
    main()
