"""Phase 2 generator: per-chapter deep extraction for The Laws of Human Nature
(Robert Greene).

Adds one chapter entry (lh00..lh18) per book section (Introduction, Law 1..18),
each with 5 assets (one per asset type), while keeping the existing topical
entries (introduction, ch01..ch18) untouched.

Run from the repo root:
    python extract/tools/gen_laws_p2.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets", "laws_human_nature_assets.json")

sys.path.insert(0, HERE)
from laws_p2_data_a import CHAPTERS as DATA_A
from laws_p2_data_b import CHAPTERS as DATA_B
from laws_p2_data_c import CHAPTERS as DATA_C

CHAPTERS = DATA_A + DATA_B + DATA_C

SLOTS = {
    "scrub": ("CUE_SCRUBBER_STATION", "Beginner"),
    "dialogue": ("DYNAMIC_DIALOGUE_SIM", "Intermediate"),
    "audit": ("DECEPTION_AUDIT_FILE", "Intermediate"),
    "matrix": ("DISCRIMINATION_MATRIX", "Advanced"),
    "boss": ("BOSS_BATTLE", "Advanced"),
}


def build_chapter_entry(ch, num):
    """ch: dict with num, title, pages, domain, scrub, dialogue, audit, matrix, boss
    Each slot is a 4-tuple (topic, mission, visual, concepts)."""
    assets = []
    for slot, (asset_type, difficulty) in SLOTS.items():
        topic, mission, visual, concepts = ch[slot]
        assets.append(
            {
                "asset_type": asset_type,
                "domain": ch["domain"],
                "topic": topic,
                "visual_frame_description": visual,
                "player_mission": mission,
                "key_concepts": concepts,
                "difficulty_level": difficulty,
            }
        )
    return {
        "id": "lh%02d" % num,
        "title": ch["title"],
        "pages": ch["pages"],
        "assets": assets,
    }


def main():
    with open(OUT, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {ch.get("id") for ch in data["chapters"]}
    n = 0
    added = 0
    for ch in CHAPTERS:
        cid = "lh%02d" % n
        while cid in existing_ids:
            n += 1
            cid = "lh%02d" % n
        entry = build_chapter_entry(ch, n)
        data["chapters"].append(entry)
        existing_ids.add(cid)
        n += 1
        added += 1
        print("added", cid, "-", entry["title"])

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total = sum(len(ch["assets"]) for ch in data["chapters"])
    print("wrote %s: %d chapter entries, %d assets" % (OUT, len(data["chapters"]), total))


if __name__ == "__main__":
    main()
