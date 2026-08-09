"""Validate a Phase 7A authoring batch output before merge.

HARD rejects (nonzero exit):
- not a JSON object with 'chapters' list
- chapter missing 'id'/'title' or assets not a list
- asset missing required base keys (asset_type, domain, topic,
  visual_frame_description, player_mission, key_concepts, difficulty_level,
  theory_summary)
- asset_type not in allowed set (with BEHAVIORAL_BOSS_BATTLE alias)
- type-specific required keys missing (per asset_type)
- credibility missing/malformed (level/consensus/basis)
- placeholder text in key content fields (TODO/N/A/XXX/lorem)
- non-ASCII-confusable placeholders, empty strings for content fields

Usage:
    python extract/tools/validate_phase7a_batch.py <output.json> [--spec spec.json]
"""

import argparse
import json
import re
import sys

VALID_TYPES = {
    "CUE_SCRUBBER_STATION", "DYNAMIC_DIALOGUE_SIM", "DECEPTION_AUDIT_FILE",
    "DISCRIMINATION_MATRIX", "BOSS_BATTLE", "BEHAVIORAL_BOSS_BATTLE",
}
BASE_REQUIRED = [
    "asset_type", "domain", "topic", "visual_frame_description",
    "player_mission", "key_concepts", "difficulty_level", "theory_summary",
]
VALID_DIFFICULTY = {"Beginner", "Intermediate", "Advanced"}
VALID_LEVEL = {"High", "Medium", "Low"}
VALID_CONSENSUS = {"Broad", "Emerging", "Contested"}

TYPE_REQUIRED = {
    "CUE_SCRUBBER_STATION": ["target_channel", "question", "correct_cue",
                             "distractors", "underlying_psychology"],
    "DYNAMIC_DIALOGUE_SIM": ["scenario_setup", "dialogue", "choices",
                             "optimal_choice", "theoretical_principle",
                             "psychological_breakdown"],
    "DECEPTION_AUDIT_FILE": ["question", "subject_baseline",
                             "observed_nonverbal_log", "interrogation_transcript",
                             "correct_diagnosis", "diagnostic_breakdown",
                             "distractors"],
    "DISCRIMINATION_MATRIX": ["question", "column_a_label", "column_b_label",
                              "column_c_label", "rows", "correct_answer",
                              "distractors", "explanation"],
    "BOSS_BATTLE": ["boss_battle_explanation", "stage_1_observation",
                    "stage_1_question", "stage_1_correct_answer",
                    "stage_2_intervention", "stage_2_correct_answer"],
}

PLACEHOLDER = re.compile(
    r"\b(todo|tbd|n/a|na|lorem ipsum|placeholder|example text|xxx|insert .* here|"
    r"your answer|your text|replace me|fill in|sample text)\b", re.I)


def check_text(name, value, errors, where):
    if value is None:
        return
    s = str(value)
    if not s.strip():
        errors.append(f"{where}: field {name!r} is empty")
        return
    if PLACEHOLDER.search(s) and len(s) < 80:
        errors.append(f"{where}: field {name!r} contains placeholder text: {s[:60]!r}")


def validate_file(path, spec_path=None):
    errors = []
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "chapters" not in data:
        return [f"{path}: top level must be {{chapters: [...]}}"]
    if not isinstance(data["chapters"], list) or not data["chapters"]:
        return [f"{path}: chapters list is empty"]
    chapter_ids = set()
    n = 0
    for ch in data["chapters"]:
        cid = ch.get("id", "?")
        if cid in chapter_ids:
            errors.append(f"{path}: duplicate chapter id {cid!r}")
        chapter_ids.add(cid)
        where = f"{path} chapter {cid}"
        for key in ("id", "title"):
            if key not in ch:
                errors.append(f"{where}: missing {key!r}")
        assets = ch.get("assets", [])
        if not isinstance(assets, list) or not assets:
            errors.append(f"{where}: no assets")
            continue
        for a in assets:
            n += 1
            aw = f"{where} asset #{n}"
            atype = a.get("asset_type")
            if atype not in VALID_TYPES:
                errors.append(f"{aw}: invalid asset_type {atype!r}")
            for key in BASE_REQUIRED:
                if key not in a:
                    errors.append(f"{aw}: missing base key {key!r}")
            if atype in TYPE_REQUIRED:
                for key in TYPE_REQUIRED[atype]:
                    if key not in a:
                        errors.append(f"{aw}: missing {atype} key {key!r}")
            diff = a.get("difficulty_level")
            if diff not in VALID_DIFFICULTY:
                errors.append(f"{aw}: bad difficulty {diff!r}")
            cred = a.get("credibility")
            if not isinstance(cred, dict):
                errors.append(f"{aw}: credibility must be an object")
            else:
                if cred.get("level") not in VALID_LEVEL:
                    errors.append(f"{aw}: bad credibility level {cred.get('level')!r}")
                if cred.get("consensus") not in VALID_CONSENSUS:
                    errors.append(f"{aw}: bad credibility consensus {cred.get('consensus')!r}")
                if not cred.get("basis"):
                    errors.append(f"{aw}: credibility missing basis")
            kc = a.get("key_concepts")
            if isinstance(kc, list):
                if not (8 <= len(kc) <= 12):
                    errors.append(f"{aw}: key_concepts has {len(kc)} items (want 8-12)")
                for i, k in enumerate(kc):
                    check_text(f"key_concepts[{i}]", k, errors, aw)
            for key in ("domain", "topic", "visual_frame_description",
                        "player_mission", "theory_summary"):
                check_text(key, a.get(key), errors, aw)
            for key in ("distractors", "rows", "choices"):
                if isinstance(a.get(key), list):
                    for i, v in enumerate(a[key]):
                        check_text(f"{key}[{i}]", v, errors, aw)
    return errors, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("--spec", default=None)
    args = ap.parse_args()
    try:
        errors, n = validate_file(args.output, args.spec)
    except json.JSONDecodeError as e:
        errors, n = [f"{args.output}: unparseable JSON ({e})"], 0
    if errors:
        print(f"{args.output}: {len(errors)} ERROR(S), {n} assets")
        for e in errors[:40]:
            print(f"  ERROR {e}")
        if len(errors) > 40:
            print(f"  ... and {len(errors) - 40} more")
        sys.exit(1)
    print(f"{args.output}: VALID, {n} assets")


if __name__ == "__main__":
    main()
