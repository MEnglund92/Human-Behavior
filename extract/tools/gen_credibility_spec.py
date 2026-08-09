# -*- coding: utf-8 -*-
"""Generate the credibility-profile authoring spec for the 25 asset libraries."""
import io
import json
import os
import glob

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_assets")

LIBRARIES = []
for path in sorted(glob.glob(os.path.join(OUT, "*_assets.json"))):
    name = os.path.basename(path)
    if name in ("truth_and_lies_assets.json", "power_body_language_assets.json") or "pages" in name:
        continue
    try:
        d = json.load(io.open(path, encoding="utf-8"))
    except Exception:
        continue
    title = d.get("source", "") if isinstance(d, dict) else ""
    chs = d.get("chapters", []) if isinstance(d, dict) else []
    n = sum(len(c.get("assets", [])) for c in chs)
    chaps = [c.get("title", "") for c in chs][:14]
    LIBRARIES.append({"book_id": name.replace("_assets.json", ""), "title": title, "assets": n, "chapters": chaps})

spec = {
    "job": "credibility_profiles",
    "task": (
        "Classify each book below by the scientific standing of the claims it makes, producing a per-library "
        "credibility profile. This feeds per-asset credibility labels shown to learners, so be honest and nuanced. "
        "For each book provide: level (High|Medium|Low), consensus (Broad|Emerging|Contested), and a 1-2 sentence "
        "note explaining the rating (e.g. 'peer-reviewed synthesis of controlled experiments' vs 'trade book with "
        "anecdotal evidence' vs 'popular claims contested by later research'). Do not rate the BOOK's quality; rate "
        "the scientific confidence a learner should attach to claims derived from it."
    ),
    "level_defs": {
        "High": "claims rest on replicated, peer-reviewed research (controlled studies, meta-analyses)",
        "Medium": "claims are evidence-based but with caveats: case studies, single studies, or expert synthesis",
        "Low": "claims are anecdotal, popularized, or contradicted by current research; treat as ideas, not findings"
    },
    "consensus_defs": {
        "Broad": "most researchers in the field would agree",
        "Emerging": "active research area with growing but not settled support",
        "Contested": "significant disagreement or claims at odds with mainstream science"
    },
    "schema": [
        {"book_id": "string (from the list)", "level": "High|Medium|Low", "consensus": "Broad|Emerging|Contested", "note": "string"}
    ],
    "libraries": LIBRARIES,
}

with io.open(os.path.join(OUT, "phase7d_credibility_spec.json"), "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print("wrote phase7d_credibility_spec.json with", len(LIBRARIES), "libraries")