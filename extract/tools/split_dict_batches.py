# -*- coding: utf-8 -*-
"""Phase 5: split the 312 dictionary entries into N batches for parallel
authoring agents. Each batch file: extract/generated_assets/dict_batch_XX.json
= list of {concept, definition}. Agents produce
extract/tools/dict_enrich_XX.json = {concept: {real_world_scenario,
case_study_cloze, sv: {concept, definition, real_world_scenario,
case_study_cloze}}}. merge_dict_enrich.py applies them."""
import json
import math
import os

BASE = r"extract/generated_assets/dictionary_entries_base.json"
BATCHES = 8
OUTDIR = r"extract/generated_assets"

entries = json.load(open(BASE, encoding="utf-8"))
n = math.ceil(len(entries) / BATCHES)
for i in range(BATCHES):
    chunk = entries[i * n:(i + 1) * n]
    if not chunk:
        continue
    p = os.path.join(OUTDIR, "dict_batch_%02d.json" % (i + 1))
    with open(p, "w", encoding="utf-8") as f:
        json.dump(chunk, f, ensure_ascii=False, indent=1)
    print("%s -> %d entries" % (p, len(chunk)))
print("total split:", sum(len(json.load(open(os.path.join(OUTDIR, "dict_batch_%02d.json" % (i + 1)), encoding="utf-8"))) for i in range(BATCHES)))
