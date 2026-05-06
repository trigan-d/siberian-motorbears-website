"""Общая машинная переводка HTML (MyMemory + кеш)."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

REPO = Path(__file__).resolve().parent.parent
GLOBAL_CACHE_PATH = REPO / "scripts" / "data" / "mt_global_cache.json"

CYR = re.compile(r"[а-яА-ЯёЁ]")


def fix_motor_terms(s: str) -> str:
    s = re.sub(r"\bMotorized\s+Bears\b", "Motorbears", s)
    s = re.sub(r"\bmotorized\s+bears\b", "motorbears", s)
    s = re.sub(r"\bMotorized\s+bear\b", "Motorbear", s)
    s = re.sub(r"\bmotorized\s+bear\b", "motorbear", s)
    return s


OLD_ROUTES_CACHE = REPO / "scripts" / "data" / "routes_mt_cache.json"


def load_cache() -> dict[str, str]:
    c: dict[str, str] = {}
    if GLOBAL_CACHE_PATH.exists():
        try:
            c.update(json.loads(GLOBAL_CACHE_PATH.read_text(encoding="utf-8")))
        except Exception:
            pass
    if OLD_ROUTES_CACHE.exists():
        try:
            c.update(json.loads(OLD_ROUTES_CACHE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return c


def save_cache(c: dict[str, str]) -> None:
    GLOBAL_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    GLOBAL_CACHE_PATH.write_text(json.dumps(c, ensure_ascii=False, indent=0), encoding="utf-8")


def translate_line(q: str, cache: dict[str, str]) -> str:
    q = q.strip()
    if not q or not CYR.search(q):
        return q
    if q in cache:
        return cache[q]
    if len(q) > 480:
        parts = re.split(r"(?<=[.!?…])\s+", q)
        if len(parts) <= 1:
            parts = [q[i : i + 400] for i in range(0, len(q), 400)]
        out_chunks: list[str] = []
        buf = ""
        for p in parts:
            if not p.strip():
                continue
            if len(buf) + len(p) < 430:
                buf = (buf + " " + p).strip()
            else:
                if buf:
                    out_chunks.append(translate_line(buf, cache))
                buf = p
        if buf:
            out_chunks.append(translate_line(buf, cache))
        merged = " ".join(out_chunks)
        cache[q] = merged
        return merged

    url = (
        "https://api.mymemory.translated.net/get?q="
        + urllib.parse.quote(q)
        + "&langpair=ru|en"
    )
    for attempt in range(12):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                data = json.loads(resp.read().decode())
            tr = data.get("responseData", {}).get("translatedText", q)
            tr = fix_motor_terms(tr)
            cache[q] = tr
            time.sleep(0.35)
            return tr
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(90 + attempt * 30)
                continue
            time.sleep(1.5 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            time.sleep(1.5 * (attempt + 1))
    cache[q] = q
    return q


def translate_navigable_strings(soup: BeautifulSoup, cache: dict[str, str]) -> None:
    for node in list(soup.descendants):
        if not isinstance(node, NavigableString):
            continue
        if not CYR.search(str(node)):
            continue
        parent = getattr(node, "parent", None)
        if parent is not None and parent.name in ("script", "style"):
            continue
        original = str(node)
        key = original.strip()
        if key in cache:
            node.replace_with(cache[key])
            continue
        translated = translate_line(key, cache)
        if translated != key:
            node.replace_with(translated)


def _translate_json_values(obj: object, cache: dict[str, str]) -> object:
    if isinstance(obj, str):
        if not CYR.search(obj):
            return obj
        return translate_line(obj, cache)
    if isinstance(obj, list):
        return [_translate_json_values(x, cache) for x in obj]
    if isinstance(obj, dict):
        return {k: _translate_json_values(v, cache) for k, v in obj.items()}
    return obj


def translate_ld_json_scripts(soup: BeautifulSoup, cache: dict[str, str]) -> None:
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string
        if not raw or not raw.strip():
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        data = _translate_json_values(data, cache)
        script.string = json.dumps(data, ensure_ascii=False)


def translate_route_info_js(html: str, cache: dict[str, str]) -> str:
    def repl_name(m: re.Match[str]) -> str:
        inner = m.group(1)
        if not CYR.search(inner):
            return m.group(0)
        return "name: '" + translate_line(inner, cache).replace("'", "\\'") + "'"

    def repl_days(m: re.Match[str]) -> str:
        inner = m.group(1)
        if not CYR.search(inner):
            return m.group(0)
        return "days: '" + translate_line(inner, cache).replace("'", "\\'") + "'"

    html = re.sub(r"name:\s*'([^']*)'", repl_name, html)
    html = re.sub(r"days:\s*'([^']*)'", repl_days, html)
    return html


def finalize_routes_from_ru(html: str) -> str:
    """После перевода сырыого RU routes/index: UNIVERSAL, ../../assets, absolute URLs."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "build_en_site", REPO / "scripts" / "build_en_site.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    t = html
    t = mod.apply_pairs(t, mod.UNIVERSAL_DEEP)
    t = mod.fix_deep_en_asset_paths(t)
    t = mod.fix_page_absolute_urls(t)
    return t
