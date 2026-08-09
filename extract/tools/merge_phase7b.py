# -*- coding: utf-8 -*-
"""Merge Phase 7B authored batches into data/topics JS files, wiring data.js.

Reads:  extract/generated_assets/phase7b/{t19_b1,b2,b3, t20_a,b}_output.json
Writes: data/topics/topic-choice-architecture.js and topic-dark-triad.js,
        then patches data.js topics[] concat list.
"""
import io
import json
import os
import re

BATCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_assets", "phase7b")
DATA_TOPICS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "topics")
DATA_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data.js")

CATS19 = [
    {"id": "choice-architecture", "name": "Choice Architecture", "color": "#fde68a"},
    {"id": "habit-loops", "name": "Habit Loops", "color": "#86efac"},
    {"id": "friction-design", "name": "Friction & Design", "color": "#c4b5fd"},
]
CATS20 = [
    {"id": "manipulation-tactics", "name": "Manipulation Tactics", "color": "#fca5a5"},
    {"id": "toxic-dynamics", "name": "Toxic Dynamics", "color": "#f9a8d4"},
    {"id": "defenses", "name": "Defenses & Recovery", "color": "#93c5fd"},
]


def esc(s):
    return s.encode("unicode_escape").decode("ascii").replace("'", "\\'")


def entry_line(e):
    sv = e["sv"]
    rel = ", ".join('"%s"' % r.replace('"', "") for r in e["related_concepts"])
    return (
        "      { concept: \"%s\", definition: \"%s\", category: \"%s\", "
        "real_world_scenario: \"%s\", case_study_cloze: \"%s\", "
        "related_concepts: [%s], sv: { concept: \"%s\", definition: \"%s\", "
        "real_world_scenario: \"%s\", case_study_cloze: \"%s\" } },"
        % (
            esc(e["concept"]), esc(e["definition"]), esc(e["category"]),
            esc(e["real_world_scenario"]), esc(e["case_study_cloze"]),
            rel, esc(sv["concept"]), esc(sv["definition"]),
            esc(sv["real_world_scenario"]), esc(sv["case_study_cloze"]),
        )
    )


def build_topic_file(const_name, topic_id, title, cats, entries, out_path):
    lines = ["const %s = [" % const_name, ""]
    lines.append("  {")
    lines.append('    id: "%s",' % topic_id)
    lines.append('    name: "%s",' % esc(title))
    lines.append("    categories: [")
    for c in cats:
        lines.append('      { id: "%s", name: "%s", color: "%s" },' % (c["id"], c["name"], c["color"]))
    lines.append("    ],")
    lines.append("    entries: [")
    for e in entries:
        lines.append(entry_line(e))
    lines.append("    ]")
    lines.append("  }")
    lines.append("];")
    lines.append("")
    with io.open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", out_path, "with", len(entries), "entries")


def load_batches(paths):
    out = []
    for p in paths:
        with io.open(os.path.join(BATCH_DIR, p), encoding="utf-8") as f:
            out.extend(json.load(f))
    return out


def patch_data_js():
    with io.open(DATA_JS, encoding="utf-8") as f:
        src = f.read()
    for const_id in ("_t_choice_architecture", "_t_dark_triad"):
        if const_id in src:
            continue
        src = re.sub(r"(_t_body_language_extracted,\n)", r"\1  %s,\n" % const_id, src, count=1)
    with io.open(DATA_JS, "w", encoding="utf-8") as f:
        f.write(src)
    print("patched data.js")


if __name__ == "__main__":
    entries = load_batches(["t19_b1_output.json", "t19_b2_output.json", "t19_b3_output.json"])
    build_topic_file("_t_choice_architecture", "choice-architecture",
                     "19. Choice Architecture & Habit Mechanics", CATS19, entries,
                     os.path.join(DATA_TOPICS, "topic-choice-architecture.js"))
    entries = load_batches(["t20_a_output.json", "t20_b_output.json"])
    build_topic_file("_t_dark_triad", "dark-triad",
                     "20. Dark Triad & Covert Manipulation", CATS20, entries,
                     os.path.join(DATA_TOPICS, "topic-dark-triad.js"))
    patch_data_js()