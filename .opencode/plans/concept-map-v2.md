# Concept Map v2 — "Explore · Connect · Understand"

Goal: make the 🕸️ Concept Map (121 nodes / 180 edges / 7 groups, `data/concept-map.js`)
look professional and actually teach how human-behavior concepts connect.
All work in `index.html` (`renderConceptMap` ~line 104k region) + small `initQuiz`
topic filter + `sw.js` bump + SV keys. No changes to `data/concept-map.js`.

## 1. Visual overhaul (rewrite renderConceptMap)
- Keep radial layout but add per-group translucent **sector halos** (large soft ellipses
  behind each group's nodes, group color at ~12% opacity) so the 7 clusters read at a glance.
- Nodes: r=13-15, group-color fill, 2px white stroke, hover ring.
- Labels: 10.5-11px on semi-transparent rounded chips, pointer-events none.
- Layout clamp: after computing positions, scale/translate into 1000x720 with 40px padding
  (fixes current bottom-edge clipping where y can reach ~983).
- Edges: curved bezier paths, 1.4px, arrowhead SVG markers, slight arc bend; hover tooltip
  already exists via <title> - keep, ensure type text localized.
- Background: subtle radial gradient + faint dot grid; svg rounded corners already styled.
- One compact legend bar (7 group dots + 4 edge-type colors + counts) above the map.

## 2. Interaction
- Pan & zoom: mousedown/mousemove/mouseup drag on empty svg (cursor grab/grabbing),
  wheel zoom (0.1 steps, clamp 0.4x-2.5x), dbl-click resets. Implement via <g id="mapWorld">
  transform translate/scale. Mouse coords converted via getBoundingClientRect.
- Hover: node mouseenter -> highlight node + direct neighbors + incident edges,
  dim everything else to 0.25; mouseleave restores.
- Search input above map ("Search concepts..." / SV): case-insensitive substring on
  label+entry; matches get accent ring; non-matches dim 0.15; Enter or first match
  auto-pans/zooms to center it.
- Filter chips: "All" + 7 groups + topics (18-19). Clicking shows only that cluster's
  nodes (visibility toggle; edges pruned to visible pairs; halo of filtered group
  highlighted, others faded). Counter line: "121 concepts · 180 links · n shown".
- Detail card (existing) upgraded: definition + relations (keep) + buttons:
  - Study this concept (existing -> browse filtered)
  - Open Deep Dive (new) - if node.topicId has _deepDives entries -> switchTab('deep')
    and set deep filter to that topic
  - Test yourself (new) - switchTab('quiz') + initQuiz({topic: node.topicId}) filter
    (small initQuiz topic-filter addition)
  - Jump-to-neighbor links (existing data-jump behavior kept)

## 3. Guided Tour (teaching mode)
- Button "▶ Guided Tour" (SV) next to search/filters.
- Starts at node "behavior" (or clicked node when opened from a node card).
- BFS over edges with priority foundation > builds-on > applies-to, max 7 stops,
  max 2 hops from start; prefers contrasts-with as final stop to sharpen distinctions.
- Tour bar (below map): "2/7 · Label — definition (short)" + "why it matters" line
  generated from edge types (e.g., "Classical Conditioning builds on Stimulus→Response:
  learning happens through association") + Back/Next/End.
- Map highlights current node (accent ring) + traversed path edges thicker.
- Clicking any node during tour re-routes path from that node.
- No new authored copy needed - text derived from existing entries + edge types.

## 4. SV keys (add to svUI)
Search concepts, Guided Tour, End tour, Back, Next, Test yourself, Open Deep Dive,
Reset view, concepts, links, shown, Why it matters, + any new labels.

## 5. Verification & deploy
- Re-extract inline JS + node --check (both index.html and full extraction).
- Local CDP e2e probe: map renders (halo count 7, node count 121), hover highlight,
  search filters, group filter, pan/zoom events attached, tour advances 7 steps and
  ends, deep-dive jump lands on deep tab, quiz jump lands with topic filter,
  0 runtime exceptions; SV toggle spot-check.
- validate.py untouched (no asset changes).
- sw.js v31 -> v32. Commit, push origin main:master + main, live CDP spot-check.

## Files
- index.html (renderConceptMap region ~104.6k-109.7k, svUI, initQuiz, tab-map HTML)
- sw.js (v32)
- No changes: data/concept-map.js, extract/*, assets/*
