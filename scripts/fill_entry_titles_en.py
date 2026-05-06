#!/usr/bin/env python3
"""
Собрать site/blog/entry_titles_en.json из entry_titles.json (перевод заголовков ru→en).

Используется тот же GTX endpoint, что и в fill_blog_text_en.py.
Запуск из корня: python3 scripts/fill_entry_titles_en.py

После правок заголовков на русском — перегенерировать этот файл и страницы записей:
  python3 scripts/render_blog_entry_pages.py 200
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = REPO_ROOT / "site" / "blog"
GTX = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ru&tl=en&dt=t&q="


def gtx_translate(text: str) -> str:
    if not text.strip():
        return text
    q = urllib.parse.quote(text, safe="")
    req = urllib.request.Request(
        GTX + q,
        headers={"User-Agent": "Mozilla/5.0 (compatible; siberian-motorbears/1.0)"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.loads(r.read().decode())
            break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if attempt == 4:
                raise RuntimeError(f"translate failed: {e}") from e
            time.sleep(1.2 * (attempt + 1))
    parts: list[str] = []
    for block in data[0] or []:
        if block and block[0]:
            parts.append(block[0])
    return "".join(parts)


def main() -> None:
    src = BLOG_DIR / "entry_titles.json"
    out = BLOG_DIR / "entry_titles_en.json"
    if not src.exists():
        print("Нет файла:", src, file=sys.stderr)
        sys.exit(1)
    ru_titles = json.loads(src.read_text(encoding="utf-8"))
    en_titles: dict[str, str] = {}
    keys = sorted(ru_titles.keys(), key=lambda k: int(k) if k.isdigit() else 0)
    for i, key in enumerate(keys):
        ru = ru_titles[key]
        try:
            en_titles[key] = gtx_translate(ru)
        except Exception as e:
            print("Ошибка для ключа", key, e, file=sys.stderr)
            sys.exit(1)
        print(key, "OK")
        if i < len(keys) - 1:
            time.sleep(0.35)
    out.write_text(json.dumps(en_titles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Записано:", out, "ключей:", len(en_titles))


if __name__ == "__main__":
    main()
