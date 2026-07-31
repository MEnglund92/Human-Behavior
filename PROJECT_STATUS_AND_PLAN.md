# Human Behavior Project — Progress & Continuation Plan

> Purpose: This document is a complete handoff so work can continue from another
> computer. It records what was built, where everything lives, the data schema,
> the generation workflow, validation results, and exactly what remains to do.
>
> Last updated: 2026-07-31

---

## 1. Project Overview

**Goal:** Build a gamified behavioral-science asset library. Each asset turns
real book content (body language, deception detection, emotions, persuasion,
evolutionary psychology) into an interactive training game. The user demanded
**100% extraction** — every concept/topic in every chapter must become playable
content, even if it takes many sessions. A flat 230-asset coverage pass was
explicitly rejected as insufficient; depth per book is the priority.

**Deliverable format:** JSON files in `extract\generated_assets\`, one file per
book, all sharing one schema (Section 4). They feed a game (PWA frontend,
`data.js` at repo root) that renders 5 asset types as interactive challenges.

---

## 2. Machine / Environment Facts

- Workspace root: `C:\Users\Matt\Desktop\Education\Human Behavior`
- OS: Windows, PowerShell 5.1 (commands in this doc are PowerShell)
- Git repo: yes (branch default), only `data.js` and a few commits; `extract/`
  is currently **untracked** (`git status` shows `?? extract/`) — commit or copy
  it before moving machines.
- Temp work dir used by the AI sessions: `C:\Users\Matt\AppData\Local\Temp\opencode\`
  (NOT part of the repo — PDFs were copied there as `glass.pdf`, `reiman.pdf`,
  `bowden.pdf` and text-extracted to `glass.txt`, `reiman.txt`, `bowden.txt`,
  along with generator scripts `gen_*.py` and `validate.py`). These are NOT
  required on the new machine if PDFs can be re-extracted there, but they are
  handy. The JSON outputs they produced ARE the durable artifacts.
- Python is available (generators are plain stdlib `json` scripts; PDF text
  extraction used `pdftotext`-style tooling already on the machine — the text
  files are the extraction results and were written to %TEMP%).

---

## 3. Book Inventory & Priority

### Priority books (full deep extraction — done or in progress)

| # | Book | Author | Status | Assets |
|---|------|--------|--------|--------|
| 1 | Workbook of Attached (adult attachment) | Levine & Heller | DONE | 45 |
| 2 | The Definitive Book of Body Language | Pease & Pease | DONE | 100 |
| 3 | What Every BODY Is Saying | Navarro | DONE | 50 |
| 4 | Emotions Revealed | Ekman | DONE (deep pass) | 135 |
| 5 | Telling Lies | Ekman | DONE (deep pass) | 65 |
| 6 | The Dictionary of Body Language | Navarro | DONE (deep pass) | 75 |
| 7 | **The Body Language of Liars** | Lillian Glass | **DONE (Phase 1 new)** | 60 |
| 8 | **The Power of Body Language** | Tonya Reiman | **DONE (Phase 1 new)** | 60 |
| 9 | **Truth & Lies** | Bowden & Thomson | **DONE (Phase 1 new)** | 70 |

**Running total: 660 assets, all validated (see Section 6).**

### Marked `(Not)` / skip — do NOT generate assets for these
- Body Language (Allan Pease)
- Nonverbal Communication (general textbook)
- Self-Presentation (Leary)
- Snoop: What Your Stuff Says About You (Gosling)
- SAOL (Swedish dictionary — "skip SAOL for now")

### Other books with assets in generated_assets (from earlier/other tracks)
Not part of the 660 total above: Behave (31), Influence (51), Laws of Human
Nature (23), Man's Search for Meaning (10), Mistakes Were Made (36), Moral
Animal (30), Predictably Irrational (22), Righteous Mind (39), Social Animal
(47), Social Intelligence (22), Truth & Lies (65) — NOTE: there are TWO files
with similar names: `truth_and_lies_assets.json` (65, older/different) and
`bowden_truth_lies_assets.json` (70, the new Bowden Phase-1 deliverable). The
Bowden one is the Phase-1 canonical output. `apa_nonverbal_assets.json` and
`research_methods_assets.json` contain 0 assets (placeholders).

---

## 4. Asset Schema (single canonical format — ALL files use this)

Top level:
```json
{
  "source": "<Book Title> - <Author>",
  "chapters": [
    {
      "id": "<book-prefix><nn>",      // e.g. "gl01", "re02", "bo01"
      "title": "<chapter or part title>",
      "pages": "<page range as string>",
      "assets": [ ...asset objects... ]
    }
  ]
}
```

Each asset object:
```json
{
  "asset_type": "CUE_SCRUBBER_STATION | DYNAMIC_DIALOGUE_SIM | DECEPTION_AUDIT_FILE | DISCRIMINATION_MATRIX | BOSS_BATTLE",
  "domain": "Body Language | Deception Detection | Nonverbal Communication | Critical Thinking ...",
  "topic": "Human-readable topic name",
  "visual_frame_description": "Scene/wireframe description for the game UI",
  "player_mission": "What the player must do (the actual game task)",
  "key_concepts": ["Array of 8-12 short concept strings distilled from the book"],
  "difficulty_level": "Beginner | Intermediate | Advanced"
}
```

### The 5 asset types (the game mechanics)
1. **CUE_SCRUBBER_STATION** — identify/classify cues from video-style clips; reference/lexicon drills. (Glass files may use the alias `BEHAVIORAL_BOSS_BATTLE` for boss battles — treated as valid.)
2. **DYNAMIC_DIALOGUE_SIM** — roleplay/dialogue where you read cues in real time and choose responses.
3. **DECEPTION_AUDIT_FILE** — case-file review: analyze logs, dossiers, patterns, field data.
4. **DISCRIMINATION_MATRIX** — grid tasks: map cues × contexts × interpretations; reliability ratings.
5. **BOSS_BATTLE** — timed high-stakes scenario that combines multiple concepts (named `BEHAVIORAL_BOSS_BATTLE` in glass_liars_assets.json).

Rule of thumb: **5 assets per sub-section** (one of each type), sub-sections
cover every chapter's topics. Generator scripts construct them programmatically
with a small `asset()` helper (see Section 7).

---

## 5. Per-Book Structure of the Phase-1 Deliverables (most recent work)

### glass_liars_assets.json — "The Body Language of Liars" (Lillian Glass) — 60 assets / 12 sub-sections
Lie types & morality, betrayal trauma, developmental lying, the 7 motives,
cyber/online deception, instincts & baseline, body tells, facial tells, vocal
tells, speech content, relationship/cheating tells, psychopath/sociopath profile.

### reiman_power_body_language_assets.json — "The Power of Body Language" (Tonya Reiman) — 60 assets / 9 chapters
Ch1 Power Behind BL (Five Immutable Truths, origins, mirror neurons), Ch2
Language of the Face (7 universal emotions, eyes/eyebrows, smiles/scowls/
lips/nose/chin), Ch3 Language of the Body (head/torso, arms/hands), Ch4 Space &
Touch (4 zones, 14 social touches), Ch5 Language of Sound (paralanguage), Ch6
First Impressions (3-stage model, 17 turn-offs), Ch7 Reading Signals (norming,
10 signal clusters), Ch8 Sending Signals (WIIFM, anchoring), Ch9 Reiman Rapport
Method (10-step system).

### bowden_truth_lies_assets.json — "Truth & Lies" (Bowden & Thomson) — 255 assets / 41 chapter entries (4 parts + 37 chapters) / Phase 2 COMPLETE
Core philosophy: body language is NOT a fixed code; all behavior is a display
of/response to power; the **SCAN process** (Suspend judgment → Context → Ask
"What else?" → New judgment & test). Part One Genuine Deceptions (Ch1-4), Part
Two Dating (Ch5-16: attraction, hard-to-get, ghosting, jealousy, breakup),
Part Three Friends & Family (Ch17-27: friendship, FOMO, control freaks,
exclusion, invisibility), Part Four Working Life (Ch28-37: interviews, big
dogs, conflict, meetings, teams, leadership, workplace theft) + Bonus Bluff
(poker tells).

Phase 2 (2026-07-31): added chapter-level entries `ch01`-`ch37`, one per book
chapter, each with 5 assets (one per type: CUE_SCRUBBER_STATION Beginner,
DYNAMIC_DIALOGUE_SIM Intermediate, DECEPTION_AUDIT_FILE Intermediate,
DISCRIMINATION_MATRIX Advanced, BOSS_BATTLE Advanced). Chapter-specific topics
covered include: the language myth (Ch1), power sources/chin jut (Ch2), 50/50
judgment accuracy (Ch3), Paul Nadeau interrogation + shoelace case (Ch4),
8-repetition eye targeting (Ch5), allotropic signals + μ-opioid rejection pain
(Ch6), pupillary contagion (Ch7), Hall's proxemics (Ch8), Hare checklist (Ch9),
Goodall/Darwin power (Ch10), FACS + misquoted 7-38-55 (Ch11), contempt
research (Ch12/16), Ekman clusters + Othello error (Ch13/37), pupil-dilation
gaze research (Ch14), online profile deception research (Ch15), Gambetta's
trust codes (Ch17), charisma measurement (Ch18), Napoleon/Leonardo poses +
selfie power poses (Ch19), Hertenstein touch emotions + Karpman triangle (Ch20),
Suvilehto touch topography (Ch21), Birdwhistell kinesics (Ch22), drama vs.
emergency (Ch23), attention-span research (Ch24), NLP eye-accessing debunked
(Ch25), teen eye-rolling research + Gottman (Ch26), power-posing debate (Ch27),
handshake chemosignaling (Ch28), emoji research (Ch29), static vs. dynamic face
cues (Ch30), smiling-in-pain (Ch31), empathy imbalance + yawn contagion (Ch32),
red-color anger research + IED (Ch33), ethology + dog yawns + emoticons (Ch34),
NBA tactile cooperation (Ch35), protean pointing (Ch36), guilt vs. shame +
Dobby effect + burden of proof + Hartley interrogation (Ch37).

---

## 6. Validation Status (as of 2026-07-31)

Every generator output is run through a validator that:
- parses the JSON
- counts assets
- checks every asset_type is in the allowed set
  `{CUE_SCRUBBER_STATION, DYNAMIC_DIALOGUE_SIM, DECEPTION_AUDIT_FILE, DISCRIMINATION_MATRIX, BOSS_BATTLE, BEHAVIORAL_BOSS_BATTLE}`

Latest run results (2026-07-31, after Phase 2 Bowden):
- bowden_truth_lies_assets.json — 255 assets, ALL VALID (50 warnings = only
  the known part-level duplicate-asset_type artifacts in bo01-bo04)
- glass_liars_assets.json — 60 assets, ALL VALID
- reiman_power_body_language_assets.json — 60 assets, ALL VALID

Also valid (earlier passes): attached_workbook (45), definitive_body_language
(100), what_every_body (50), emotions_revealed (135), telling_lies (65),
dictionary_body_language (75), truth_and_lies (65), influence (51),
social_animal (47), behave (31), moral_animal (30), righteous_mind (39),
predictably_irrational (22), social_intelligence (22), laws_human_nature (23),
mistakes (36), mans_search_meaning (10), power_body_language (50).
**Grand total: 1271 assets, ALL VALID** (except the two known placeholder
files `apa_nonverbal_assets.json` and `research_methods_assets.json`, which
are not JSON objects and have 0 assets - intentionally left alone).

Known quirk: the Reiman/Bowden generators originally emitted assets wrapped in
a redundant list `[[asset]]`; the emitted JSON files were fixed by unwrapping
(asset = asset[0] when len==1). New generators should build flat lists directly
and re-run the validator after generation.

---

## 7. Generation Workflow (how assets were produced)

1. **Extract text** — copy source PDF to `%TEMP%\opencode\<shortname>.pdf`,
   run a PDF→text tool (pdftotext style) producing `<shortname>.txt` in the
   same temp dir. (E.g. glass.txt 239pp/320K chars, reiman.txt 360pp/581K,
   bowden.txt 216pp/512K.)
2. **Map structure** — read the TOC + chapter headings from the .txt to define
   sub-sections (the explore agent was used for this; may be done inline).
3. **Write generator** — a standalone Python file in `%TEMP%\opencode\gen_<book>.py`
   with a small `asset(type, topic, visual, mission, concepts, diff)` helper and
   a `chapter(id, title, pages, assets)` helper; writes directly to
   `extract\generated_assets\<book>_assets.json`.
4. **Run** — `python "%TEMP%\opencode\gen_<book>.py"`.
5. **Validate** — `python "%TEMP%\opencode\validate.py"` (update its file list
   if validating other books).
6. **Report totals** — 5 assets per sub-section; update running total (was
   470 pre-Phase-1; now 660).

IMPORTANT CONVENTIONS:
- domain strings like `"Body Language | Deception Detection"`.
- Always 5 distinct asset types per sub-section (avoid duplicating a type
  within one sub-section).
- key_concepts must be substantive book content, not generic filler.
- Difficulty levels: Beginner / Intermediate / Advanced (mix them).

---

## 8. Phase 2 (STARTED 2026-07-31 — Bowden complete)

The user explicitly stated that after Phase 1 extraction, **Phase 2** will be
activated, which demands an EVEN DEEPER re-read/re-extraction of the books
(some phrases used: "even deeper re-extraction", content was previously deemed
insufficient at 230 assets). Plan for Phase 2:
- Re-open each book's `.txt` (re-extract PDFs if moving machines — sources in
  `Sources\Kroppsspråk & Icke-verbal kommunikation\` and
  `Sources\Beteendepsykologi, Socialpsykologi & Mänsklig Natur\`)
- Go section by section again, find topics NOT yet represented in the existing
  JSON (compare key_concepts coverage against the chapter text)
- Generate supplemental assets (new sub-sections / additional assets per
  sub-section) and merge into the existing JSON files (or add new files, then
  update the frontend data source)
- Re-validate everything; report the new totals
- The user may also want the 3 non-Priority books un-marked later — do not
  generate for them unless asked.

### Phase 2 progress

- **Bowden (Truth & Lies) — DONE 2026-07-31.** 70 → 255 assets. Book fully
  re-read from `bowden.txt` (7634 lines / 216 pp); chapter start pages mapped
  from `--- PAGE n ---` markers; per-chapter entries `ch01`-`ch37` added with
  one asset of each type per chapter. Existing part entries bo01-bo04 kept.
  Generator lives in-repo: `extract\tools\gen_bowden_p2.py` + chapter data
  `extract\tools\bowden_p2_data_{a..f}.py`. Re-run with
  `python extract/tools/gen_bowden_p2.py` (idempotent - skips existing ids).
- **Next book (not started): The Body Language of Liars (Glass)** — follow the
  same recipe: read TOC, map chapter start pages from the txt, author data
  files, run generator, validate, update this doc.

---

## 8b. Phase 3 (STARTED 2026-07-31 — frontend integration, COMPLETE)

Goal: expose all extracted assets in the PWA instead of leaving them as JSON.

1. **data.js split (done)** — the monolithic `data.js` (18 topics, deepDives,
   resources) is split into `data/topics/topic-<id>.js` + `data/deep-dives.js`
   + `data/resources.js`; `data.js` is now a small aggregator. The monolith is
   preserved as `data-full.js` (regenerate: `python extract\tools\split_data_js.py`).
   - **Bug found & fixed**: `data.js` had a stray `},` after the
     existential-humanistic topic (line 606) that made the whole file invalid
     JS (`node --check` failed); the app could not load. Fixed in `data-full.js`;
     splitter now also preserves the monolith so runs are repeatable.
2. **Scenario Lab tab (done)** — new 🧪 tab with 21 scenario libraries (1,207
   assets) from `extract\generated_assets\*.json` (all books incl. secondary,
   minus retired legacy files):
   - Selectors: library (21 books), chapter, mode (5 asset types), difficulty
     (Beginner/Intermediate/Advanced), session size (5/10/20/All)
   - Flow per asset: briefing (visual frame + mission, plus type-specific
     dossier: dialogue / case file / matrix / subject baseline) → verification
     (auto-graded multiple choice when the asset has question/choices/distractors;
     otherwise reveal insights + self-grade Got it / Missed it) → insights panel
     (key concepts + correct cue/diagnosis/breakdown)
   - Results: session score overlay + confetti (≥70%); every graded asset is
     written into the SM-2 SRS store (`lab:<book>: <topic>`) so the sidebar
     "Needs Review" and Dashboard pick it up
   - UI chrome bilingual (existing EN/SV toggle); asset content stays English
   - `assets.js` + `assets/assetlib-<book>.js` generated by
     `python extract\tools\build_frontend_assets.py` (re-runnable; skips legacy)
3. **Retired legacy duplicates (done)** — `truth_and_lies_assets.json` (65) and
   `power_body_language_assets.json` (50) moved to
   `extract\generated_assets\legacy\`; canonical sources are
   `bowden_truth_lies_assets.json` (255) and `reiman_power_body_language_assets.json` (60).
4. **Service worker (done)** — cache bumped to v7; FILES now lists all
   `data/` and `assets/` files.
5. **Docs (done)** — README + this doc updated.

### Phase 3 verification status (2026-07-31)
- All 22 data files, 22 asset files, sw.js, and the inline app script pass
  `node --check`
- Full-chain test (exact index.html script order): `topics`=18, `deepDives`=17,
  `resources`=5, `ASSET_LIBS`=21, 1,207 assets
- All 1,207 assets have asset_type + topic + difficulty_level; filters
  (book/chapter/mode/difficulty) verified in node
- `python server.py` → every URL (index.html, data.js, data/*, assets/*, sw.js,
  manifest.json) returns 200
- NOTE: no automated browser test — do a manual pass on localhost:8765
  (Scenario Lab: pick a book, run a session in each mode; verify SRS "Needs
  Review" updates; verify offline via PWA after a refresh)

---

## 9. Files & Locations Index

### Durable project files (must be moved to the new machine)
- `extract\generated_assets\*.json` — ALL asset libraries (the deliverables)
- `Sources\<folder>\*.pdf` — source books (two folders, note non-ASCII folder
  names: "Kroppsspråk & Icke-verbal kommunikation", "Beteendepsykologi,
  Socialpsykologi & Mänsklig Natur")
- `data.js` — frontend data consumed by the game PWA (repo root)
- `extract\` — pipeline code (config.py, run.py, pipeline\orchestrator.py,
  pipeline\classifier.py, output\*, review\, cache\, extracted_json\, etc.)
- `icons\`, `imports\` — frontend assets

### Reproducible / temp (not required but helpful)
- `%TEMP%\opencode\*.txt` — extracted book text
- `%TEMP%\opencode\gen_*.py` — generator scripts (legacy)
- `%TEMP%\opencode\validate.py` — validator (legacy)

### Durable pipeline tools (in-repo, since 2026-07-31)
- `extract\tools\extract_text.py` — PDF→txt dumper (pdfplumber, page markers)
- `extract\tools\validate.py` — validator (hard errors + soft warnings)
- `extract\tools\gen_bowden_p2.py` + `bowden_p2_data_{a..f}.py` — Phase 2
  Bowden generator and its per-chapter content data
- `extract\tools\split_data_js.py` — Phase 3: `data-full.js` → `data/` + `data.js`
- `extract\tools\build_frontend_assets.py` — Phase 3: `extract\generated_assets\`
  → `assets/assetlib-*.js` + `assets.js`

### Git note
The tree is now committed (d517f14 "Phase 3 start" snapshot includes the full
working tree incl. `extract/`). Future commits should follow per-feature.
Do NOT commit the source PDFs if licensing is a concern — the JSONs are derived
content.

---

## 10. Quick Start on the New Machine

1. Copy the repo folder (or clone from remote if pushed). Ensure `extract\generated_assets\` came along.
2. Python 3.x available (generators use only stdlib `json`).
3. Open an AI coding session with the workspace at the copied root.
4. Read this document, then either:
   - **Resume Phase 1 follow-up**: validate current files (Section 6 script),
   - **Start Phase 2**: ask the user which book to re-read first, re-extract
     its PDF text (needs a PDF→text tool — reinstall if the new machine lacks
     it), then follow Section 7 steps.
5. After any generation: always re-run validation and update the running total
   in the final summary message.

---

## 11. Open Questions / Decisions Logged

- Phase 2 scope and per-session granularity: ask the user when starting.
- Whether to convert assets into the actual game JSON consumed by `data.js`
  (the pipeline under `extract\` may be intended for this; `run.py` +
  `config.py` orchestrate extraction of other sources) — verify with user.
- The older `truth_and_lies_assets.json` (65 assets) vs new
  `bowden_truth_lies_assets.json` (70 assets): confirm which one the frontend
  should consume (recommend the bowden one; possibly delete/rename the other).
  **RESOLVED 2026-07-31**: bowden (255 assets) is canonical; both legacy
  duplicates retired to `extract\generated_assets\legacy\` (kept, not deleted).
