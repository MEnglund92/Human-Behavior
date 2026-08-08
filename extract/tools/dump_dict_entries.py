# -*- coding: utf-8 -*-
"""Dump the 312 dictionary entries (concept+definition) to JSON for Phase 5
enrichment (real_world_scenario, case_study_cloze, sv)."""
import json
import re

SRC = r"data/topics/topic-body-language-extracted.js"
OUT = r"extract/generated_assets/dictionary_entries_base.json"

s = open(SRC, encoding="utf-8").read()
m = re.search(r"entries:\s*\[(.*?)\]\s*\}\s*\]\s*;", s, re.S)
body = m.group(1)
items = re.findall(r"\{([^{}]*)\}", body)
entries = []
for it in items:
    c = re.search(r"concept:\s*\"((?:[^\"\\]|\\.)*)\"", it)
    d = re.search(r"definition:\s*\"((?:[^\"\\]|\\.)*)\"", it)
    cat = re.search(r"category:\s*\"((?:[^\"\\]|\\.)*)\"", it)
    entries.append(
        {
            "concept": c.group(1) if c else "",
            "definition": d.group(1) if d else "",
            "category": cat.group(1) if cat else "",
        }
    )
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=1)
print("dumped %d entries -> %s" % (len(entries), OUT))
