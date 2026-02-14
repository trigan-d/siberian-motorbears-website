#!/usr/bin/env python3
"""
Обновить локальную копию блога по последним 5 постам из VK:
1) Если пост уже есть у нас, но в VK изменён — обновить запись и картинки.
2) Если пост новый — добавить (entry_N+1.json и т.д.).
3) Если один из наших «последних» постов удалён в VK — удалить его и у нас.
4) Обновить список BLOG_ENTRIES в site/blog/index.html.
5) Перегенерировать 10 вшитых постов на странице блога.

Запуск из корня репозитория: python3 scripts/update_blog.py
Требуется VK_ACCESS_TOKEN в scripts/.env или в окружении.
"""
import json
import os
import re
import sys
from pathlib import Path

# Общая логика и настройки из save_blog_entries
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
import save_blog_entries as blog_save
from render_blog_initial import is_entry_file_empty

OUT_DIR = blog_save.OUT_DIR
ENV_FILE = blog_save.ENV_FILE
INDEX_HTML = REPO_ROOT / "site" / "blog" / "index.html"
FETCH_COUNT = 5


def load_existing_entries() -> dict[int, int]:
    """Прочитать все entry_*.json, вернуть { vk_post_id: entry_number }."""
    id_to_num = {}
    pat = re.compile(r"^entry_(\d+)\.json$")
    for p in OUT_DIR.glob("entry_*.json"):
        m = pat.match(p.name)
        if not m:
            continue
        num = int(m.group(1))
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            vk_id = data.get("id")
            if vk_id is not None:
                id_to_num[vk_id] = num
        except Exception:
            pass
    return id_to_num


def delete_entry_media(entry_num: int) -> None:
    """Удалить все файлы изображений для записи entry_num (entry_N_1.jpg и т.д.)."""
    prefix = f"entry_{entry_num}_"
    for p in OUT_DIR.iterdir():
        if p.is_file() and p.name.startswith(prefix) and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            p.unlink()


def delete_entry_fully(entry_num: int, id_to_num: dict) -> None:
    """Удалить запись целиком (json и медиа), индивидуальную страницу, манифест/sitemap; убрать из id_to_num."""
    delete_entry_media(entry_num)
    path = OUT_DIR / f"entry_{entry_num}.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            vk_id = data.get("id")
            if vk_id is not None:
                id_to_num.pop(vk_id, None)
        except Exception:
            pass
        path.unlink()
    import render_blog_entry_pages
    render_blog_entry_pages.delete_entry_page(entry_num)


def post_unchanged(vk_post: dict, our_data: dict) -> bool:
    """Проверить, совпадает ли пост из VK с нашей сохранённой записью (без загрузки медиа)."""
    if our_data.get("id") != vk_post.get("id"):
        return False
    if our_data.get("date") != vk_post.get("date"):
        return False
    text_vk = (vk_post.get("text") or "").strip()
    text_our = (our_data.get("text") or "").strip()
    if text_vk != text_our:
        return False
    photos_vk = sum(1 for a in (vk_post.get("attachments") or []) if a.get("type") == "photo")
    photos_our = len(our_data.get("photos") or [])
    if photos_vk != photos_our:
        return False
    has_video_vk = any(a.get("type") == "video" for a in (vk_post.get("attachments") or []))
    has_video_our = our_data.get("video") is not None
    if has_video_vk != has_video_our:
        return False
    return True


def get_all_entry_filenames_sorted_desc() -> list[str]:
    """Список имён entry_X.json по убыванию номера (новые первые)."""
    pat = re.compile(r"^entry_(\d+)\.json$")
    numbers = []
    for p in OUT_DIR.glob("entry_*.json"):
        m = pat.match(p.name)
        if m:
            numbers.append(int(m.group(1)))
    numbers.sort(reverse=True)
    return [f"entry_{n}.json" for n in numbers]


