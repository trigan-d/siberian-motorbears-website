#!/usr/bin/env python3
"""
Показать несколько последних постов из сообщества VK siberian_motorbears.
Токен: VK_ACCESS_TOKEN в окружении или в scripts/.env
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen, Request

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_FILE = SCRIPT_DIR / ".env"
API_BASE = "https://api.vk.com/method"
API_VERSION = "5.199"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip("'\"").strip()
            if key:
                os.environ.setdefault(key, value)


def vk_request(method: str, params: dict) -> dict:
    params.setdefault("v", API_VERSION)
    params.setdefault("access_token", os.environ.get("VK_ACCESS_TOKEN", ""))
    url = f"{API_BASE}/{method}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "SiberianMotorbearsBlog/1.0"})
    with urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    if "error" in data:
        raise RuntimeError(f"VK API error: {data['error'].get('error_msg', data['error'])}")
    return data.get("response", {})


def resolve_group_id(screen_name: str) -> int:
    # groups.getById принимает short name и доступен для токена сообщества
    resp = vk_request("groups.getById", {"group_id": screen_name})
    groups = resp if isinstance(resp, list) else [resp]
    if not groups:
        raise RuntimeError(f"Group not found: {screen_name}")
    return int(groups[0]["id"])


def get_wall_posts(owner_id: int, count: int = 3) -> list:
    resp = vk_request(
        "wall.get",
        {"owner_id": -owner_id, "count": count, "filter": "owner"},
    )
    return resp.get("items", [])


def format_date(ts: int) -> str:
    return datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def photo_url(att: dict) -> str | None:
    p = att.get("photo", {}) if isinstance(att.get("photo"), dict) else {}
    for key in "photo_2560", "photo_1280", "photo_807", "photo_604", "photo_130":
        if p.get(key):
            return p[key]
    return None


def main():
    load_dotenv(ENV_FILE)
    token = os.environ.get("VK_ACCESS_TOKEN")
    if not token:
        print("Задайте VK_ACCESS_TOKEN в окружении или в scripts/.env", file=sys.stderr)
        sys.exit(1)

    screen_name = "siberian_motorbears"
    # ID группы siberian_motorbears (без минуса); можно переопределить через VK_GROUP_ID
    group_id = int(os.environ.get("VK_GROUP_ID", "197853818"))
    posts = get_wall_posts(group_id, count=3)
    base_url = f"https://vk.com/{screen_name}"

    for i, post in enumerate(posts, 1):
        pid = post.get("id")
        date = format_date(post.get("date", 0))
        text = (post.get("text") or "").strip()
        link = f"{base_url}?w=wall-{group_id}_{pid}"

        print()
        print("=" * 60)
        print(f"Пост {i} | {date}")
        print(f"Ссылка: {link}")
        print("-" * 60)
        if text:
            # ограничим длину вывода
            if len(text) > 1200:
                text = text[:1200] + "\n... [обрезано]"
            print(text)
        else:
            print("(без текста)")

        attachments = post.get("attachments") or []
        photos = [a for a in attachments if a.get("type") == "photo"]
        if photos:
            print()
            print("Фото:", len(photos))
            for j, att in enumerate(photos[:5], 1):
                url = photo_url(att)
                if url:
                    print(f"  {j}. {url}")
            if len(photos) > 5:
                print(f"  ... и ещё {len(photos) - 5}")
        print()

    print("=" * 60)
    print("Готово.")


if __name__ == "__main__":
    main()
