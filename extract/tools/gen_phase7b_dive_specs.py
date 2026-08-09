# -*- coding: utf-8 -*-
"""Generate authoring specs for the 3 Phase 7B deep dives."""
import io
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_assets", "phase7b")

COMMON = {
    "output_dir": os.path.abspath(OUT),
    "schema": {
        "title": "string, plain English title",
        "framework_description": "intro paragraph, then exactly 3 marked sections separated by \\n: \"\\n.1. Heading Here\\n...paragraph...\", \"\\n.2. ...\", \"\\n.3. ...\"",
        "key_takeaways": "array of exactly 4 English takeaways",
        "sections": "array of exactly 2 objects: { heading: str, source: str (format 'AuthorName, Initial. (Year)'), body: str (2-3 sentences) }",
        "svg": "single-line SVG string: only <rect> and <text> elements; viewBox=\"0 0 820 300\"; first element is <rect width=\"820\" height=\"300\" fill=\"#181825\" rx=\"10\" for the dark background; ends with </svg>",
        "sv": {
            "title": "natural Swedish title",
            "framework_description": "Swedish version with the same .\\n.1/.2/.3 structure",
            "key_takeaways": "exactly 4 Swedish takeaways",
            "sections": "exactly 2 objects: { heading, body } in Swedish, no source field"
        }
    },
    "quality_bar": [
        "psychologically accurate and measured; both languages natural, correct, zero typos",
        "no markdown, no backticks; no [] or {} characters inside any string value",
        "exactly the fields above and nothing more"
    ]
}

DIVES = [
    {
        "spec_file": "deepdive_ekman_barrett.json",
        "dive_topic_key": "emotion-expression",
        "content": "Paul Ekman's basic-emotion model (6-7 universal categories, cross-culturally recognized facial expressions) vs Lisa Feldman Barrett's constructed-emotion model (emotions are concepts the brain builds from core bodily feelings + context + culture). Cover: how each model reads the same evidence, key experiments (Ekman's Papua New Guinea photos; Barrett's re-analyses / machine-learning studies), the practical lesson for reading faces in real life (coarse signals are useful, exact labels need context), and what a balanced debate looks like. Neither side presented as definitively wrong.",
        "svg_hint": "Two side-by-side boxes with bg rect; left box: 'Ekman: Universal Emotions', bullets '6-7 basic emotions', 'Same face signals worldwide', 'Biologically hardwired'; right box: 'Barrett: Constructed Emotions', bullets 'Emotions are concepts', 'Context changes meaning', 'Culture shapes feelings'; title: 'Ekman vs. Barrett'.",
    },
    {
        "spec_file": "deep_dive_polyvagal.json",
        "dive_topic_key": "biological-bases",
        "content": "Stephen Porges' Polyvagal Theory for stress and regulation: the autonomic nervous system prioritizes responses via three evolutionarily layered branches — 1) ventral vagal (social engagement: calm, connected, safe — top of hierarchy), 2) sympathetic (fight/flight mobilization — middle), 3) dorsal vagal (freeze/shutdown — oldest, last resort). Explain the hierarchy of triaging (the brain reads safety via what Porges calls neuroception), what a re-triggered demotion through the states looks like in daily life, practical regulation implications (safety cues, vagal tone), and how this helps triage behavior in others.",
        "svg_hint": "Three horizontal boxes: green 'Ventral Vagal - Social Engagement: calm, connection', amber 'Sympathetic - Fight or Flight: mobilization', red 'Dorsal Vagal - Freeze/Shutdown: conservation'; title: 'The Polyvagal Hierarchy'.",
    },
    {
        "spec_file": "deep_dive_status.json",
        "dive_topic_key": "evolutionary-psych",
        "content": "Dominance and prestige as the two evolutionarily validated pathways to status, building on Henrich & Gil-White (2001) and Tracey's empirical work: dominance = rank won through coercion/fear (the oldest animal route), prestige = rank freely given for skill, wisdom, generosity (typical of human hierarchies). Contrast the two: compliance vs genuine esteem, anxiety vs stability of rank, costs. Ties into office hierarchies, public life, dating markets; end on practical signals (who gets looked at/deferred to) and the cost of confusing the two paths (despotic dominance vs humble prestige).",
        "svg_hint": "Two boxes: red 'Dominance: coercion, fear, obedience' vs green 'Prestige: skill, respect, freely given'; title 'Dominance vs. Prestige'.",
    },
]

for d in DIVES:
    s = dict(COMMON)
    s.update(d)
    with io.open(os.path.join(OUT, d["spec_file"]), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("wrote spec", d["spec_file"])