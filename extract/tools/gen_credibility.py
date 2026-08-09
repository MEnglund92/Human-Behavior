# -*- coding: utf-8 -*-
"""Inject per-asset credibility ratings into all *_assets.json from phase7d profiles."""
import glob
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets")

profiles = json.load(io.open(os.path.join(OUT, "phase7d_credibility_profiles.json"), encoding="utf-8"))
by_id = {p["book_id"]: p for p in profiles}

SKIP = ("truth_and_lies_assets.json", "power_body_language_assets.json")
total = 0
for path in sorted(glob.glob(os.path.join(OUT, "*_assets.json"))):
    name = os.path.basename(path)
    if name in SKIP or "pages" in name:
        continue
    book_id = name.replace("_assets.json", "")
    profile = by_id[book_id]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    note = profile["note"].strip()
    if len(note) > 180:
        note = note[:177].rstrip() + "..."
    cred = {
        "level": profile["level"],
        "consensus": profile["consensus"],
        "basis": note,
    }
    n = 0
    for ch in data.get("chapters", []):
        for a in ch.get("assets", []):
            a["credibility"] = dict(cred)
            n += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    total += n
    print(f"{name:50s} {n:4d} assets  {cred['level']:6s} {cred['consensus']}")

print("TOTAL", total, "assets tagged")