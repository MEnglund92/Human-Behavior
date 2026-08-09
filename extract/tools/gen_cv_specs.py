# -*- coding: utf-8 -*-
"""Generate per-asset cultural_variations authoring specs for gesture-heavy libraries."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets")

LIBRARIES = [
    "body_language_assets.json",
    "definitive_body_language_assets.json",
    "dictionary_body_language_assets.json",
    "what_every_body_assets.json",
    "reiman_power_body_language_assets.json",
]
MAX_PER_SPEC = 100

for path in LIBRARIES:
    with open(os.path.join(OUT, path), encoding="utf-8") as f:
        d = json.load(f)
    book_id = path.replace("_assets.json", "")
    entries = []
    for ch in d["chapters"]:
        for i, a in enumerate(ch.get("assets", [])):
            frame = (a.get("visual_frame_description") or a.get("topic") or "")[:200]
            entries.append({
                "chapter_id": ch["id"],
                "index": i,
                "asset_type": a.get("asset_type"),
                "topic": a.get("topic"),
                "frame_excerpt": frame,
            })
    n_batches = (len(entries) + MAX_PER_SPEC - 1) // MAX_PER_SPEC
    for b in range(n_batches):
        chunk = entries[b * MAX_PER_SPEC:(b + 1) * MAX_PER_SPEC]
        spec = {
            "job": "cultural_variations",
            "book_id": book_id,
            "task": (
                "For each asset below, write 1-3 short cross-cultural notes for the gesture / body-language / "
                "proximity / eye-contact / touch claim it makes. Purpose: the app shows these as caveats so learners "
                "don't over-generalize US/Eurocentric findings. Rules: each note is 4-14 words; each starts with a "
                "culture/region; focus on genuine documented variation (e.g. 'Thumbs-up is offensive in Iran and "
                "parts of Africa', 'OK hand sign is vulgar in Brazil and Turkey', 'direct eye contact reads as "
                "disrespectful in many East Asian and Indigenous cultures', 'personal space is smaller in Latin "
                "America and the Middle East', 'head shake gestures mean no in Bulgaria'). If the claim is purely "
                "cognitive/psychological with no meaningful cross-cultural gesture variation, use an empty array [] "
                "or a single caveat if a mild one applies. Never invent; prefer well-documented examples. Keep all "
                "text English."
            ),
            "schema": {
                "note": "array of objects, one per asset below, same order",
                "each_object": {
                    "chapter_id": "string (copy from entry)",
                    "index": "int (copy from entry)",
                    "cultural_variations": ["array of 1-3 short strings, or []"]
                },
                "requirement": "include EVERY entry below exactly once in order; use [] where none apply"
            },
            "entries": chunk,
        }
        out = os.path.join(OUT, "phase7d_cv_%s_b%d.json" % (book_id, b + 1))
        with io.open(out, "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False, indent=1)
        print("wrote", os.path.basename(out), len(chunk), "entries")
