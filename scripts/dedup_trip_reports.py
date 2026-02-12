#!/usr/bin/env python3
"""
Дедупликация pictures/trip_reports/ по перцептивному хешу (почти одинаковые фото).

- Считает average hash (aHash) для каждого изображения через PIL.
- Группирует фото с расстоянием Хэмминга <= threshold (по умолчанию 3).
- В каждой группе оставляет один файл (самый большой по размеру), остальные удаляет.

Использование:
  python3 dedup_trip_reports.py              # dry-run
  python3 dedup_trip_reports.py --apply      # реально удалить
  python3 dedup_trip_reports.py --threshold 5   # более агрессивное слияние (больше дублей)
"""
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Установите Pillow: pip install Pillow")
    sys.exit(1)

TRIP_REPORTS = Path(__file__).resolve().parent.parent / "pictures" / "trip_reports"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
DEFAULT_THRESHOLD = 3
HASH_SIZE = 8  # 8x8 → 64 бита


def ahash(path: Path) -> int | None:
    """Average hash: 8x8 grayscale, бит 1 если пиксель >= среднее."""
    try:
        with Image.open(path) as img:
            img = img.convert("L").resize((HASH_SIZE, HASH_SIZE), Image.Resampling.LANCZOS)
            pixels = list(img.getdata())
            avg = sum(pixels) / len(pixels)
            bits = 0
            for i, p in enumerate(pixels):
                if p >= avg:
                    bits |= 1 << i
            return bits
    except Exception:
        return None


def hamming(a: int, b: int) -> int:
    x = a ^ b
    n = 0
    while x:
        n += x & 1
        x >>= 1
    return n


def main():
    args = [a for a in sys.argv[1:] if a != "--apply"]
    dry_run = "--apply" not in sys.argv
    threshold = DEFAULT_THRESHOLD
    for i, a in enumerate(args):
        if a == "--threshold" and i + 1 < len(args):
            try:
                threshold = int(args[i + 1])
            except ValueError:
                pass
            break

    if not TRIP_REPORTS.is_dir():
        print(f"Папка не найдена: {TRIP_REPORTS}")
        return 1

    if dry_run:
        print("DRY RUN (use --apply to actually delete)")
    print(f"Threshold (Hamming): {threshold}")

    files = [f for f in TRIP_REPORTS.iterdir() if f.is_file() and f.suffix in IMAGE_EXT]
    if not files:
        print("Нет изображений в trip_reports.")
        return 0

    # Вычисляем хеши
    hashes = {}
    for f in files:
        h = ahash(f)
        if h is not None:
            hashes[f] = h
        else:
            print(f"Skip (не удалось прочитать): {f.name}")

    paths = list(hashes.keys())
    n = len(paths)

    # Union-Find: объединяем пары с расстоянием <= threshold
    parent = list(range(n))

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        pi, pj = find(i), find(j)
        if pi != pj:
            parent[pi] = pj

    for i in range(n):
        for j in range(i + 1, n):
            if hamming(hashes[paths[i]], hashes[paths[j]]) <= threshold:
                union(i, j)

    # Группы по корню
    groups = {}
    for i in range(n):
        root = find(i)
        groups.setdefault(root, []).append(paths[i])

    deleted_count = 0
    for root, group in groups.items():
        if len(group) <= 1:
            continue
        # Оставляем самый большой файл
        group.sort(key=lambda p: p.stat().st_size, reverse=True)
        keep, remove = group[0], group[1:]
        for p in remove:
            print(f"Near-duplicate: remove {p.name} (keep {keep.name})")
            if not dry_run:
                p.unlink()
                deleted_count += 1

    print(f"\nTotal removed: {deleted_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
