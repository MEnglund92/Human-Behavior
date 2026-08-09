# -*- coding: utf-8 -*-
"""Insert the 3 Phase 7B deep dives into data/deep-dives.js."""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BATCH = os.path.join(ROOT, "extract", "generated_assets", "phase7b")
DIVES_FILE = os.path.join(ROOT, "data", "deep-dives.js")

JOBS = [
    ("emotion-expression", "dive1_output.json"),
    ("biological-bases", "dive2_output.json"),
    ("evolutionary-psych", "dive3_output.json"),
]


def js_str(s):
    return json.dumps(s, ensure_ascii=True)


def block_for(d):
    lines = ["      {"]
    lines.append("        id: %s," % js_str(d["id"]))
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
    lines.append("      }")
    return lines


def main():
    with io.open(DIVES_FILE, encoding="utf-8") as f:
        src = f.read()
    src = src.rstrip()
    assert src.endswith("};"), "file does not end with };"
    sep = src.rfind("};")
    head, tail = src[:sep], src[sep:]

    inserts = []
    for topic_key, fname in JOBS:
        with io.open(os.path.join(BATCH, fname), encoding="utf-8") as f:
            d = json.load(f)
        d["id"] = "phase7b-%s" % topic_key
        lines = block_for(d)
        inserts.append("\n  %s: [\n%s\n  ]," % (js_str(topic_key), "\n".join(lines)))

    new_src = head.rstrip() + "," + "\n" + "\n".join(inserts) + "\n" + tail + "\n"
    with io.open(DIVES_FILE, "w", encoding="utf-8") as f:
        f.write(new_src)
    print("inserted", len(JOBS), "dives")


if __name__ == "__main__":
    main()