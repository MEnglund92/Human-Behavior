"""Phase 2 generator: per-chapter deep extraction for Truth & Lies (Bowden & Thomson).

Adds one chapter entry (ch01..ch37) per book chapter, each with 5 assets (one
per asset type, mirroring the part-level sub-section rule), while keeping the
existing part-level entries (bo01..bo04) untouched.

Run from the repo root:
    python extract/tools/gen_bowden_p2.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets", "bowden_truth_lies_assets.json")

sys.path.insert(0, HERE)
from bowden_p2_data_a import CHAPTERS as DATA_A
from bowden_p2_data_b import CHAPTERS as DATA_B
from bowden_p2_data_c import CHAPTERS as DATA_C
from bowden_p2_data_d import CHAPTERS as DATA_D
from bowden_p2_data_e import CHAPTERS as DATA_E
from bowden_p2_data_f import CHAPTERS as DATA_F

CHAPTERS = DATA_A + DATA_B + DATA_C + DATA_D + DATA_E + DATA_F

SLOTS = {
    "scrub": ("CUE_SCRUBBER_STATION", "Beginner"),
    "dialogue": ("DYNAMIC_DIALOGUE_SIM", "Intermediate"),
    "audit": ("DECEPTION_AUDIT_FILE", "Intermediate"),
    "matrix": ("DISCRIMINATION_MATRIX", "Advanced"),
    "boss": ("BOSS_BATTLE", "Advanced"),
}


def build_chapter_entry(ch):
    """ch: dict with num, title, page, domain, scrub, dialogue, audit, matrix, boss
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
        "id": "ch%02d" % ch["num"],
        "title": "Chapter %d: %s" % (ch["num"], ch["title"]),
        "pages": pages,
        "assets": assets,
    }


def main():
    with open(OUT, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {ch.get("id") for ch in data["chapters"]}
    new_entries = [build_chapter_entry(ch) for ch in CHAPTERS]
    for entry in new_entries:
        if entry["id"] in existing_ids:
            print("WARNING: skipping duplicate chapter id", entry["id"])
            continue
        data["chapters"].append(entry)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total = sum(len(ch["assets"]) for ch in data["chapters"])
    print("wrote %s: %d chapter entries, %d assets" % (OUT, len(data["chapters"]), total))


if __name__ == "__main__":
    main()
