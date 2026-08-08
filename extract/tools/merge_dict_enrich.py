# -*- coding: utf-8 -*-
# Phase 5 merge: apply dict_enrich_*.json enrichments to
# data/topics/topic-body-language-extracted.js.
# Each entry gains: real_world_scenario, case_study_cloze,
# sv{concept, definition, real_world_scenario, case_study_cloze}.
# Written as JSON strings with \u escapes to match the existing style.
import glob
import json
import re
import sys

SRC = r"data/topics/topic-body-language-extracted.js"

enrich = {}
for p in sorted(glob.glob(r"extract/tools/dict_enrich_*.json")):
    d = json.load(open(p, encoding="utf-8"))
    for k, v in d.items():
        enrich[k] = v
print("enrichment concepts:", len(enrich))

s = open(SRC, encoding="utf-8").read()
m = re.search(r"(entries:\s*\[)(.*?)(\]\s*\}\s*\]\s*;)", s, re.S)
if not m:
    sys.exit("entries block not found")
head, body, tail = m.group(1), m.group(2), m.group(3)


def jstr(x):
    return json.dumps(x, ensure_ascii=True)


items = re.findall(r"\{([^{}]*)\}", body)
out_lines = []
count = 0
for it in items:
    c = re.search(r"concept:\s*\"((?:[^\"\\]|\\.)*)\"", it)
    d = re.search(r"definition:\s*\"((?:[^\"\\]|\\.)*)\"", it)
    cat = re.search(r"category:\s*\"((?:[^\"\\]|\\.)*)\"", it)
    concept = c.group(1) if c else ""
    definition = d.group(1) if d else ""
    category = cat.group(1) if cat else ""
    line = '      { concept: ' + jstr(concept) + ', definition: ' + jstr(definition) + ', category: ' + jstr(category)
    if concept in enrich:
        e = enrich[concept]
        line += ', real_world_scenario: ' + jstr(e["real_world_scenario"])
        line += ', case_study_cloze: ' + jstr(e["case_study_cloze"])
        sv = e["sv"]
        line += ', sv: { concept: ' + jstr(sv.get("concept", ""))
        line += ', definition: ' + jstr(sv.get("definition", ""))
        line += ', real_world_scenario: ' + jstr(sv.get("real_world_scenario", ""))
        line += ', case_study_cloze: ' + jstr(sv.get("case_study_cloze", "")) + ' }'
        count += 1
    line += " },"
    out_lines.append(line)

missing = len(items) - count
new_body = "\n".join(out_lines)
new_s = s[: m.start(2)] + new_body + s[m.end(2):]
open(SRC, "w", encoding="utf-8", newline="").write(new_s)
print("entries:", len(items), "| enriched:", count, "| missing:", missing)
