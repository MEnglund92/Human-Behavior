"""Validate all generated asset libraries in extract/generated_assets/.

HARD checks (fail the run):
- file parses as JSON
- top level has "source" and "chapters" (list)
- each asset has an asset_type in the allowed set

SOFT checks (warnings only, matching historical conventions where older
files use e.g. difficulty "Expert"/"Novice" or 13+ key_concepts):
- required asset fields present
- difficulty in {Beginner, Intermediate, Advanced}
- key_concepts length 8-12
- no duplicated asset_type within one chapter (sub-sections are not
  represented in the schema, so this can only be a hint)

Usage:
    python extract/tools/validate.py [file.json ...]

With no args, validates every *_assets.json in generated_assets/.
"""

import glob
import json
import os
import sys

VALID_TYPES = {
    "CUE_SCRUBBER_STATION",
    "DYNAMIC_DIALOGUE_SIM",
    "DECEPTION_AUDIT_FILE",
    "DISCRIMINATION_MATRIX",
    "BOSS_BATTLE",
    "BEHAVIORAL_BOSS_BATTLE",
}
REQUIRED = [
    "asset_type",
    "domain",
    "topic",
    "visual_frame_description",
    "player_mission",
    "key_concepts",
    "difficulty_level",
]
VALID_DIFFICULTY = {"Beginner", "Intermediate", "Advanced"}
VALID_LEVEL = {"High", "Medium", "Low"}
VALID_CONSENSUS = {"Broad", "Emerging", "Contested"}

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(HERE, "..", "generated_assets")


def validate_file(path):
    errors = []
    warnings = []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        return [f"{path}: top level is not a JSON object"], 0, []
    if "source" not in data:
        errors.append(f"{path}: missing 'source'")
    chapters = data.get("chapters", [])
    if not isinstance(chapters, list):
        return [f"{path}: 'chapters' is not a list"], 0, []
    n_assets = 0
    seen_chapters = set()
    for ch in chapters:
        cid = ch.get("id", "?")
        if cid in seen_chapters:
            warnings.append(f"{path}: duplicate chapter id {cid!r}")
        seen_chapters.add(cid)
        for key in ("title", "pages"):
            if key not in ch:
                warnings.append(f"{path}: chapter {cid} missing {key!r}")
        assets = ch.get("assets", [])
        if not isinstance(assets, list):
            errors.append(f"{path}: chapter {cid} 'assets' is not a list")
            continue
        types_in_chapter = set()
        for a in assets:
            if not isinstance(a, dict):
                errors.append(f"{path}: chapter {cid} has non-object asset")
                continue
            n_assets += 1
            atype = a.get("asset_type")
            if atype not in VALID_TYPES:
                errors.append(f"{path}: chapter {cid} invalid asset_type {atype!r}")
            if atype in types_in_chapter:
                warnings.append(f"{path}: chapter {cid} duplicates asset_type {atype!r}")
            types_in_chapter.add(atype)
            for key in REQUIRED:
                if key not in a:
                    warnings.append(f"{path}: chapter {cid} asset missing {key!r}")
            diff = a.get("difficulty_level")
            if diff not in VALID_DIFFICULTY:
                warnings.append(f"{path}: chapter {cid} non-standard difficulty {diff!r}")
            cred = a.get("credibility")
            if not isinstance(cred, dict):
                errors.append(f"{path}: chapter {cid} asset missing credibility")
            else:
                if cred.get("level") not in VALID_LEVEL:
                    errors.append(f"{path}: chapter {cid} invalid credibility level {cred.get('level')!r}")
                if cred.get("consensus") not in VALID_CONSENSUS:
                    errors.append(f"{path}: chapter {cid} invalid credibility consensus {cred.get('consensus')!r}")
                if not cred.get("basis"):
                    errors.append(f"{path}: chapter {cid} credibility missing basis")
            kc = a.get("key_concepts")
            if isinstance(kc, list) and not (8 <= len(kc) <= 12):
                warnings.append(f"{path}: chapter {cid} key_concepts has {len(kc)} items (want 8-12)")
    return errors, n_assets, warnings


def main():
    files = sys.argv[1:]
    if not files:
        files = sorted(glob.glob(os.path.join(ASSETS_DIR, "*_assets.json")))
    total = 0
    ok = True
    n_warn = 0
    for path in files:
        try:
            errors, n, warnings = validate_file(path)
        except Exception as e:
            errors, n, warnings = [f"{path}: UNPARSEABLE ({e})"], 0, []
        status = "ALL VALID" if not errors else f"{len(errors)} ERROR(S)"
        print(f"{os.path.basename(path):50s} {n:4d} assets  {status}  ({len(warnings)} warnings)")
        for e in errors:
            print(f"    ERROR   {e}")
            ok = False
        for w in warnings:
            print(f"    warning {w}")
        total += n
        n_warn += len(warnings)
    print(f"\nTOTAL: {total} assets, {n_warn} warnings, {'ALL FILES VALID' if ok else 'FIX ERRORS ABOVE'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
