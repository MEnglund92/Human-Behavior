# -*- coding: utf-8 -*-
"""Insert the 16 Phase 7A deep dives into data/deep-dives.js, appending IN PLACE
into each existing topic's array (no duplicate top-level keys -> no shadowing)."""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BATCH = os.path.join(ROOT, "extract", "generated_assets", "phase7a", "dives")
DIVES_FILE = os.path.join(ROOT, "data", "deep-dives.js")

JOBS = [
    ("cognitive-biases", "kahneman_dive1_output.json"),
    ("cognitive-biases", "kahneman_dive2_output.json"),
    ("choice-architecture", "poh_dive1_output.json"),
    ("choice-architecture", "poh_dive2_output.json"),
    ("personality", "mindset_dive1_output.json"),
    ("personality", "mindset_dive2_output.json"),
    ("social-psych", "lucifer_dive1_output.json"),
    ("social-psych", "lucifer_dive2_output.json"),
    ("interpersonal-dynamics", "ei_dive1_output.json"),
    ("interpersonal-dynamics", "ei_dive2_output.json"),
    ("personality", "drive_dive1_output.json"),
    ("personality", "drive_dive2_output.json"),
    ("reading-people", "gof_dive1_output.json"),
    ("reading-people", "gof_dive2_output.json"),
    ("dark-triad", "dp_dive1_output.json"),
    ("dark-triad", "dp_dive2_output.json"),
]


def js_str(s):
    return json.dumps(s, ensure_ascii=True)


def block_for(d, dive_id):
    lines = ["    {"]
    lines.append("        id: %s," % js_str(dive_id))
    lines.append("        title: %s," % js_str(d["title"]))
    lines.append("        framework_description: %s," % js_str(d["framework_description"]))
    lines.append("        svg: %s," % js_str(d["svg"]))
    lines.append("        key_takeaways: [")
    for k in d["key_takeaways"]:
        lines.append("          %s," % js_str(k))
    lines.append("        ],")
    lines.append("        sections: [")
    for s in d["sections"]:
        lines.append("          { heading: %s, source: %s, body: %s }," % (js_str(s["heading"]), js_str(s["source"]), js_str(s["body"])))
    lines.append("        ],")
    lines.append("        sv: {")
    lines.append("          title: %s," % js_str(d["sv"]["title"]))
    lines.append("          framework_description: %s," % js_str(d["sv"]["framework_description"]))
    lines.append("          key_takeaways: [")
    for k in d["sv"]["key_takeaways"]:
        lines.append("            %s," % js_str(k))
    lines.append("          ],")
    lines.append("          sections: [")
    for s in d["sv"]["sections"]:
        lines.append("            { heading: %s, body: %s }," % (js_str(s["heading"]), js_str(s["body"])))
    lines.append("          ]")
    lines.append("        }")
    lines.append("    }")
    return lines


def find_array_block(src, key, start_search=0):
    """Return (start_of_array, end_of_array) for the FIRST occurrence of
    '<key>": [' at top level starting search from start_search."""
    pat = re.compile(r'\n  "%s": \[(.*?)\n  \],' % re.escape(key), re.S)
    m = pat.search(src, start_search)
    if not m:
        return None
    return m.start(1), m.end(1)


def main():
    with io.open(DIVES_FILE, encoding="utf-8") as f:
        src = f.read()

    per_topic = {}
    for topic_key, fname in JOBS:
        with io.open(os.path.join(BATCH, fname), encoding="utf-8") as f:
            d = json.load(f)
        dive_id = "phase7a-%s" % os.path.basename(fname).rsplit("_output.json", 1)[0]
        per_topic.setdefault(topic_key, []).append((dive_id, d))

    # Process topics; append in place for existing keys, add new top-level
    # keys for missing ones (choice-architecture, dark-triad).
    total = 0
    existing_keys = [m.group(1) for m in re.finditer(r'^\s{2}"([a-z\-]+)": \[', src, re.M)]
    new_blocks = []
    for topic_key, items in per_topic.items():
        blocks = []
        for dive_id, d in items:
            blocks.extend(block_for(d, dive_id))
            blocks.append(",")
        blocks = blocks[:-1]
        insertion = ",\n" + "\n".join(blocks)
        if topic_key in existing_keys:
            seg_start, seg_end = find_array_block(src, topic_key, 0)
            src = src[:seg_end] + insertion + src[seg_end:]
            print("appended", len(items), "dives to existing topic", topic_key)
        else:
            new_blocks.append('\n  "%s": [%s\n  ],' % (topic_key, insertion[1:]))
            print("adding NEW topic key", topic_key, "with", len(items), "dives")
        total += len(items)

    if new_blocks:
        src = src.rstrip()
        sep = src.rfind("};")
        head, tail = src[:sep], src[sep:]
        head = head.rstrip()
        if head.endswith(","):
            head = head[:-1].rstrip()
        src = head + "," + "\n" + "\n".join(new_blocks) + "\n" + tail + "\n"

    with io.open(DIVES_FILE, "w", encoding="utf-8") as f:
        f.write(src)
    print("TOTAL inserted:", total)


if __name__ == "__main__":
    main()