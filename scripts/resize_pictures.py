#!/usr/bin/env python3
"""Ресайз изображений в pictures/ если длинная сторона > MAX_SIDE. Соотношение сторон не менять."""
from pathlib import Path
from PIL import Image

PICTURES = Path(__file__).resolve().parent.parent / "pictures"
MAX_SIDE = 1920
JPEG_QUALITY = 88

def main():
    resized = 0
    for path in PICTURES.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        try:
            img = Image.open(path)
        except Exception:
            continue
        w, h = img.size
        if max(w, h) <= MAX_SIDE:
            continue
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        ratio = MAX_SIDE / max(w, h)
        nw, nh = int(w * ratio), int(h * ratio)
        img = img.resize((nw, nh), Image.Resampling.LANCZOS)
        ext = path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            img.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True)
        else:
            img.save(path, "PNG", optimize=True)
        resized += 1
    print(f"Resized: {resized}")

if __name__ == "__main__":
    main()
