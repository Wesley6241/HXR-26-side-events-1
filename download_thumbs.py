"""Download placeholder images to public/assets/thumbs. Run: python download_thumbs.py"""
import urllib.request
import os

THUMBS_DIR = os.path.join(os.path.dirname(__file__), "public", "assets", "thumbs")
URLS = [
    ("https://picsum.photos/id/10/400/300", "workshop1.jpg"),
    ("https://picsum.photos/id/11/400/300", "workshop2.jpg"),
    ("https://picsum.photos/id/12/400/300", "workshop3.jpg"),
    ("https://picsum.photos/id/13/400/300", "workshop4.jpg"),
    ("https://picsum.photos/id/14/400/300", "workshop5.jpg"),
]

for url, filename in URLS:
    path = os.path.join(THUMBS_DIR, filename)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            with open(path, "wb") as f:
                f.write(resp.read())
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed {filename}: {e}")
