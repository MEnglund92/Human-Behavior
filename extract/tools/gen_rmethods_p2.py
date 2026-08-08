#!/usr/bin/env python3
"""Phase 3 generator: per-chapter deep extraction for the Handbook of Research
Methods in Social and Personality Psychology (3rd ed., Reis, West & Judd, 2024).

One authoring agent per chapter produced extract/tools/rmethods_p2_chNN.py
(each defines a single CHAPTER dict). This generator loads all of them and
writes the dict-style library to generated_assets/research_methods_assets.json
REPLACING the legacy flat 28-asset library (approved at integration time).

Run from the repo root:
    python extract/tools/gen_rmethods_p2.py
"""

import glob
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmethods_p2_map import CHAPTERS as MAP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets", "research_methods_assets.json")

SLOTS = {
    "scrub": ("CUE_SCRUBBER_STATION", "Beginner"),
    "dialogue": ("DYNAMIC_DIALOGUE_SIM", "Intermediate"),
    "audit": ("DECEPTION_AUDIT_FILE", "Intermediate"),
    "matrix": ("DISCRIMINATION_MATRIX", "Advanced"),
    "boss": ("BOSS_BATTLE", "Advanced"),
}


def load_chapters():
    chapters = []
    for path in sorted(glob.glob(os.path.join(HERE, "rmethods_p2_ch*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ch = dict(mod.CHAPTER)
        meta = next((m for m in MAP if m["num"] == ch["num"]), None)
        if meta:
            ch["pages"] = meta["pages"]
            ch["title"] = meta["title"]
        chapters.append(ch)
    chapters.sort(key=lambda c: c["num"])
    return chapters


def build_chapter_entry(ch, num):
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
        "id": "rm%02d" % num,
        "title": ("Introduction" if num == 0 else "Chapter %d: %s" % (ch["num"], ch["title"])),
        "pages": ch["pages"],
        "assets": assets,
    }


def main():
    chapters = load_chapters()
    data = {
        "source": "Handbook of Research Methods in Social and Personality Psychology, 3rd ed. (Reis, West & Judd, 2024)",
        "chapters": [build_chapter_entry(ch, n) for n, ch in enumerate(chapters, 0)],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("wrote %d chapters / %d assets -> %s" % (len(chapters), len(chapters) * 5, OUT))


if __name__ == "__main__":
    main()
