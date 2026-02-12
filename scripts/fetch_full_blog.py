#!/usr/bin/env python3
"""
Одноразовая полная выкачка ленты блога из VK: очистить entries,
загрузить все посты с пагинацией (VK API не более 100 за запрос),
сохранить entry_1.json (самый старый) … entry_N.json (самый новый),
обновить index.html и вшитые 10 постов.

Запуск из корня репозитория: python3 scripts/fetch_full_blog.py
Требуется VK_ACCESS_TOKEN в scripts/.env или в окружении.
"""
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
import save_blog_entries as blog_save
from render_blog_initial import is_entry_file_empty

OUT_DIR = blog_save.OUT_DIR
ENV_FILE = blog_save.ENV_FILE
INDEX_HTML = REPO_ROOT / "site" / "blog" / "index.html"
WALL_PAGE_SIZE = 100  # лимит VK API за один запрос


def get_wall_posts_page(owner_id: int, offset: int, count: int = WALL_PAGE_SIZE) -> list:
    """Одна страница wall.get (до 100 записей)."""
    resp = blog_save.vk_request(
        "wall.get",
        {"owner_id": -owner_id, "count": count, "offset": offset, "filter": "owner"},
    )
    return resp.get("items", [])


def fetch_all_wall_posts(owner_id: int) -> list:
    """Вся лента постами (пагинация по 100). Новые первые в ответе VK — возвращаем от старых к новым."""
    all_posts = []
    offset = 0
    while True:
        page = get_wall_posts_page(owner_id, offset)
        if not page:
            break
        all_posts.extend(page)
        if len(page) < WALL_PAGE_SIZE:
            break
        offset += WALL_PAGE_SIZE
        print(f"  загружено {len(all_posts)} постов…", file=sys.stderr)
    # VK отдаёт от новых к старым; для entry_1=старый, entry_N=новый переворачиваем
    all_posts.reverse()
    return all_posts


def clear_entries_dir() -> None:
    """Удалить все entry_*.json и entry_*_* (медиа) в папке entries."""
    for p in OUT_DIR.iterdir():
        if not p.is_file():
            continue
        if (p.name.startswith("entry_") and p.suffix.lower() == ".json") or (
            re.match(r"^entry_\d+_\d+\.", p.name)
        ):
            p.unlink()
    print("Папка entries очищена.", file=sys.stderr)


def get_all_entry_filenames_sorted_desc() -> list[str]:
    """Имена entry_X.json по убыванию номера."""
    pat = re.compile(r"^entry_(\d+)\.json$")
    numbers = []
    for p in OUT_DIR.glob("entry_*.json"):
        m = pat.match(p.name)
        if m:
            numbers.append(int(m.group(1)))
    numbers.sort(reverse=True)
    return [f"entry_{n}.json" for n in numbers]


def update_index_blog_entries(filenames: list[str]) -> None:
    """Подставить в index.html массив BLOG_ENTRIES (без первых 10 — они вшиты)."""
    if not INDEX_HTML.exists():
        return
    text = INDEX_HTML.read_text(encoding="utf-8")
    js_entries = filenames[10:]
    if js_entries:
        new_array = "    var BLOG_ENTRIES = [\n      " + ",\n      ".join(f"'{f}'" for f in js_entries) + "\n    ];"
    else:
        new_array = "    var BLOG_ENTRIES = [];"
    pattern = re.compile(r"var BLOG_ENTRIES = \[\s*(?:'[^']*',?\s*)*\];", re.DOTALL)
    if not pattern.search(text):
        print("В index.html не найден массив BLOG_ENTRIES.", file=sys.stderr)
        return
    new_text = pattern.sub(new_array, text, count=1)
    INDEX_HTML.write_text(new_text, encoding="utf-8")


def main() -> None:
    blog_save.load_dotenv(ENV_FILE)
    if not os.environ.get("VK_ACCESS_TOKEN"):
        print("Задайте VK_ACCESS_TOKEN в окружении или в scripts/.env", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    group_id = int(os.environ.get("VK_GROUP_ID", "197853818"))
    base_url = "https://vk.com/siberian_motorbears"

    clear_entries_dir()

    print("Загрузка ленты с пагинацией…", file=sys.stderr)
    posts = fetch_all_wall_posts(group_id)
    if not posts:
        print("Постов не получено.", file=sys.stderr)
        sys.exit(1)
    print(f"Всего постов: {len(posts)}", file=sys.stderr)

    video_keys = []
    for post in posts:
        for a in post.get("attachments") or []:
            if a.get("type") == "video":
                v = a.get("video") or {}
                oid, vid = v.get("owner_id"), v.get("id")
                if oid is not None and vid is not None:
                    video_keys.append(f"{oid}_{vid}")
    video_map = blog_save.fetch_video_players(video_keys)

    for i, post in enumerate(posts):
        entry_num = i + 1
        data = blog_save.normalize_post(post, group_id, base_url, entry_num, video_map, OUT_DIR)
        path = OUT_DIR / f"entry_{entry_num}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        if entry_num % 50 == 0 or entry_num == len(posts):
            print(f"  сохранено {entry_num}/{len(posts)}", file=sys.stderr)

    filenames = get_all_entry_filenames_sorted_desc()
    filenames = [f for f in filenames if not is_entry_file_empty(OUT_DIR / f)]
    update_index_blog_entries(filenames)

    import render_blog_initial
    render_blog_initial.main()

    print("Готово. Записей:", len(posts), file=sys.stderr)


if __name__ == "__main__":
    main()