def update_index_blog_entries(filenames: list[str]) -> None:
    """Подставить в index.html массив BLOG_ENTRIES и BLOG_ENTRY_PAGES (без первых 10 — они вшиты)."""
    if not INDEX_HTML.exists():
        return
    text = INDEX_HTML.read_text(encoding="utf-8")
    # На странице вшиты первые 10 постов; в JS — остальные для подгрузки по скроллу
    js_entries = filenames[10:]
    if js_entries:
        new_array = "    var BLOG_ENTRIES = [\n      " + ",\n      ".join(f"'{f}'" for f in js_entries) + "\n    ];"
    else:
        new_array = "    var BLOG_ENTRIES = [];"

    pattern = re.compile(
        r"var BLOG_ENTRIES = \[\s*(?:'[^']*',?\s*)*\];",
        re.DOTALL,
    )
    if not pattern.search(text):
        print("В index.html не найден массив BLOG_ENTRIES.", file=sys.stderr)
        return
    new_text = pattern.sub(new_array, text, count=1)

    # BLOG_ENTRY_PAGES: entry_N.json → entry_N_slug.html (из манифеста страниц записей)
    manifest_path = INDEX_HTML.parent / "entry_pages_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entry_pages = {f"entry_{k}.json": v for k, v in manifest.items()}
    except Exception:
        entry_pages = {}
    new_entry_pages = "    var BLOG_ENTRY_PAGES = " + json.dumps(entry_pages, ensure_ascii=False) + ";"
    pattern_pages = re.compile(r"var BLOG_ENTRY_PAGES = \s*[^;]+;", re.DOTALL)
    if pattern_pages.search(new_text):
        new_text = pattern_pages.sub(new_entry_pages, new_text, count=1)

    INDEX_HTML.write_text(new_text, encoding="utf-8")
    print("Обновлён список BLOG_ENTRIES в index.html (записей для подгрузки:", len(js_entries), ")")


def main() -> None:
    blog_save.load_dotenv(ENV_FILE)
    token = os.environ.get("VK_ACCESS_TOKEN")
    if not token:
        print("Задайте VK_ACCESS_TOKEN в окружении или в scripts/.env", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    group_id = int(os.environ.get("VK_GROUP_ID", "197853818"))
    base_url = "https://vk.com/siberian_motorbears"

    id_to_num = load_existing_entries()
    max_num = max(id_to_num.values()) if id_to_num else 0

    posts = blog_save.get_wall_posts(group_id, count=FETCH_COUNT)
    if not posts:
        print("Нет постов от VK.", file=sys.stderr)
        sys.exit(1)

    video_keys = []
    for post in posts:
        for a in post.get("attachments") or []:
            if a.get("type") == "video":
                v = a.get("video") or {}
                oid, vid = v.get("owner_id"), v.get("id")
                if oid is not None and vid is not None:
                    video_keys.append(f"{oid}_{vid}")
    video_map = blog_save.fetch_video_players(video_keys)

    count_new = 0
    count_updated = 0
    count_unchanged = 0

    for post in posts:
        vk_id = post.get("id")
        if vk_id is None:
            continue
        if vk_id in id_to_num:
            entry_num = id_to_num[vk_id]
            path = OUT_DIR / f"entry_{entry_num}.json"
            try:
                our_data = json.loads(path.read_text(encoding="utf-8"))
                if post_unchanged(post, our_data):
                    count_unchanged += 1
                    print(f"  entry_{entry_num}.json — без изменений (VK id {vk_id})")
                    continue
            except Exception:
                pass
            delete_entry_media(entry_num)
            action = "обновлён"
            count_updated += 1
        else:
            max_num += 1
            entry_num = max_num
            id_to_num[vk_id] = entry_num
            action = "добавлен"
            count_new += 1

        data = blog_save.normalize_post(post, group_id, base_url, entry_num, video_map, OUT_DIR)
        path = OUT_DIR / f"entry_{entry_num}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  entry_{entry_num}.json — {action} (VK id {vk_id})")

    count_deleted = 0
    vk_ids_current = {p.get("id") for p in posts if p.get("id") is not None}
    filenames = get_all_entry_filenames_sorted_desc()
    for filename in filenames[:FETCH_COUNT]:
        path = OUT_DIR / filename
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            vk_id = data.get("id")
            if vk_id is not None and vk_id not in vk_ids_current:
                entry_num = int(path.stem.split("_")[1])
                delete_entry_fully(entry_num, id_to_num)
                count_deleted += 1
                print(f"  entry_{entry_num}.json — удалён (в VK удалён, id {vk_id})")
        except Exception:
            pass

    filenames = get_all_entry_filenames_sorted_desc()
    filenames = [f for f in filenames if not is_entry_file_empty(OUT_DIR / f)]
    update_index_blog_entries(filenames)

    # Индивидуальные страницы записей и sitemap
    import render_blog_entry_pages
    render_blog_entry_pages.main(count=len(filenames))

    # Перегенерировать 10 вшитых постов
    import render_blog_initial
    render_blog_initial.main()

    print("Готово.")
    print(f"Новых: {count_new}, отредактировано: {count_updated}, удалено: {count_deleted}, без изменений: {count_unchanged}.")


if __name__ == "__main__":
    main()
