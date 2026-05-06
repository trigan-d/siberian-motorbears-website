#!/usr/bin/env python3
"""
Заполнить поле text_en в site/blog/entries/entry_*.json (RU → EN).

Используется встроенный urllib и публичный client=gtx (как в переводчике в браузере).
Запуск из корня репозитория:
  python3 scripts/fill_blog_text_en.py

Перезаписать существующий text_en: --force

После запуска:
  python3 scripts/render_blog_initial.py
  python3 scripts/render_blog_entry_pages.py 200
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "site" / "blog" / "entries"

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
                raise RuntimeError(f"translate failed after retries: {e}") from e
            time.sleep(1.2 * (attempt + 1))
    parts: list[str] = []
    for block in data[0] or []:
        if block and block[0]:
            parts.append(block[0])
    return "".join(parts)


def translate_in_batches(text: str) -> str:
    lines = text.split("\n")
    batches: list[str] = []
    buf: list[str] = []
    size = 0
    for line in lines:
        add_len = len(line) + (1 if buf else 0)
        if size + add_len > 1800 and buf:
            batches.append("\n".join(buf))
            buf = [line]
            size = len(line)
        else:
            buf.append(line)
            size += add_len
    if buf:
        batches.append("\n".join(buf))

    out: list[str] = []
    for i, batch in enumerate(batches):
        if not batch.strip():
            out.append(batch)
        else:
            out.append(gtx_translate(batch))
        if i < len(batches) - 1:
            time.sleep(0.4)
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Перезаписать существующий text_en")
    args = ap.parse_args()

    pattern = re.compile(r"^entry_(\d+)\.json$")
    paths = sorted(
        ENTRIES_DIR.glob("entry_*.json"),
        key=lambda p: int(m.group(1)) if (m := pattern.match(p.name)) else 0,
    )
    done = 0
    for path in paths:
        if not pattern.match(path.name):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print("Пропуск (разбор):", path.name, e, file=sys.stderr)
            continue
        ru = (data.get("text") or "").strip()
        if not ru:
            continue
        existing = (data.get("text_en") or "").strip()
        if existing and not args.force:
            continue

        try:
            data["text_en"] = translate_in_batches(ru)
        except Exception as e:
            print("Ошибка перевода", path.name, e, file=sys.stderr)
            sys.exit(1)

        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("OK:", path.name)
        done += 1
        time.sleep(0.15)

    print("Готово, обновлено файлов:", done)


if __name__ == "__main__":
    main()
