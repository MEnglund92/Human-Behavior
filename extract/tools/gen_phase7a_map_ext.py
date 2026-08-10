# -*- coding: utf-8 -*-
"""Generate the Phase 7A hybrid concept-map extension spec.

The existing data/concept-map.js has 89 nodes across 20 topics. This extension
adds ~32 new nodes drawn from the 8 Phase 7A books, using ONLY concept names
that exist verbatim in the topics reference, and typed edges that link the new
nodes into the existing graph (at least one edge per new node, connecting to
existing node ids where possible)."""

import io
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated_assets", "phase7a", "dives")

spec = {
    "spec_file": "map_ext.json",
    "job": "concept_map_extension",
    "task": (
        "Extend an existing cross-book concept map for a behavioral-science study app. "
        "The current map (data\\concept-map.js) has 89 nodes and about 110 typed edges. "
        "Add exactly 32 NEW nodes representing the standout concepts of 8 newly added "
        "books, and typed edges linking them into the existing graph."
    ),
    "books_to_cover": {
        "kahneman": "cognitive-biases",
        "power_of_habit": "choice-architecture",
        "mindset": "personality",
        "lucifer_effect": "social-psych",
        "emotional_intelligence": "interpersonal-dynamics",
        "drive": "personality",
        "gift_of_fear": "reading-people",
        "dark_psychology": "dark-triad",
    },
    "steps": [
        "Read C:\\Users\\matti\\Desktop\\Education\\Human Behavior\\extract\\generated_assets\\phase7d_topics_ref.txt (all 20 topics, 750 concepts).",
        "Read C:\\Users\\matti\\Desktop\\Education\\Human Behavior\\data\\concept-map.js (existing nodes with ids, groups, topicIds, entries).",
        "Create exactly 32 new nodes, 4 per book (8 books). Each node MUST use an entry that exists VERBATIM in the topics reference file under the node's topicId. Prefer entries already used by the app for that book's domain; if a canonical book concept lacks a ref entry, use the closest existing ref entry from the book's topic binding instead.",
        "node.id: new kebab-slug unique vs existing ids; node.label: short display label; node.group: one of the 7 groups below; node.topicId: one of the 20 topic ids; node.entry: exact ref name (case-sensitive).",
        "Add edges: each new node gets 1-3 edges; at least half of all added edges must connect a new node to an EXISTING node id from the current map (read them from concept-map.js). Edge types: builds-on, contrasts-with, applies-to, foundation.",
        "Output ONLY the extension JSON below, no markdown."
    ],
    "groups": {
        "learning": {"label": "Learning & Habits", "color": "#38bdf8"},
        "cognition": {"label": "Cognition & Biases", "color": "#a78bfa"},
        "emotion": {"label": "Emotion", "color": "#f472b6"},
        "social": {"label": "Social Influence", "color": "#fbbf24"},
        "individual": {"label": "Self & Personality", "color": "#34d399"},
        "relationships": {"label": "Relationships", "color": "#fb7185"},
        "reading": {"label": "Reading Others", "color": "#4ade80"},
    },
    "edge_types": ["builds-on", "contrasts-with", "applies-to", "foundation"],
    "output_schema": {
        "nodes": [{"id": "kebab-slug", "label": "short label", "group": "one of the 7", "topicId": "topic id from ref", "entry": "exact concept name from ref"}],
        "edges": [{"from": "node id (new or existing)", "to": "node id (new or existing)", "type": "one of the 4"}]
    },
    "verification": [
        "Exactly 32 nodes, 4 per listed book.",
        "Every node.entry exists verbatim in the topics ref under node.topicId.",
        "Every edge from/to is a defined node id (new or existing).",
        "At least 16 edges connect a new node to an existing node id.",
        "No duplicate node ids; no edge duplicates.",
        "All node groups among the 7; all edge types among the 4."
    ],
}

with io.open(os.path.join(OUT, spec["spec_file"]), "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print("wrote", spec["spec_file"])