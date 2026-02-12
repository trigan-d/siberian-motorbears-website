#!/usr/bin/env python3
"""
Скачать 30 последних постов из VK siberian_motorbears и сохранить
каждый в site/blog/entries/entry_X.json (X=1..30: 1=самый старый из 30, 30=самый новый).
Фото скачиваются в папку entries (entry_X_1.jpg, ...) и сжимаются для WEB
(макс. сторона 1200px, JPEG quality 85).
Видео сохраняются как embed_url для iframe (video.get → player).
Токен: VK_ACCESS_TOKEN в scripts/.env или в окружении.
"""
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import urlopen, Request

try:
    from PIL import Image
    import io
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Параметры сжатия для WEB
IMG_MAX_SIZE = 1200  # пикселей по длинной стороне
IMG_QUALITY = 85

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
ENV_FILE = SCRIPT_DIR / ".env"
OUT_DIR = REPO_ROOT / "site" / "blog" / "entries"
API_BASE = "https://api.vk.com/method"
API_VERSION = "5.199"
COUNT = 30


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


def get_wall_posts(owner_id: int, count: int) -> list:
    resp = vk_request(
        "wall.get",
        {"owner_id": -owner_id, "count": count, "filter": "owner"},
    )
    return resp.get("items", [])


def fetch_video_players(video_keys: list) -> dict:
    """video_keys = ["owner_id_id", ...]. Returns dict key -> player URL.
    Если у токена нет прав video — возвращает {} (видео не будут сохранены).
    """
    if not video_keys:
        return {}
    out = {}
    try:
        for i in range(0, len(video_keys), 200):
            chunk = video_keys[i : i + 200]
            resp = vk_request("video.get", {"videos": ",".join(chunk)})
            items = resp.get("items", []) if isinstance(resp, dict) else resp
            if isinstance(items, list):
                for v in items:
                    oid = v.get("owner_id")
                    vid = v.get("id")
                    player = v.get("player")
                    if oid is not None and vid is not None and player:
                        out[f"{oid}_{vid}"] = player
    except RuntimeError as e:
        print("Видео не загружены (нужен доступ video в токене):", e, file=sys.stderr)
    return out


def photo_url_from_attachment(att: dict) -> str | None:
    """Из вложения типа photo извлечь URL (приоритет: большие размеры)."""
    p = att.get("photo")
    if not p or not isinstance(p, dict):
        return None
    for key in ("photo_2560", "photo_1280", "photo_807", "photo_604", "photo_130"):
        if p.get(key):
            return p[key]
    sizes = p.get("sizes")
    if isinstance(sizes, list) and sizes:
        best = max(
            (s for s in sizes if isinstance(s, dict) and s.get("url")),
            key=lambda s: s.get("width") or 0,
            default=None,
        )
        if best:
            return best.get("url")
    return None


def download_and_optimize_image(url: str, out_dir: Path, base_name: str) -> str | None:
    """Скачать изображение, сжать для WEB (JPEG 1200px, quality 85). Возвращает имя файла или None."""
    try:
        req = Request(url, headers={"User-Agent": "SiberianMotorbearsBlog/1.0"})
        with urlopen(req, timeout=30) as r:
            data = r.read()
        if not HAS_PIL:
            ext = extension_from_url(url)
            dest = out_dir / (base_name + ext)
            dest.write_bytes(data)
            return dest.name
        img = Image.open(io.BytesIO(data))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > IMG_MAX_SIZE:
            if w >= h:
                new_w, new_h = IMG_MAX_SIZE, int(h * IMG_MAX_SIZE / w)
            else:
                new_w, new_h = int(w * IMG_MAX_SIZE / h), IMG_MAX_SIZE
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        dest = out_dir / (base_name + ".jpg")
        img.save(dest, "JPEG", quality=IMG_QUALITY, optimize=True)
        return dest.name
    except Exception:
        return None


def extension_from_url(url: str) -> str:
    """Используется только для имени файла до сохранения; итог всегда .jpg при оптимизации."""
    path = urlparse(url).path.lower()
    if ".jpg" in path or "jpeg" in path:
        return ".jpg"
    if ".png" in path:
        return ".png"
    if ".webp" in path:
        return ".webp"
    return ".jpg"


def normalize_post(
    post: dict,
    group_id: int,
    base_url: str,
    entry_num: int,
    video_map: dict,
    out_dir: Path,
) -> dict:
    """Привести пост к формату для фронта; скачать фото в out_dir."""
    pid = post.get("id")
    vk_url = f"{base_url}?w=wall-{group_id}_{pid}"
    photos_local: list[str] = []
    video_embed: str | None = None

    for a in post.get("attachments") or []:
        atype = a.get("type")
        if atype == "photo":
            url = photo_url_from_attachment(a)
            if url:
                base_name = f"entry_{entry_num}_{len(photos_local) + 1}"
                filename = download_and_optimize_image(url, out_dir, base_name)
                if filename:
                    photos_local.append(filename)
        elif atype == "video":
            v = a.get("video") or {}
            oid = v.get("owner_id")
            vid = v.get("id")
            if oid is not None and vid is not None and video_embed is None:
                key = f"{oid}_{vid}"
                video_embed = video_map.get(key)
                if not video_embed:
                    # Fallback: if video.get недоступен, пробуем URL без hash (для публичных видео может сработать)
                    video_embed = f"https://vk.com/video_ext.php?oid={oid}&id={vid}"

    return {
        "id": pid,
        "date": post.get("date", 0),
        "text": (post.get("text") or "").strip(),
        "vk_url": vk_url,
        "photos": photos_local,
        "video": {"embed_url": video_embed} if video_embed else None,
    }


def main() -> None:
    load_dotenv(ENV_FILE)
    token = os.environ.get("VK_ACCESS_TOKEN")
    if not token:
        print("Задайте VK_ACCESS_TOKEN в окружении или в scripts/.env", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    group_id = int(os.environ.get("VK_GROUP_ID", "197853818"))
    base_url = "https://vk.com/siberian_motorbears"

    posts = get_wall_posts(group_id, count=COUNT)
    if len(posts) < COUNT:
        print(f"Получено постов: {len(posts)}, ожидалось {COUNT}", file=sys.stderr)

    # Собрать все video attachment для одного запроса video.get
    video_keys: list[str] = []
    for post in posts:
        for a in post.get("attachments") or []:
            if a.get("type") == "video":
                v = a.get("video") or {}
                oid, vid = v.get("owner_id"), v.get("id")
                if oid is not None and vid is not None:
                    video_keys.append(f"{oid}_{vid}")
    video_map = fetch_video_players(video_keys)
    if video_keys:
        print("Видео для embed:", len(video_map), "из", len(video_keys), file=sys.stderr)

    for i, post in enumerate(posts):
        num = COUNT - i
        if num < 1:
            break
        data = normalize_post(post, group_id, base_url, num, video_map, OUT_DIR)
        path = OUT_DIR / f"entry_{num}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(path.name)

    print("Готово.", len(posts), "записей сохранено в", OUT_DIR)


if __name__ == "__main__":
    main()
