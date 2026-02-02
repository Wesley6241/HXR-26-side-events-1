Placeholder images: part of the library and used to fill empty slots.

- index/gallery load from public/placeholders/ (same base as public/data/, public/assets/).
- Run once from project root: python rename_placeholders.py
  That copies/renames images from placeholders/ to public/placeholders/ and writes manifest.json there.
  Without this step, images will 404 and you will see "Placeholder 1", "Placeholder 2" text instead of pictures.

Naming: use numbers 1, 2, 3, ... (formats .jpg, .jpeg, .png, .webp). The script normalizes non-number filenames (same number extends).
