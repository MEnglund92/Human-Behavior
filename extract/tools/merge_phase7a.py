"""Merge validated Phase 7A batch outputs into a book-level *_assets.json.

Usage:
    python extract/tools/merge_phase7a.py <book_key> [batch_output.json ...]

With no batch files, merges every b*.output.json in
extract/generated_assets/phase7a/<book_key>/outputs/ (in batch order).
Writes extract/generated_assets/<book_key>_assets.json.
"""

import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, "..", "generated_assets")
BOOKS_DIR = os.path.join(GEN, "phase7a")


def chapter_key(c):
    m = re.match(r"(\d+)", str(c.get("id", "")))
    return int(m.group(1)) if m else 999


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_key")
    ap.add_argument("outputs", nargs="*")
    args = ap.parse_args()

    book_dir = os.path.join(BOOKS_DIR, args.book_key)
    if args.outputs:
        paths = args.outputs
    else:
        out_dir = os.path.join(book_dir, "outputs")
        paths = sorted(glob.glob(os.path.join(out_dir, "*_output.json")))

    if not paths:
        print(f"no batch outputs for {args.book_key}")
        sys.exit(1)

    chapters = []
    asset_total = 0
    for p in paths:
        with open(p, encoding="utf-8-sig") as f:
            data = json.load(f)
        chs = data.get("chapters", [])
        for ch in chs:
            chapters.append({
                "id": ch.get("id", ""),
                "title": ch.get("title", ""),
                "pages": ch.get("pages", ""),
                "assets": ch.get("assets", []),
            })
            asset_total += len(ch.get("assets", []))
    # keep batch order stable, then dedupe by chapter id
    seen = set()
    unique = []
    for ch in chapters:
        if ch["id"] in seen:
            print(f"skip duplicate chapter id {ch['id']!r}")
            continue
        seen.add(ch["id"])
        unique.append(ch)
    unique.sort(key=chapter_key)

    book_meta = {
        "source": f"Phase 7A: {args.book_key}",
        "weighted_modality": True,
        "chapters": unique,
    }
    out = os.path.join(GEN, f"{args.book_key}_assets.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(book_meta, f, ensure_ascii=False, indent=2)
    print(f"wrote {out}: {len(unique)} chapters, {asset_total} assets")


if __name__ == "__main__":
    main()
