#!/usr/bin/env python3
"""
Сортировка фотографий из original_photos в pictures по PHOTO_SORTING_MAP.md.
- Дедупликация по хешу содержимого (construction/final/others — один экземпляр на хеш;
  trip_reports может повторять final, внутри trip_reports — без дубликатов).
- Ресайз только если длинная сторона > MAX_SIDE (1920), соотношение сторон не менять.
- Исключения: .mp4, .eps, .zip, .pdf, папки spam, файлы (copy).
"""
import os
import re
import hashlib
import shutil
from pathlib import Path
from PIL import Image

PROJECT = Path(__file__).resolve().parent.parent
ORIGINAL = PROJECT / "original_photos"
PICTURES = PROJECT / "pictures"
MAX_SIDE = 1920
JPEG_QUALITY = 88
SKIP_EXT = {".mp4", ".eps", ".zip", ".pdf", ".gif"}
SKIP_SUBPATHS = ["/spam/", " (copy)", "(copy)", " copy."]
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}


def should_skip(path: Path) -> bool:
    p = path.as_posix()
    for skip in SKIP_SUBPATHS:
        if skip in p:
            return True
    if path.suffix in SKIP_EXT:
        return True
    if path.suffix not in IMAGE_EXT:
        return True
    return False


def content_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sanitize_name(name: str) -> str:
    name = re.sub(r"[\s()]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "image"


def resize_if_needed(src: Path, dst: Path, do_resize: bool = True) -> None:
    if not do_resize:
        shutil.copy2(src, dst)
        return
    try:
        img = Image.open(src)
    except Exception:
        shutil.copy2(src, dst)
        return
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    if max(w, h) <= MAX_SIDE:
        shutil.copy2(src, dst)
        return
    ratio = MAX_SIDE / max(w, h)
    nw, nh = int(w * ratio), int(h * ratio)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    out_ext = dst.suffix.lower()
    if out_ext in (".jpg", ".jpeg"):
        img.save(dst, "JPEG", quality=JPEG_QUALITY, optimize=True)
    else:
        img.save(dst, "PNG", optimize=True)


# Маппинг: (путь относительно original_photos или префикс) -> (база в pictures, construction | final)
# Формат: (path_prefix, is_construction) -> target_dir e.g. ("baribal", True) -> "baribal/barney/construction"
def build_rules():
    return [
        # baribal barney
        (("baribal", "baribal/parts", "baribal/prof_photo"), "baribal/barney/construction"),
        (("baribal/sale", "baribal/site"), "baribal/barney/final"),  # site и все подпапки обработаем отдельно
        (("rv_construction/baribal",), "baribal/barney/construction"),
        (("goods_15/baribal barney",), "baribal/barney/final"),
        # baribal baron
        (("baribal2/ящики",), "baribal/baron/construction"),
        (("baribal2/site",), "baribal/baron/final"),
        (("baron/photo",), "baribal/baron/final"),
        (("rv_construction/baribal2",), "baribal/baron/construction"),
        (("goods_15/baribal baron",), "baribal/baron/final"),
        (("goods_15/baribals",), "baribal/baron/final"),
        # panda mia
        (("panda mia/production",), "panda/mia/construction"),
        (("panda mia/website", "panda mia/VK"), "panda/mia/final"),
        (("rv_construction/panda",), "panda/mia/construction"),
        (("goods_15/construction_examples/panda",), "panda/mia/construction"),
        # grizzly green
        (("sale_grizzly",), "grizzly/green/final"),
        (("гризли грин в гугл фото",), "grizzly/green/final"),  # по умолчанию final
        (("rv_construction/grizly",), "grizzly/green/construction"),
        # polar potap
        (("sale_potap", "polar_potap"), "polar/potap/final"),
        (("rv_construction/potap",), "polar/potap/construction"),
        # others
        (("fiat",), "others/fiat_krasnoyarsk/final"),
        (("goods_15/construction_examples/fiat",), "others/fiat_krasnoyarsk/construction"),
        (("asmp",), "others/trekol_asmp/construction"),
        (("trekol", "rv_construction/trekol"), "others/trekol_asmp/construction"),
        (("goods_15/construction_examples/trekol",), "others/trekol_asmp/construction"),
        (("rv_construction/unfinished",), "others/unfinished/construction"),
        (("гризли нг 2023",), "others/grizzly_ng2023/final"),
        # trip_reports
        (("rental_page", "tomsk"), "trip_reports"),
    ]


def get_target(rel_path: str, rules: list) -> str | None:
    rel = rel_path.replace("\\", "/")
    # baribal/sale и baribal/site (и подпапки) -> barney final (приоритет перед общим baribal)
    if rel.startswith("baribal/sale") or rel.startswith("baribal/site"):
        return "baribal/barney/final"
    # baribal root (IMG_*, car1) -> barney construction
    if rel.startswith("baribal/") and rel.count("/") == 1:
        return "baribal/barney/construction"
    # baribal2 root: только .jpg/.jpeg (без .eps, .zip, .png)
    if rel.startswith("baribal2/") and rel.count("/") == 1:
        if rel.lower().endswith((".jpg", ".jpeg")):
            return "baribal/baron/construction"
        return None
    # panda mia root (photo_*)
    if rel.startswith("panda mia/") and rel.count("/") == 1:
        return "panda/mia/final"
    # root files: baikal, aNQOi5aFSGQ
    if "/" not in rel and (rel.lower().startswith("baikal") or "anqoi" in rel.lower()):
        return "trip_reports"
    # goods_15/panda (без construction_examples) -> final
    if rel.startswith("goods_15/panda/") and "construction_examples" not in rel:
        return "panda/mia/final"
    for prefixes, target in rules:
        for prefix in prefixes:
            if rel.startswith(prefix + "/") or rel == prefix:
                return target
    return None


def collect_files(only_prefixes: list[str] | None = None):
    files_to_copy = []
    for root, dirs, files in os.walk(ORIGINAL, topdown=True):
        dirs[:] = [d for d in dirs if "spam" not in d.lower()]
        root_path = Path(root)
        try:
            rel_base = root_path.relative_to(ORIGINAL).as_posix().replace("\\", "/")
        except ValueError:
            continue
        if only_prefixes:
            if not any(rel_base.startswith(p) or p.startswith(rel_base) for p in only_prefixes):
                continue
        for f in files:
            src = root_path / f
            if should_skip(src):
                continue
            rel = (root_path / f).relative_to(ORIGINAL).as_posix().replace("\\", "/")
            target_dir = get_target(rel, build_rules())
            if target_dir:
                files_to_copy.append((src, PICTURES / target_dir))
    return files_to_copy


def existing_hashes_in_pictures():
    """Хеши уже лежащих в pictures файлов (для инкрементального запуска)."""
    seen = set()
    for path in PICTURES.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXT:
            continue
        try:
            seen.add(content_hash(path))
        except Exception:
            pass
    return seen


def existing_hashes_trip_reports():
    seen = set()
    trip_dir = PICTURES / "trip_reports"
    if not trip_dir.exists():
        return seen
    for path in trip_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXT:
            continue
        try:
            seen.add(content_hash(path))
        except Exception:
            pass
    return seen


def main():
    import sys
    do_resize = "--no-resize" not in sys.argv
    only_prefixes = None
    for i, a in enumerate(sys.argv):
        if a == "--only" and i + 1 < len(sys.argv):
            only_prefixes = [p.strip() for p in sys.argv[i + 1].split(",")]
            break
    os.chdir(PROJECT)
    rules = build_rules()
    files_to_copy = collect_files(only_prefixes=only_prefixes)
    seen_hash_main = set()
    seen_hash_trip = set()
    if only_prefixes:
        seen_hash_main = existing_hashes_in_pictures()
        seen_hash_trip = existing_hashes_trip_reports()
    name_count = {}
    copied = 0
    skipped_dup = 0
    errors = []

    for src, dest_dir in files_to_copy:
        if not src.exists():
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        h = content_hash(src)
        is_trip = "trip_reports" in dest_dir.as_posix()
        if is_trip:
            if h in seen_hash_trip:
                skipped_dup += 1
                continue
        else:
            if h in seen_hash_main:
                skipped_dup += 1
                continue

        base = sanitize_name(src.stem) + src.suffix
        key = (dest_dir, base)
        name_count[key] = name_count.get(key, 0) + 1
        n = name_count[key]
        if n > 1:
            base = sanitize_name(src.stem) + f"_{n}" + src.suffix
        dest = dest_dir / base

        try:
            resize_if_needed(src, dest, do_resize=do_resize)
            copied += 1
            if is_trip:
                seen_hash_trip.add(h)
            else:
                seen_hash_main.add(h)
        except Exception as e:
            errors.append((str(src), str(e)))

    print(f"Copied: {copied}, Skipped duplicates: {skipped_dup}")
    for s, e in errors[:20]:
        print(f"Error: {s} -> {e}")
    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more errors")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
