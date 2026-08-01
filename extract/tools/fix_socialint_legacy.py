"""Fix social_intelligence_assets.json legacy assets (ch01..ch21): add
player_mission, difficulty_level, visual_frame_description, and expand
key_concepts 8-12 from Phase-2 chapter data."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "generated_assets", "social_intelligence_assets.json")

sys.path.insert(0, HERE)
from socialint_p2_data_a import CHAPTERS as A
from socialint_p2_data_b import CHAPTERS as B
from socialint_p2_data_c import CHAPTERS as C
from socialint_p2_data_d import CHAPTERS as D
from socialint_p2_data_e import CHAPTERS as E

CHAPTERS = A + B + C + D + E
SLOTS = ("scrub", "dialogue", "audit", "matrix", "boss")
TYPE_SLOT = {
    "CUE_SCRUBBER_STATION": "scrub",
    "DYNAMIC_DIALOGUE_SIM": "dialogue",
    "DECEPTION_AUDIT_FILE": "audit",
    "DISCRIMINATION_MATRIX": "matrix",
    "BOSS_BATTLE": "boss",
    "BEHAVIORAL_BOSS_BATTLE": "boss",
}
DEFAULT_DIFF = {
    "CUE_SCRUBBER_STATION": "Beginner",
    "DYNAMIC_DIALOGUE_SIM": "Intermediate",
    "DECEPTION_AUDIT_FILE": "Intermediate",
    "DISCRIMINATION_MATRIX": "Advanced",
    "BOSS_BATTLE": "Advanced",
}


def chapter_for(num):
    return next(c for c in CHAPTERS if c["num"] == num)


def pool_for(num):
    ch = chapter_for(num)
    seen = []
    for slot in SLOTS:
        for c in ch[slot][3]:
            if c not in seen:
                seen.append(c)
    return seen


def visual_for(num, atype):
    return chapter_for(num)[TYPE_SLOT.get(atype, "scrub")][2]


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    for ch in data["chapters"]:
        cid = ch["id"]
        if not (cid.startswith("ch") and cid[2:].isdigit()):
            continue
        num = int(cid[2:])
        pool = pool_for(num)
        for a in ch["assets"]:
            changed = False
            if "player_mission" not in a:
                a["player_mission"] = a.get("question", a.get("description", ""))
                changed = True
            if not a.get("difficulty_level"):
                a["difficulty_level"] = DEFAULT_DIFF.get(a["asset_type"], "Intermediate")
                changed = True
            if "visual_frame_description" not in a:
                a["visual_frame_description"] = visual_for(num, a["asset_type"])
                changed = True
            kc = a.get("key_concepts") or []
            for c in pool:
                if len(kc) >= 12:
                    break
                if c not in kc:
                    kc.append(c)
                    changed = True
            a["key_concepts"] = kc
            if changed:
                fixed += 1

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    bad = [(c["id"], len(a["key_concepts"])) for c in data["chapters"] for a in c["assets"]
           if not 8 <= len(a["key_concepts"]) <= 12]
    missing = [(c["id"], a["asset_type"]) for c in data["chapters"] for a in c["assets"]
               if "player_mission" not in a or "difficulty_level" not in a or "visual_frame_description" not in a]
    total = sum(len(c["assets"]) for c in data["chapters"])
    print("fixed:", fixed)
    print("bad concept counts:", bad)
    print("missing fields:", missing)
    print("assets:", total)


if __name__ == "__main__":
    main()
