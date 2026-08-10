# -*- coding: utf-8 -*-
"""Merge the Phase 7A hybrid concept-map extension into data/concept-map.js."""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "extract", "generated_assets", "phase7a", "dives", "map_ext_output.json")
MAP = os.path.join(ROOT, "data", "concept-map.js")

with io.open(SRC, encoding="utf-8") as f:
    ext = json.load(f)

staged = map(json.dumps, ext["nodes"])
edges_block = ",\n".join(json.dumps(e) for e in ext["edges"])

with io.open(MAP, encoding="utf-8") as f:
    src = f.read()

# nodes: insert after the last node line inside nodes: [ ... ]
n_start = src.find("nodes: [") + len("nodes: [")
n_end = src.find("edges:")
nodes_inner = src[n_start:n_end]

# find the insertion point: after the last "], ... {" node line, before the closing "]"
# Locate the LAST '"id":' occurrence in the nodes block, then its closing brace.
last_id = nodes_inner.rfind('"id":')
line_start = nodes_inner.rfind("\n", 0, last_id)
line_end = nodes_inner.find("\n", last_id)
assert "}" in nodes_inner[line_start:line_end], "node line malformed"
# insert after the comment-safe end of that node object: find its closing brace
obj_end = nodes_inner.find('},', last_id)
if obj_end == -1:
    obj_end = nodes_inner.rfind('}')
insert_at = obj_end + 1

new_nodes_inner = nodes_inner[:insert_at] + ",\n" + ",\n".join(staged) + nodes_inner[insert_at:]
src = src[:n_start] + new_nodes_inner + src[n_end:]

# edges: insert before the closing '],' of the edges array (which has a trailing comma)
e_start = src.find("edges: [") + len("edges: [")
e_end = src.rfind("],")
edges_inner = src[e_start:e_end]
insert_at2 = edges_inner.rfind("\n")
new_edges_inner = edges_inner[:insert_at2] + ",\n" + edges_block + edges_inner[insert_at2:]
src = src[:e_start] + new_edges_inner + src[e_end:]

with io.open(MAP, "w", encoding="utf-8") as f:
    f.write(src)

print("merged", len(ext['nodes']), "nodes and", len(ext['edges']), "edges")