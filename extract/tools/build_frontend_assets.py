#!/usr/bin/env python3
"""Build frontend scenario-asset libraries from extract/generated_assets/*_assets.json.

Input : extract/generated_assets/<book>_assets.json (dict-style {source, chapters:[{assets}]}
        or list-style [{chapter, type, title, description, stimulus}])
Output: assets/assetlib-<book>.js  (one file per book, const _AL_<book>)
        assets.js                  (const ASSET_LIBS = [...], aggregator)

Regeneration: python extract\tools\build_frontend_assets.py
Legacy duplicates (truth_and_lies_assets.json, power_body_language_assets.json) are
retired to generated_assets/legacy/ and intentionally skipped.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(ROOT, "extract", "generated_assets")
ASSETS_DIR = os.path.join(ROOT, "assets")

TYPE_ALIASES = {"BEHAVIORAL_BOSS_BATTLE": "BOSS_BATTLE"}
DEFAULT_DIFFICULTY = {
    "CUE_SCRUBBER_STATION": "Beginner",
    "DYNAMIC_DIALOGUE_SIM": "Intermediate",
    "DECEPTION_AUDIT_FILE": "Intermediate",
    "DISCRIMINATION_MATRIX": "Advanced",
    "BOSS_BATTLE": "Advanced",
}
VALID_TYPES = set(DEFAULT_DIFFICULTY)

LEGACY = {"truth_and_lies_assets.json", "power_body_language_assets.json"}


def norm_asset(raw, fallback_difficulty):
    a = dict(raw)
    atype = TYPE_ALIASES.get(a.get("asset_type", a.get("type", "")), a.get("asset_type", a.get("type", "")))
    a["asset_type"] = atype
    if "topic" not in a and "title" in a:
        a["topic"] = a["title"]
    if "visual_frame_description" not in a and "stimulus" in a:
        a["visual_frame_description"] = a.get("stimulus", "")
    if "player_mission" not in a:
        a["player_mission"] = a.get("description", a.get("question", ""))
    if "key_concepts" not in a:
        a["key_concepts"] = [a["target_channel"]] if a.get("target_channel") else []
    if not a.get("difficulty_level"):
        a["difficulty_level"] = fallback_difficulty.get(atype, "Intermediate")
    return a


def book_id(filename):
    return os.path.basename(filename).replace("_assets.json", "")


def book_title(book, data):
    if isinstance(data, dict) and data.get("source"):
        return data["source"]
    return re.sub(r"[-_]", " ", book).title()


def load_book(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    book = book_id(path)
    if isinstance(data, dict) and "chapters" in data:
        chapters = []
        for ch in data["chapters"]:
            assets = [norm_asset(a, DEFAULT_DIFFICULTY) for a in ch.get("assets", [])]
            chapters.append({
                "id": ch.get("id", ""),
                "title": ch.get("title", ""),
                "pages": ch.get("pages", ""),
                "assets": assets,
            })
        return {"id": book, "title": book_title(book, data), "chapters": chapters}
    if isinstance(data, list):
        assets = [norm_asset(a, DEFAULT_DIFFICULTY) for a in data]
        chapters_by_id = {}
        for a in assets:
            cid = str(a.get("chapter", "all"))
            chapters_by_id.setdefault(cid, []).append(a)
        chapters = [{"id": cid, "title": cid, "assets": lst} for cid, lst in sorted(chapters_by_id.items())]
        return {"id": book, "title": book_title(book, data), "chapters": chapters}
    return None


def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    libs = []
    total = 0
    stats = {}
    for path in sorted(glob.glob(os.path.join(SRC_DIR, "*_assets.json"))):
        name = os.path.basename(path)
        if name in LEGACY:
            print(f"skip (legacy)  {name}")
            continue
        try:
            book = load_book(path)
        except json.JSONDecodeError as ex:
            print(f"skip (bad json) {name}: {ex}")
            continue
        if not book:
            print(f"skip (no assets) {name}")
            continue
        count = sum(len(c["assets"]) for c in book["chapters"])
        total += count
        for c in book["chapters"]:
            for a in c["assets"]:
                stats[a["asset_type"]] = stats.get(a["asset_type"], 0) + 1
        libs.append(book)
        out = os.path.join(ASSETS_DIR, f"assetlib-{book['id']}.js")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"// Scenario Lab asset library — {book['title']}\n")
            f.write(f"const _AL_{book['id']} = ")
            json.dump(book, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
        print(f"wrote {out} ({count} assets)")

    aggr = [
        "// Scenario Lab asset libraries — regenerate with:",
        "//   python extract\\tools\\build_frontend_assets.py",
        "const ASSET_LIBS = [",
        *[f"  _AL_{b['id']}," for b in libs],
        "];",
        "",
    ]
    with open(os.path.join(ROOT, "assets.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(aggr))

    print(f"\nlibraries: {len(libs)}, total assets: {total}")
    print("by type:", dict(sorted(stats.items())))


if __name__ == "__main__":
    main()
