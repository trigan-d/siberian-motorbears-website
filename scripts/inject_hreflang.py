#!/usr/bin/env python3
"""Вставить hreflang link-теги во все HTML под site/, у которых есть пара RU↔EN.

x-default указывает на русскую версию. Идемпотентно: блок ограничен маркерами.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
ORIGIN = "https://siberian-motorbears.ru"

MARKER_START = "<!-- HREFLANG_ALTERNATES -->"
MARKER_END = "<!-- /HREFLANG_ALTERNATES -->"
BLOCK_RE = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL)


def url_for(rel: Path) -> str:
    """site/foo/index.html → /foo/ ; site/blog/entry_X.html → /blog/entry_X.html"""
    parts = list(rel.parts)
    if parts[-1] == "index.html":
        parts = parts[:-1]
        path = "/" + "/".join(parts)
        if not path.endswith("/"):
            path += "/"
    else:
        path = "/" + "/".join(parts)
    return ORIGIN + path


def counterpart_rel(rel: Path) -> Path | None:
    parts = list(rel.parts)
    if parts and parts[0] == "en":
        # /en/foo/... -> /foo/...
        return Path(*parts[1:]) if len(parts) > 1 else None
    return Path("en", *parts)


def render_block(ru_url: str, en_url: str) -> str:
    return (
        f"{MARKER_START}\n"
        f'  <link rel="alternate" hreflang="ru" href="{ru_url}">\n'
        f'  <link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{ru_url}">\n'
        f"  {MARKER_END}"
    )


def main() -> None:
    changed = 0
    skipped_no_pair = 0
    for path in sorted(SITE.rglob("*.html")):
        rel = path.relative_to(SITE)
        if "yandex" in path.name.lower():
            continue
        pair_rel = counterpart_rel(rel)
        if pair_rel is None:
            continue
        pair_path = SITE / pair_rel
        if not pair_path.exists():
            skipped_no_pair += 1
            continue

        is_en = rel.parts and rel.parts[0] == "en"
        ru_url = url_for(pair_rel if is_en else rel)
        en_url = url_for(rel if is_en else pair_rel)
        block = render_block(ru_url, en_url)

        text = path.read_text(encoding="utf-8")
        if MARKER_START in text and MARKER_END in text:
            new_text = BLOCK_RE.sub(block, text, count=1)
        elif "</head>" in text:
            new_text = text.replace("</head>", block + "\n</head>", 1)
        else:
            continue
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"Изменено файлов: {changed}")
    print(f"Пропущено (нет пары): {skipped_no_pair}")


if __name__ == "__main__":
    main()
