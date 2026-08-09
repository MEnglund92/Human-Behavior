# -*- coding: utf-8 -*-
"""Write the concept-map authoring spec."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "generated_assets")

spec = {
    "job": "concept_map",
    "task": (
        "Author a curated cross-book concept map (graph) for a behavioral-science study app. The app already has "
        "750 concept entries organized into 20 topic modules. You will select ~85 of those entries and connect them "
        "with typed edges showing how concepts relate ACROSS modules."
    ),
    "steps": [
        "Read C:\\Users\\matti\\Desktop\\Education\\Human Behavior\\extract\\generated_assets\\phase7d_topics_ref.txt (all 20 topics, 750 concepts).",
        "Select ~85 concepts total, spread across ALL 20 topics (roughly 4-5 per topic; fewer for small topics). Choose concepts that genuinely form a connected web with cross-topic links (e.g., Social Proof links Cognitive Biases and Social Psychology; Attachment links Relationships and Personality; Self-Serving Bias links Cognitive Biases and Social Psychology; Operant Conditioning links Behavioral Psych and Habit/Choice Architecture; Mirror Neurons links Biological Bases and Emotion; Impression Management links Reading People and Social Psych...).",
        "Group the nodes into 7 thematic groups with the EXACT group ids, labels, and colors given below. Assign every node to exactly one group.",
        "Add edges between nodes. Every edge must reference valid node ids. Use 4 edge types: builds-on (concept builds on prior concept), contrasts-with (opposes/contrasts), applies-to (one concept is applied in the other's context), foundation (one concept is a foundational prerequisite). Aim for ~110 edges. Each node should have at least 1 edge; the graph should be connected (no isolated components).",
        "node.entry MUST be the EXACT English concept name as it appears in the reference file (case-sensitive, same punctuation) for the given topicId. The app resolves definitions by exact match, so typos break nodes. Choose node.entry from the SAME topic as node.topicId.",
        "node.id is a short kebab-slug you invent. node.label is a short display label (4-6 words max)."
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
        "CONCEPT_MAP": {
            "groups": "the 7 groups above exactly as given",
            "nodes": [{"id": "kebab-slug", "label": "short label", "group": "one of the 7", "topicId": "topic id from ref", "entry": "exact concept name from ref"}],
            "edges": [{"from": "node id", "to": "node id", "type": "one of the 4"}]
        }
    },
    "verification": [
        "Every node.topicId exists in the reference file.",
        "Every node.entry exists verbatim under that topic in the reference file.",
        "Every edge from/to is a defined node id.",
        "Graph is connected (ignoring direction).",
        "All node groups are among the 7; all edge types among the 4."
    ],
}

with io.open(os.path.join(OUT, "phase7d_conceptmap_spec.json"), "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print("wrote phase7d_conceptmap_spec.json")
