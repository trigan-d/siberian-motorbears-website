#!/usr/bin/env python3
"""
Удаление дубликатов в pictures/.

1) Точные дубликаты (одинаковый SHA256) в одной папке: оставить один файл, остальные удалить.
2) Имя-дубликаты в одной папке (например DSC01047.JPG и DSC01047_2.JPG): оставить файл
   с большим размером (как лучший по качеству), остальные с тем же базовым именем удалить.

По умолчанию --dry-run (только вывод). Запуск с --apply реально удаляет файлы.
"""
import hashlib
import re
import sys
from pathlib import Path
from collections import defaultdict

PICTURES = Path(__file__).resolve().parent.parent / "pictures"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}


def content_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_numbered_duplicate(stem: str) -> tuple[bool, str]:
    """
    Если stem имеет вид 'base_2', 'base_3' и т.д. (суффикс _целое >= 2), возвращаем (True, base).
    Иначе (False, stem).
    """
    m = re.match(r"^(.+)_(\d+)$", stem)
    if m and int(m.group(2)) >= 2:
        return True, m.group(1)
    return False, stem


def main():
    dry_run = "--apply" not in sys.argv
    if dry_run:
        print("DRY RUN (use --apply to actually delete)")

    deleted_count = 0

    # 1) По папкам: группы с одинаковым хешем в одной папке
    for folder in sorted(PICTURES.rglob("*")):
        if not folder.is_dir():
            continue
        by_hash = defaultdict(list)
        for f in folder.iterdir():
            if not f.is_file() or f.suffix not in IMAGE_EXT:
                continue
            try:
                by_hash[content_hash(f)].append(f)
            except Exception:
                continue
        for h, group in by_hash.items():
            if len(group) <= 1:
                continue
            group.sort(key=lambda p: p.name)
            keep, remove = group[0], group[1:]
            for p in remove:
                print(f"Exact duplicate (same content): remove {p.relative_to(PICTURES)}")
                if not dry_run:
                    p.unlink()
                    deleted_count += 1

    # 2) В каждой папке: только пары вида name.ext и name_2.ext (оставляем больший по размеру)
    for folder in sorted(PICTURES.rglob("*")):
        if not folder.is_dir():
            continue
        numbered = []  # (base_stem, path)
        rest = []      # (stem, path)
        for f in folder.iterdir():
            if not f.is_file() or f.suffix not in IMAGE_EXT:
                continue
            is_num, base = is_numbered_duplicate(f.stem)
            if is_num:
                numbered.append((base, f))
            else:
                rest.append((f.stem, f))
        rest_names = {s for s, _ in rest}
        # Обработать каждую базу один раз (есть и base, и base_2)
        bases_done = set()
        for base, path in numbered:
            if base not in rest_names or base in bases_done:
                continue
            bases_done.add(base)
            group = [p for s, p in rest if s == base] + [p for b, p in numbered if b == base]
            group.sort(key=lambda p: p.stat().st_size, reverse=True)
            keep, remove = group[0], group[1:]
            for p in remove:
                print(f"Name duplicate (keep larger): remove {p.relative_to(PICTURES)} (keep {keep.name})")
                if not dry_run:
                    p.unlink()
                    deleted_count += 1

    print(f"\nTotal removed: {deleted_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
