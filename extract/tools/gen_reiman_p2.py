"""Phase 2 generator: per-chapter deep extraction for The Power of Body Language
(Tonya Reiman).

Adds one chapter entry (re10..re18) per book chapter (Ch1..Ch9), each with 5
assets (one per asset type, mirroring the part-level sub-section rule), while
keeping the existing topical entries (re01..re09) untouched.

Run from the repo root:
    python extract/tools/gen_reiman_p2.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets", "reiman_power_body_language_assets.json")

sys.path.insert(0, HERE)
from reiman_p2_data_a import CHAPTERS as DATA_A
from reiman_p2_data_b import CHAPTERS as DATA_B
from reiman_p2_data_c import CHAPTERS as DATA_C
from reiman_p2_data_d import CHAPTERS as DATA_D

CHAPTERS = DATA_A + DATA_B + DATA_C + DATA_D

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
    pages = ch["pages"]
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
        "id": "re%02d" % num,
        "title": "Chapter %d: %s" % (ch["num"], ch["title"]),
        "pages": pages,
        "assets": assets,
    }


def main():
    with open(OUT, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {ch.get("id") for ch in data["chapters"]}
    start = 10
    n = start
    added = 0
    for ch in CHAPTERS:
        cid = "re%02d" % n
        while cid in existing_ids:
            n += 1
            cid = "re%02d" % n
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
