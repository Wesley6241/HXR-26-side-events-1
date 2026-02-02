#!/usr/bin/env python3
"""
Rename placeholder images to numeric names (1, 2, 3, ...) and output to public/placeholders/.
- Reads from placeholders/ (or public/placeholders/ if you put images there).
- Writes to public/placeholders/ so index/gallery can load them (same base as public/data/, public/assets/).
- Same number extends: e.g. 1.jpeg, 1.png -> 1.jpeg, 2.png
Run from project root: python rename_placeholders.py
"""

import json
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_ROOT / "placeholders"
TARGET_DIR = PROJECT_ROOT / "public" / "placeholders"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SKIP_FILES = {"README.txt", "manifest.json"}


def key_for_sort(path: Path) -> tuple:
    """Sort: numeric stem first (by value), then non-numeric by filename."""
    stem = path.stem
    try:
        n = int(stem)
        return (0, n, path.name)
    except ValueError:
        return (1, 0, path.name)


def main():
    # Prefer source from placeholders/; fallback to public/placeholders/ if only that has images
    if SOURCE_DIR.is_dir():
        src_dir = SOURCE_DIR
    elif TARGET_DIR.is_dir():
        src_dir = TARGET_DIR
    else:
        print("Neither placeholders/ nor public/placeholders/ found. Create placeholders/ and add images.")
        return
    files = [
        f
        for f in src_dir.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS and f.name not in SKIP_FILES
    ]
    files.sort(key=key_for_sort)
    if not files:
        print("No image files found.")
        return
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    ext_map = {}
    for i, path in enumerate(files, start=1):
        ext = path.suffix.lower().lstrip(".")
        ext_map[str(i)] = ext
        target_file = TARGET_DIR / f"{i}{path.suffix}"
        if path.resolve() != target_file.resolve():
            shutil.copy2(path, target_file)
        print(f"  {target_file.name}")
    obj = {"indices": list(range(1, len(files) + 1)), "extensions": ext_map}
    manifest = TARGET_DIR / "manifest.json"
    manifest.write_text(json.dumps(obj, indent=0), encoding="utf-8")
    print(f"Wrote {manifest}. {len(files)} files in public/placeholders/.")


if __name__ == "__main__":
    main()
