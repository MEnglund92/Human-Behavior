# -*- coding: utf-8 -*-
"""Dump all topics + entry concept names (English) to a reference file for the concept-map authoring agent."""
import io
import os
import re
import glob

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "topics")
ref = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_assets", "phase7d_topics_ref.txt"), "w", encoding="utf-8")
for path in sorted(glob.glob(os.path.join(OUT, "topic-*.js"))):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"const (_t_\w+) = (\[.*)$", src, re.S)
    if not m:
        ref.write(path + ": PARSE FAIL\n")
        continue
    name = m.group(1)
    arr_src = m.group(2).rstrip().rstrip(";")
    ns = {}
    try:
        exec(arr_src, ns)
        data = ns["data"] if "data" in ns else ns[name]
    except Exception as e:
        ref.write(path + ": EVAL FAIL " + str(e) + "\n")
        continue
    ref.write("\n### " + os.path.basename(path) + " (" + name + ")\n")
    for t in data:
        ref.write("\n-- topic id=" + t["id"] + " name=" + t["name"] + "\n")
        for e in t["entries"]:
            ref.write("  * " + e["concept"] + "\n")
ref.close()
print("wrote phase7d_topics_ref.txt")
