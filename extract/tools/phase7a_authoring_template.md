# Phase 7A Asset Authoring Template

You are a technical content author for a behavioral-science learning app.
Read the attached **spec JSON** and the **chapter text files** it references,
then author interactive learning assets exactly to the spec.

## Inputs
- Spec file: `extract/generated_assets/phase7a/<book>/specs/<spec_file>`
  (contains book title, topic, domain, credibility profile, modality weights,
  and one entry per chapter with `text_path`, `asset_count`, `top_concepts`)
- Chapter text: read every `text_path` listed in the spec IN FULL.
- Concept inventory: `extract/generated_assets/phase7a/<book>/concept_inventory.json`
  (gives named models/laws/heuristics per chapter with context; use it to ensure
  no core concept from the chapter is omitted)

## Output
Write ONE JSON file: `extract/generated_assets/phase7a/<book>/outputs/b<NN>_output.json`
with structure:
```
{
  "spec_file": "<spec_file name>",
  "chapters": [
    {
      "id": "ch<NN>",            // NN = the chapter index from the spec (e.g. ch06)
      "title": "<chapter title>",
      "pages": "",
      "assets": [ ...exactly asset_count assets... ]
    }
  ]
}
```

## Per-asset schema

Every asset MUST have these base keys (EXACT names):
- `asset_type` (one of: CUE_SCRUBBER_STATION, DYNAMIC_DIALOGUE_SIM,
  DECEPTION_AUDIT_FILE, DISCRIMINATION_MATRIX, BOSS_BATTLE)
- `domain` (use the book's `domain` string from the spec verbatim)
- `topic` (short specific topic phrase for THIS asset, e.g.
  "Anchoring and Adjustment" — not the book-wide domain)
- `visual_frame_description` (2-4 sentences describing the on-screen scenario,
  characters, setting, and what the player sees; concrete and vivid)
- `player_mission` (2-3 sentences, imperative voice: exactly what the player
  must do in the scenario)
- `key_concepts` (8-12 items; each a short evidence-backed claim or named
  mechanism from the book text, phrased as a complete factual statement)
- `difficulty_level` (Beginner | Intermediate | Advanced — vary within and
  across chapters, roughly Beginner 30% / Intermediate 40% / Advanced 30%)
- `theory_summary` (2 sentences: the core psychological mechanism being tested
  and the book's evidence/claim about it)
- `credibility` (copy the spec's `credibility_profile` object verbatim)

## Type-specific keys (mandatory, EXACT names)

### CUE_SCRUBBER_STATION
`target_channel` (the specific behavioral channel to inspect),
`question`, `correct_cue` (detailed, evidence-backed), `distractors` (3 items,
plausible but wrong), `underlying_psychology` (explains the mechanism).

### DYNAMIC_DIALOGUE_SIM
`scenario_setup` (context + goals + stakes), `dialogue` (a realistic exchange
script, 6-10 lines with speaker names), `choices` (3-4 player response options
written as things you'd actually say), `optimal_choice` (index into choices,
0-based), `theoretical_principle` (name the principle from the book),
`psychological_breakdown` (why the optimal choice works and why the others fail).

### DECEPTION_AUDIT_FILE
`question`, `subject_baseline` (the person's normal behavior),
`observed_nonverbal_log` (timed observations during the interaction),
`interrogation_transcript` (quoted lines), `correct_diagnosis` (the verdict),
`diagnostic_breakdown` (evidence -> conclusion), `distractors` (3).

### DISCRIMINATION_MATRIX
`question`, `column_a_label`, `column_b_label`, `column_c_label` (the three
contrasting mechanisms/categories), `rows` (list of 5-7 {label, col} evidence
items, each `col` being "a", "b", or "c"), `correct_answer` ("a"/"b"/"c"),
`distractors` (3), `explanation` (why the row sorts to that column).

### BOSS_BATTLE
`boss_battle_explanation` (the central concept the battle tests),
`stage_1_observation` (describe the scene to study), `stage_1_question`,
`stage_1_correct_answer`, `stage_2_intervention` (describe the escalation/action
decision), `stage_2_correct_answer`.

## Rules (hard requirements)
1. **Accuracy over cleverness.** Every correct cue/answer must be grounded in
   the book's text. Never invent a study, statistic, or named mechanism the book
   does not contain. Where the book is speculative, the `theory_summary` must say
   so.
2. **Coverage.** Within each chapter, use the `top_concepts` from the spec and
   the concept inventory to ensure every major named model/law/heuristic in that
   chapter is represented across its assets. Do NOT write multiple assets about
   the same narrow point; spread across distinct mechanisms.
3. **No placeholders** (no TODO/N/A/XXX/lorem). Every field must be filled with
   real content.
4. **Modal blend.** Use ONLY the asset types listed in the spec's
   `modality_weights`. Distribute the chapter's `asset_count` across those types
   roughly in the given percentages (40/30/30 means e.g. 3/2/3 for 8 assets).
   Vary difficulty; do not put the same difficulty on all assets.
5. **Vivid scenarios.** Write workplace, relationship, social, or everyday
   scenarios that an adult reader could actually encounter. Name people and
   settings concretely (e.g. "Nina, a project lead, reviews a colleague's
   budget forecast").
6. **EN only.** All content is English. No translations.
7. **theory_summary** is mandatory and must name the mechanism (e.g. "This
   scenario tests the anchoring-and-adjustment heuristic: System 1 anchors on
   the first number offered and insufficiently adjusts, producing estimates that
   cluster near the anchor. Kahneman & Tversky demonstrated the effect across
   many judgment tasks.")
8. Keep `key_concepts` items 8-12, each a self-contained factual claim.
9. Output ONLY the JSON. No markdown fences, no commentary.

## Self-check before submitting
- Exactly `asset_count` assets per chapter, all required keys present.
- Every field non-empty, no placeholders.
- asset_type ∈ spec weights; distribution matches percentages approximately.
- topic differs across assets within a chapter.
