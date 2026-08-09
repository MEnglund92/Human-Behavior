# -*- coding: utf-8 -*-
"""Merge authored cultural_variations into the 5 gesture libraries and rebuild frontend assets."""
import glob
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets")

PAIRS = [
    ("body_language_assets.json", ["phase7d_cv_body_language_out.json"]),
    ("definitive_body_language_assets.json", ["phase7d_cv_definitive_body_language_out1.json", "phase7d_cv_definitive_body_language_out2.json"]),
    ("dictionary_body_language_assets.json", ["phase7d_cv_dictionary_body_language_out.json"]),
    ("what_every_body_assets.json", ["phase7d_cv_what_every_body_out.json"]),
    ("reiman_power_body_language_assets.json", ["phase7d_cv_reiman_power_body_language_out1.json", "phase7d_cv_reiman_power_body_language_out2.json"]),
]

for lib, outs in PAIRS:
    with open(os.path.join(OUT, lib), encoding="utf-8") as f:
        data = json.load(f)
    by_key = {}
    for o in outs:
        arr = json.load(io.open(os.path.join(OUT, o), encoding="utf-8"))
        for item in arr:
            by_key[(item["chapter_id"], item["index"])] = item["cultural_variations"]
    n = 0
    for ch in data["chapters"]:
        for i, a in enumerate(ch.get("assets", [])):
            key = (ch["id"], i)
            if key in by_key:
                a["cultural_variations"] = by_key[key]
                n += 1
            elif "cultural_variations" in a:
                del a["cultural_variations"]
    with open(os.path.join(OUT, lib), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    total_assets = sum(len(ch.get("assets", [])) for ch in data["chapters"])
    assert n == total_assets, (lib, n, total_assets)
    print(f"{lib:50s} merged {n}/{total_assets}")

print("rebuilding frontend assets...")
r = subprocess.run([sys.executable, os.path.join(HERE, "build_frontend_assets.py")])
sys.exit(r.returncode)