# Human Behavior Project â€” Progress & Continuation Plan

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
**100% extraction** â€” every concept/topic in every chapter must become playable
content, even if it takes many sessions. A flat 230-asset coverage pass was
explicitly rejected as insufficient; depth per book is the priority.

**Deliverable format:** JSON files in `extract\generated_assets\`, one file per
book, all sharing one schema (Section 4). They feed a game (PWA frontend,
`data.js` at repo root) that renders 5 asset types as interactive challenges.

---

## 2. Machine / Environment Facts

- Workspace root: `C:\Users\matti\Desktop\Education\Human Behavior`
- OS: Windows, PowerShell 5.1 (commands in this doc are PowerShell)
- Git repo: yes (branch default), only `data.js` and a few commits; `extract/`
  is currently **untracked** (`git status` shows `?? extract/`) â€” commit or copy
  it before moving machines.
- Temp work dir used by the AI sessions: `C:\Users\matti\AppData\Local\Temp\opencode\`
  (NOT part of the repo â€” PDFs were copied there as `glass.pdf`, `reiman.pdf`,
  `bowden.pdf` and text-extracted to `glass.txt`, `reiman.txt`, `bowden.txt`,
  along with generator scripts `gen_*.py` and `validate.py`). These are NOT
  required on the new machine if PDFs can be re-extracted there, but they are
  handy. The JSON outputs they produced ARE the durable artifacts.
- Python is available (generators are plain stdlib `json` scripts; PDF text
  extraction used `pdftotext`-style tooling already on the machine â€” the text
  files are the extraction results and were written to %TEMP%).

---

## 3. Book Inventory & Priority

### Priority books (full deep extraction â€” done or in progress)

| # | Book | Author | Status | Assets |
|---|------|--------|--------|--------|
| 1 | Workbook of Attached (adult attachment) | Levine & Heller | DONE (Phase 2: 90) | 90 |
| 2 | The Definitive Book of Body Language | Pease & Pease | DONE (Phase 2: 200) | 200 |
| 3 | What Every BODY Is Saying | Navarro | DONE (Phase 2: 95) | 95 |
| 4 | Emotions Revealed | Ekman | DONE (deep pass) | 135 |
| 5 | Telling Lies | Ekman | DONE (deep pass) | 65 |
| 6 | The Dictionary of Body Language | Navarro | DONE (deep pass) | 75 |
| 7 | **The Body Language of Liars** | Lillian Glass | **DONE (Phase 2: 120)** | 120 |
| 8 | **The Power of Body Language** | Tonya Reiman | **DONE (Phase 2: 105)** | 105 |
| 9 | **Truth & Lies** | Bowden & Thomson | **DONE (Phase 1 new)** | 70 |
| 10 | **Behave** | Robert Sapolsky | **DONE (Phase 2: 126)** | 126 |
| 11 | **Influence (New & Expanded)** | Robert Cialdini | **DONE (Phase 2: 101)** | 101 |
| 12 | **The Laws of Human Nature** | Robert Greene | **DONE (Phase 2: 118)** | 118 |
| 13 | **Man's Search for Meaning** | Viktor Frankl | **DONE (Phase 2: 25)** | 25 |
| 14 | **Mistakes Were Made (But Not by Me)** | Tavris & Aronson | **DONE (Phase 2: 86)** | 86 |
| 15 | **The Moral Animal** | Robert Wright | **DONE (Phase 2: 125)** | 125 |
| 16 | **Predictably Irrational** | Dan Ariely | **DONE (Phase 2: 102)** | 102 |
| 17 | **The Social Animal** | Elliot Aronson | **DONE (Phase 2: 92)** | 92 |
| 18 | **The Righteous Mind** | Jonathan Haidt | **DONE (Phase 2: 104, OCR)** | 104 |
| 19 | **Social Intelligence** | Daniel Goleman | **DONE (Phase 2: 137, OCR)** | 137 |

**Running total: 1971 assets in the table, all validated (see Section 6).**

### Marked `(Not)` / skip â€” do NOT generate assets for these
- Body Language (Allan Pease)
- Nonverbal Communication (general textbook)
- Self-Presentation (Leary)
- Snoop: What Your Stuff Says About You (Gosling)
- SAOL (Swedish dictionary â€” "skip SAOL for now")

### Other books with assets in generated_assets (from earlier/other tracks)
Phase 2 DONE: Behave (126), Influence (101), Laws of Human Nature (118),
Man's Search for Meaning (25), Mistakes Were Made (86), Moral Animal (125),
Predictably Irrational (102), Social Animal (92), Righteous Mind (104, OCR),
Social Intelligence (137, OCR). M5 complete - all ten secondary books done.
Truth & Lies (65) — NOTE: there are TWO files with similar names:
`truth_and_lies_assets.json` (65, older/different) and
`bowden_truth_lies_assets.json` (70, the new Bowden Phase-1 deliverable). The
Bowden one is the Phase-1 canonical output. `apa_nonverbal_assets.json` and
`research_methods_assets.json` contain 0 assets (placeholders).

---

## 4. Asset Schema (single canonical format â€” ALL files use this)

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
1. **CUE_SCRUBBER_STATION** â€” identify/classify cues from video-style clips; reference/lexicon drills. (Glass files may use the alias `BEHAVIORAL_BOSS_BATTLE` for boss battles â€” treated as valid.)
2. **DYNAMIC_DIALOGUE_SIM** â€” roleplay/dialogue where you read cues in real time and choose responses.
3. **DECEPTION_AUDIT_FILE** â€” case-file review: analyze logs, dossiers, patterns, field data.
4. **DISCRIMINATION_MATRIX** â€” grid tasks: map cues Ã— contexts Ã— interpretations; reliability ratings.
5. **BOSS_BATTLE** â€” timed high-stakes scenario that combines multiple concepts (named `BEHAVIORAL_BOSS_BATTLE` in glass_liars_assets.json).

Rule of thumb: **5 assets per sub-section** (one of each type), sub-sections
cover every chapter's topics. Generator scripts construct them programmatically
with a small `asset()` helper (see Section 7).

---

## 5. Per-Book Structure of the Phase-1 Deliverables (most recent work)

### glass_liars_assets.json â€” "The Body Language of Liars" (Lillian Glass) â€” 120 assets / 24 chapter entries
Phase 1 (12 topical sub-sections, gl01-gl12): Lie types & morality, betrayal
trauma, developmental lying, the 7 motives, cyber/online deception, instincts
& baseline, body tells, facial tells, vocal tells, speech content,
relationship/cheating tells, psychopath/sociopath profile.

Phase 2 (2026-07-31): per-chapter entries gl13-gl24 (one per book chapter,
5 assets each: CUE_SCRUBBER_STATION Beginner, DYNAMIC_DIALOGUE_SIM
Intermediate, DECEPTION_AUDIT_FILE Intermediate, DISCRIMINATION_MATRIX
Advanced, BOSS_BATTLE Advanced). Chapter-specific topics: lying definitions &
religious stances (Ch1), celebrity case fallout + false accusations (Ch2),
animal/child/teen deception incl. Koko (Ch3), the 7 adult motives + ugly-baby
test (Ch4), online red flags + catfishing (Ch5), instincts vs. second-guessing
+ baselines (Ch6), breath/skin/posture/hands/feet tells + duping delight +
LGN (Ch7), eyes/nose/mouth/jaw tells + facial baselines (Ch8), vocal tells:
pitch/volume/tone/pacing (Ch9), verbal tells + transcript forensics (Ch10),
couple/cheating photo tells (Ch11), psychopath/sociopath profile + interview
tells (Ch12).

### reiman_power_body_language_assets.json â€” "The Power of Body Language" (Tonya Reiman) â€” 105 assets / 18 chapter entries
Ch1 Power Behind BL (Five Immutable Truths, origins, mirror neurons), Ch2
Language of the Face (7 universal emotions, eyes/eyebrows, smiles/scowls/
lips/nose/chin), Ch3 Language of the Body (head/torso, arms/hands), Ch4 Space &
Touch (4 zones, 14 social touches), Ch5 Language of Sound (paralanguage), Ch6
First Impressions (3-stage model, 17 turn-offs), Ch7 Reading Signals (norming,
10 signal clusters), Ch8 Sending Signals (WIIFM, anchoring), Ch9 Reiman Rapport
Method (10-step system).

Phase 2 (2026-07-31): added chapter-level entries re10-re18 (one per book
chapter, 5 assets each: CUE_SCRUBBER_STATION Beginner, DYNAMIC_DIALOGUE_SIM
Intermediate, DECEPTION_AUDIT_FILE Intermediate, DISCRIMINATION_MATRIX
Advanced, BOSS_BATTLE Advanced). Chapter-specific topics: signal origins
(hardwired vs. learned) + Five Immutable Truths (Ch1), seven universal emotions
+ eye/eyebrow signals + the smile lineup (Ch2), head/hand-to-head gestures +
the Bob Effect + congruence (Ch3), Hall's four zones + the fourteen social
touches (Ch4), the vocal cue spectrum + metamessages (Ch5), snap-judgment +
database-scan + rapport stages (Ch6), baseline norming + deceit signal clusters
(Ch7), WIIFM + trustworthiness + negotiation/closing (Ch8), the 10-step Reiman
Rapport Method (Ch9).

### bowden_truth_lies_assets.json â€” "Truth & Lies" (Bowden & Thomson) â€” 255 assets / 41 chapter entries (4 parts + 37 chapters) / Phase 2 COMPLETE
Core philosophy: body language is NOT a fixed code; all behavior is a display
of/response to power; the **SCAN process** (Suspend judgment â†’ Context â†’ Ask
"What else?" â†’ New judgment & test). Part One Genuine Deceptions (Ch1-4), Part
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
8-repetition eye targeting (Ch5), allotropic signals + Î¼-opioid rejection pain
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

Latest run results (2026-07-31, after M1-M4 Phase-2 passes):
- glass_liars_assets.json â€” 120 assets, ALL VALID (0 warnings)
- bowden_truth_lies_assets.json â€” 255 assets, ALL VALID (0 warnings)
- reiman_power_body_language_assets.json â€” 105 assets, ALL VALID (0 warnings)
- definitive_body_language_assets.json â€” 200 assets, ALL VALID (0 warnings)
- what_every_body_assets.json â€” 95 assets, ALL VALID (0 warnings)
- attached_workbook_assets.json â€” 90 assets, ALL VALID (0 warnings)
- emotions_revealed_assets.json â€” 135 assets, ALL VALID (0 warnings; 30 short
  concept lists expanded to 8-12 items from the book text)
- dictionary_body_language_assets.json â€” 75 assets, ALL VALID (0 warnings)
- telling_lies_assets.json â€” 65 assets, ALL VALID (0 warnings)
- influence (51), social_animal (47), righteous_mind (39), mistakes (36) â€”
  ALL VALID (0 warnings; duplicate-type chapters split into sub-chapters)
- behave_assets.json â€” 126 assets, ALL VALID (0 warnings; Phase 2: bh00-bh18)
- influence_assets.json â€” 101 assets, ALL VALID (0 warnings; Phase 2: in00-in09)
- laws_human_nature_assets.json â€” 118 assets, ALL VALID (0 warnings; Phase 2: lh00-lh18)
- mans_search_meaning_assets.json â€” 25 assets, ALL VALID (0 warnings; Phase 2: mf01-mf03)
- mistakes_assets.json â€” 86 assets, ALL VALID (0 warnings; Phase 2: mk00-mk09)
- moral_animal_assets.json â€” 125 assets, ALL VALID (0 warnings; Phase 2: ma00-ma18)
- predictably_irrational_assets.json â€” 102 assets, ALL VALID (0 warnings; Phase 2: pi00-pi15)
- social_animal_assets.json â€” 92 assets, ALL VALID (0 warnings; Phase 2: sa01-sa09)
- righteous_mind_assets.json â€” 104 assets, ALL VALID (0 warnings; Phase 2: rm00-rm12)
- social_intelligence_assets.json â€” 137 assets, ALL VALID (0 warnings; Phase 2: si00-si22)

All books are now clean (0 warnings). M5 (ten secondary books) is COMPLETE.
The last two books were extracted from scanned PDFs via Windows built-in OCR
(Windows.Media.Ocr, no install needed; render with `render_ocr_pages.py`,
OCR with `ocr_pages.ps1` in temp).
- **Grand total: 2156 assets, ALL VALID** (excluding the two known placeholder
  files `apa_nonverbal_assets.json` and `research_methods_assets.json`, which
  are not JSON objects and have 0 assets - intentionally left alone). After
  retiring the two legacy duplicates (truth_and_lies 65, power_body_language
  50), the frontend pipeline (`build_frontend_assets.py`) consumes **21
  libraries / 2,207 assets**.

Known quirk: the Reiman/Bowden generators originally emitted assets wrapped in
a redundant list `[[asset]]`; the emitted JSON files were fixed by unwrapping
(asset = asset[0] when len==1). New generators should build flat lists directly
and re-run the validator after generation.

---

## 7. Generation Workflow (how assets were produced)

1. **Extract text** â€” copy source PDF to `%TEMP%\opencode\<shortname>.pdf`,
   run a PDFâ†’text tool (pdftotext style) producing `<shortname>.txt` in the
   same temp dir. (E.g. glass.txt 239pp/320K chars, reiman.txt 360pp/581K,
   bowden.txt 216pp/512K.)
2. **Map structure** â€” read the TOC + chapter headings from the .txt to define
   sub-sections (the explore agent was used for this; may be done inline).
3. **Write generator** â€” a standalone Python file in `%TEMP%\opencode\gen_<book>.py`
   with a small `asset(type, topic, visual, mission, concepts, diff)` helper and
   a `chapter(id, title, pages, assets)` helper; writes directly to
   `extract\generated_assets\<book>_assets.json`.
4. **Run** â€” `python "%TEMP%\opencode\gen_<book>.py"`.
5. **Validate** â€” `python "%TEMP%\opencode\validate.py"` (update its file list
   if validating other books).
6. **Report totals** â€” 5 assets per sub-section; update running total (was
   470 pre-Phase-1; now 660).

IMPORTANT CONVENTIONS:
- domain strings like `"Body Language | Deception Detection"`.
- Always 5 distinct asset types per sub-section (avoid duplicating a type
  within one sub-section).
- key_concepts must be substantive book content, not generic filler.
- Difficulty levels: Beginner / Intermediate / Advanced (mix them).

---

## 8. Phase 2 (STARTED 2026-07-31 â€” Bowden complete)

The user explicitly stated that after Phase 1 extraction, **Phase 2** will be
activated, which demands an EVEN DEEPER re-read/re-extraction of the books
(some phrases used: "even deeper re-extraction", content was previously deemed
insufficient at 230 assets). Plan for Phase 2:
- Re-open each book's `.txt` (re-extract PDFs if moving machines â€” sources in
  `Sources\KroppssprÃ¥k & Icke-verbal kommunikation\` and
  `Sources\Beteendepsykologi, Socialpsykologi & MÃ¤nsklig Natur\`)
- Go section by section again, find topics NOT yet represented in the existing
  JSON (compare key_concepts coverage against the chapter text)
- Generate supplemental assets (new sub-sections / additional assets per
  sub-section) and merge into the existing JSON files (or add new files, then
  update the frontend data source)
- Re-validate everything; report the new totals
- The user may also want the 3 non-Priority books un-marked later â€” do not
  generate for them unless asked.

### Phase 2 progress

- **Bowden (Truth & Lies) â€” DONE 2026-07-31.** 70 â†’ 255 assets. Book fully
  re-read from `bowden.txt` (7634 lines / 216 pp); chapter start pages mapped
  from `--- PAGE n ---` markers; per-chapter entries `ch01`-`ch37` added with
  one asset of each type per chapter. Existing part entries bo01-bo04 kept.
  Generator lives in-repo: `extract\tools\gen_bowden_p2.py` + chapter data
  `extract\tools\bowden_p2_data_{a..f}.py`. Re-run with
  `python extract/tools/gen_bowden_p2.py` (idempotent - skips existing ids).
- **Reiman (The Power of Body Language) â€” DONE 2026-07-31.** 60 â†’ 105 assets.
  Book re-read from `reiman_p2.txt` (11347 lines / 360 pp, re-extracted from the
  source PDF with `extract\tools\extract_text.py`); chapter start pages mapped
  from `--- PAGE n ---` markers (Ch1 p37 .. Ch9 p297); per-chapter entries
  `re10`-`re18` added with one asset of each type per chapter. Existing topical
  entries re01-re09 kept. Generators live in-repo:
  `extract\tools\gen_reiman_p2.py` + data modules
  `extract\tools\reiman_p2_data_{a..d}.py`. Re-run with
  `python extract/tools/gen_reiman_p2.py` (idempotent - auto-skips existing ids).
- **Phase 2 complete â€” no books remain.** Both Phase-2 targets (Bowden, Glass,
  Reiman) are done.
- **What Every BODY Is Saying (Navarro) â€” DONE 2026-07-31.** 50 â†’ 95 assets.
  Book re-read from `whatbody_p2.txt` (8784 lines / 351 pp, re-extracted with
  `extract\tools\extract_text.py`); all 9 chapters mapped from their title
  pages (Ch1 p14 .. Ch9 p300); per-chapter entries `wb01`-`wb09` added with
  one asset of each type per chapter. Legacy entries (foreword, ch01-ch09)
  kept and their 4-item key_concepts expanded to 8-12 from the new chapter
  data. Generator + data modules in-repo: `extract\tools\gen_whatbody_p2.py`
  + `whatbody_p2_data_{a..c}.py`.
- **Behave (Sapolsky) â€” DONE 2026-07-31.** 31 â†’ 126 assets. Book re-read from
  `behave_p2.txt` (804 pp, extracted with PyMuPDF); all 17 chapters +
  Introduction + Epilogue mapped from title pages (Intro p11 .. Epilogue p683);
  per-chapter entries `bh00`-`bh18` added with one asset of each type per
  chapter. Legacy entries (ch01-ch18) kept, their missing fields backfilled
  (player_mission <- question, difficulty per type, visuals from chapter data)
  and key_concepts expanded to 8-12. Generator + data modules in-repo:
  `extract\tools\gen_behave_p2.py` + `behave_p2_data_{a..c}.py`.
- **Influence (Cialdini) â€” DONE 2026-07-31.** 51 â†’ 101 assets. Book re-read
  from `influence_p2.txt` (532 pp); Introduction + all 9 chapters mapped from
  title pages (Intro p10 .. Ch9 p389); per-chapter entries `in00`-`in09` added
  with one asset of each type per chapter. Legacy entries (ch01a..ch10) kept,
  their missing fields backfilled and key_concepts expanded to 8-12. Generator
  + data modules in-repo: `extract\tools\gen_influence_p2.py` +
  `influence_p2_data_{a..b}.py`.
- **Laws of Human Nature (Greene) â€” DONE 2026-07-31.** 23 â†’ 118 assets. Book
  re-read from `laws_p2.txt` (689 pp); Introduction + all 18 laws mapped from
  title pages (Intro p11 .. Law 18 p622); per-chapter entries `lh00`-`lh18`
  added with one asset of each type per law. Legacy entries (introduction,
  ch01-ch18) kept, their missing fields backfilled and key_concepts expanded
  to 8-12. Generator + data modules in-repo: `extract\tools\gen_laws_p2.py` +
  `laws_p2_data_{a..c}.py`.
- **Man's Search for Meaning (Frankl) â€” DONE 2026-08-01.** 10 â†’ 25 assets.
  Book re-read from `mans_p2.txt` (142 pp); Part I p15, Part II p88,
  Postscript p119 mapped from title pages; per-section entries `mf01`-`mf03`
  added with one asset of each type per section. Legacy entries (part1,
  part2, postscript) kept, their missing fields backfilled (player_mission <-
  stage_1_question) and key_concepts expanded to 8-12. Generator + data
  module in-repo: `extract\tools\gen_mans_p2.py` + `mans_p2_data_a.py`.
- **Mistakes Were Made (Tavris & Aronson) â€” DONE 2026-08-01.** 36 â†’ 86 assets.
  Book re-read from `mistakes_p2.txt` (369 pp); Introduction p12 + all 9
  chapters mapped from title pages (Intro p12 .. Ch9 p222); per-chapter
  entries `mk00`-`mk09` added with one asset of each type per chapter. Legacy
  entries (ch00a..ch09) kept, their missing fields backfilled and key_concepts
  expanded to 8-12. Generator + data modules in-repo:
  `extract\tools\gen_mistakes_p2.py` + `mistakes_p2_data_{a..b}.py`.
- **The Moral Animal (Wright) â€” DONE 2026-08-01.** 30 â†’ 125 assets. Book
  re-read from `moral_p2.txt` (407 pp); Introduction p9 + all 18 chapters
  mapped from title pages (Intro p9 .. Ch18 p377); per-chapter entries
  `ma00`-`ma18` added with one asset of each type per chapter. Legacy entries
  (ch01..ch18) kept, their missing fields backfilled and key_concepts expanded
  to 8-12. Generator + data modules in-repo: `extract\tools\gen_moral_p2.py` +
  `moral_p2_data_{a..c}.py`.
- **Predictably Irrational (Ariely) â€” DONE 2026-08-01.** 22 â†’ 102 assets.
  Book re-read from `predictably_p2.txt` (326 pp); Introduction p9 + all 15
  chapters mapped from title pages (Intro p9 .. Ch15 p244); per-chapter
  entries `pi00`-`pi15` added with one asset of each type per chapter. Legacy
  entries (ch_intro, ch01..ch15) kept, their missing fields backfilled and
  key_concepts expanded to 8-12. Generator + data modules in-repo:
  `extract\tools\gen_predictably_p2.py` + `predictably_p2_data_{a..c}.py`.
- **The Social Animal (Aronson) â€” DONE 2026-08-01.** 47 â†’ 92 assets. Book
  re-read from `socialanimal_p2.txt` (484 pp); all 9 chapters mapped from
  title pages (Ch1 p19 .. Ch9 p367); per-chapter entries `sa01`-`sa09` added
  with one asset of each type per chapter. Legacy entries (sa_ch01a..sa_ch09b)
  kept, their missing fields backfilled and key_concepts expanded to 8-12.
  Generator + data modules in-repo: `extract\tools\gen_socialanimal_p2.py` +
  `socialanimal_p2_data_{a..b}.py`.
- **The Righteous Mind (Haidt) â€” DONE 2026-08-01.** 39 â†’ 104 assets. Scanned
  PDF extracted with Windows built-in OCR (Windows.Media.Ocr via temp scripts
  `render_ocr_pages.py` + `ocr_pages.ps1`) to `righteous_p2.txt` (439 pp);
  Introduction p8 + all 12 chapters mapped from OCR title pages (Intro p8 ..
  Ch12 p289); per-chapter entries `rm00`-`rm12` added with one asset of each
  type per chapter. Legacy entries (rm_intro, rm_ch01..rm_ch12, rm_conclusion)
  kept, their missing fields backfilled and key_concepts expanded to 8-12.
  Generator + data modules in-repo: `extract\tools\gen_righteous_p2.py` +
  `righteous_p2_data_{a..c}.py`. OCR quality good (corrections logged by
  authoring agents; e.g. VVEIRD/YVEIRD -> WEIRD).
- **Social Intelligence (Goleman) â€” DONE 2026-08-01.** 22 â†’ 137 assets.
  Scanned PDF extracted with the same Windows OCR pipeline to
  `socialint_p2.txt` (413 pp); Prologue p11 + Ch1-21 + Epilogue p320 mapped
  from OCR title pages; per-chapter entries `si00`-`si22` added with one asset
  of each type per chapter. Legacy entries (ch01..ch21) kept, their missing
  fields backfilled and key_concepts expanded to 8-12. Generator + data
  modules in-repo: `extract\tools\gen_socialint_p2.py` +
  `socialint_p2_data_{a..e}.py`. M5 (all ten secondary books) is now COMPLETE.
- **M6 (visual design) - DONE 2026-08-01.** DESIGN_SPEC.md vs index.html gap
  analysis: zero gaps (tokens, typography, layout, breakpoints, components,
  states, keyframes, iOS PWA meta all already implemented; full_chain +
  smoke_v8 pass). No code changes required. M7 = user browser verification.
- **Attached workbook (Levine & Heller) â€” DONE 2026-07-31.** 45 â†’ 90 assets.
  Book re-read from `attached_p2.txt` (784 lines / 40 pp; this PDF is the
  BestWriters.club condensed summary of Attached; pdfplumber chokes on it, so
  the text was extracted with PyMuPDF instead). All 9 sections mapped from
  their content boundaries (Ch1 lines 99-204 .. Final Conclusion lines
  678-784); per-chapter entries `aw01`-`aw09` added with one asset of each
  type per chapter. Legacy entries (ch01-ch09) kept and their 4-item
  key_concepts expanded to 8-12 from the new chapter data. Generator + data
  modules in-repo: `extract\tools\gen_attached_p2.py` +
  `attached_p2_data_{a..b}.py`.
- **Definitive (The Definitive Book of Body Language) â€” DONE 2026-07-31.**
  100 â†’ 200 assets. Book re-read from `definitive_p2.txt` (8064 lines / 438 pp,
  re-extracted with `extract\tools\extract_text.py`); all 19 chapters +
  Introduction mapped from `--- PAGE n ---` markers (Intro p18 .. Ch19 p410);
  per-chapter entries `df00`-`df19` added with one asset of each type per
  chapter. Legacy topical entries (intro, ch01-ch19) kept and their 4-item
  key_concepts expanded to 8-12 from the new chapter data. Generators live
  in-repo: `extract\tools\gen_definitive_p2.py` + data modules
  `extract\tools\definitive_p2_data_{a..e}.py`. Re-run with
  `python extract/tools/gen_definitive_p2.py` (idempotent - auto-skips
  existing ids).

### Phase 2 progress (Glass)

- **Glass (The Body Language of Liars) â€” DONE 2026-07-31.** 60 â†’ 120 assets.
  Book re-read from `glass_p2.txt` (6728 lines / 239 pp, re-extracted from the
  source PDF with `extract\tools\extract_text.py`); chapter start pages mapped
  from `--- PAGE n ---` markers (Ch1 p18 .. Ch12 p209); per-chapter entries
  `gl13`-`gl24` added with one asset of each type per chapter. Existing topical
  entries gl01-gl12 kept. Generators live in-repo:
  `extract\tools\gen_glass_p2.py` + data modules
  `extract\tools\glass_p2_data_{a..d}.py`. Re-run with
  `python extract/tools/gen_glass_p2.py` (idempotent - auto-skips existing ids).

---

## 8b. Phase 3 (STARTED 2026-07-31 â€” frontend integration, COMPLETE)

Goal: expose all extracted assets in the PWA instead of leaving them as JSON.

1. **data.js split (done)** â€” the monolithic `data.js` (18 topics, deepDives,
   resources) is split into `data/topics/topic-<id>.js` + `data/deep-dives.js`
   + `data/resources.js`; `data.js` is now a small aggregator. The monolith is
   preserved as `data-full.js` (regenerate: `python extract\tools\split_data_js.py`).
   - **Bug found & fixed**: `data.js` had a stray `},` after the
     existential-humanistic topic (line 606) that made the whole file invalid
     JS (`node --check` failed); the app could not load. Fixed in `data-full.js`;
     splitter now also preserves the monolith so runs are repeatable.
2. **Scenario Lab tab (done)** â€” new ðŸ§ª tab with 21 scenario libraries (1,207
   assets) from `extract\generated_assets\*.json` (all books incl. secondary,
   minus retired legacy files):
   - Selectors: library (21 books), chapter, mode (5 asset types), difficulty
     (Beginner/Intermediate/Advanced), session size (5/10/20/All)
   - Flow per asset: briefing (visual frame + mission, plus type-specific
     dossier: dialogue / case file / matrix / subject baseline) â†’ verification
     (auto-graded multiple choice when the asset has question/choices/distractors;
     otherwise reveal insights + self-grade Got it / Missed it) â†’ insights panel
     (key concepts + correct cue/diagnosis/breakdown)
   - Results: session score overlay + confetti (â‰¥70%); every graded asset is
     written into the SM-2 SRS store (`lab:<book>: <topic>`) so the sidebar
     "Needs Review" and Dashboard pick it up
   - UI chrome bilingual (existing EN/SV toggle); asset content stays English
   - `assets.js` + `assets/assetlib-<book>.js` generated by
     `python extract\tools\build_frontend_assets.py` (re-runnable; skips legacy)
3. **Retired legacy duplicates (done)** â€” `truth_and_lies_assets.json` (65) and
   `power_body_language_assets.json` (50) moved to
   `extract\generated_assets\legacy\`; canonical sources are
   `bowden_truth_lies_assets.json` (255) and `reiman_power_body_language_assets.json` (105).
4. **Service worker (done)** â€” cache bumped to v7; FILES now lists all
   `data/` and `assets/` files.
5. **Docs (done)** â€” README + this doc updated.

### Phase 3 verification status (2026-07-31)
- All 22 data files, 22 asset files, sw.js, and the inline app script pass
  `node --check`
- Full-chain test (exact index.html script order): `topics`=18, `deepDives`=17,
  `resources`=5, `ASSET_LIBS`=21, 1,207 assets
- All 1,207 assets have asset_type + topic + difficulty_level; filters
  (book/chapter/mode/difficulty) verified in node
- `python server.py` â†’ every URL (index.html, data.js, data/*, assets/*, sw.js,
  manifest.json) returns 200
- NOTE: no automated browser test â€” do a manual pass on localhost:8765
  (Scenario Lab: pick a book, run a session in each mode; verify SRS "Needs
  Review" updates; verify offline via PWA after a refresh)

---
## 8c. Phase 4 (2026-07-31 â€” Review Mode + Glass Phase 2, COMPLETE)

1. **Review Mode tab (done)** â€” new ðŸ” tab between Scenario Lab and Deep Dive:
   pulls ALL due SRS cards (`getDueConcepts()`: flashcard entries + `lab:<book>:
   <topic>` keys) into a 3D-flip queue with ðŸ¤”ðŸ˜ŠðŸŒŸ ratings (SM-2 `updateSRS`,
   quality 2/3.5/5), progress bar + counter, auto-advance, end-of-session
   summary overlay + confetti â‰¥70%. Lab keys display the topic with the book
   title as subtitle; card backs show the entry definition/scenario (or the
   asset's mission/question for lab keys). Sidebar "Needs Review" rows and the
   Dashboard "Review n due cards" button now jump to this tab. Space flips.
   Tracks `stats.reviews`. Bilingual chrome (svUI keys added).
2. **Glass Phase 2 (done)** â€” see Â§8; 60 â†’ 120 assets; frontend rebuilt
   (21 libs / 1,267 assets); sw.js cache bumped v7 â†’ v8.
3. **Reiman Phase 2 (done)** â€” see Â§8; 60 â†’ 105 assets (re10-re18); frontend
   rebuilt (21 libs / 1,312 assets); sw.js cache bumped v8 â†’ v9.
4. **Definitive Phase 2 (done)** â€” see Â§8; 100 â†’ 200 assets (df00-df19);
   legacy lists expanded; frontend rebuilt (21 libs / 1,412 assets); sw.js
   cache bumped v10 â†’ v11.
5. **Verified** â€” inline script `node --check` OK (44 script tags / 1 inline);
   review logic unit-tested in node (lab key parsing, card-back resolution,
   fallbacks); full-chain: topics=18, deepDives=17, resources=5, ASSET_LIBS=21,
   assets=1412; all URLs 200 on port 8765. Manual browser pass recommended:
   rate a few cards in each source (flash + lab) so they become due, then run a
   Review session end-to-end.

---

## 8e. In-browser runtime bugfix (2026-08-01, COMPLETE)

The app's inline script had NEVER executed successfully in a browser since
Phase 3: `initMatch` declared `let t=load('topic_match','')` which shadowed
the translation function `t()`, then called `t('Matched: ')` in the same
scope -> `TypeError: t is not a function`. The startup `try/catch` swallowed
the error, so `updateUI()` and `renderBrowse()` never ran: only the static
browse hero rendered, everything else was blank. The same latent shadowing
existed in `initFlash`/`initQuiz`/`initCloze`/exam-start (initCloze threw on
Easy/Hard difficulty). All prior verification (node --check, HTTP 200 smoke,
data validation) never executed the inline script, so the bug went unnoticed
until the M7 manual browser pass.

1. **Fix (done)** - renamed shadowing locals: initFlash t/c -> ft/fc,
   initQuiz -> qt/qc (matching showQuiz's existing convention), initMatch ->
   mt/mc, initCloze -> ct/cc, exam start -> et/ec. No logic changes.
2. **New verification tool (done)** - `extract\tools\run_app_stub.js` runs
   the inline script in a node vm with DOM stubs: fires DOMContentLoaded,
   injects `window.__app` inside the callback (function declarations are
   hoisted), asserts clean init, switches through all 12 tabs, exercises
   cloze easy/hard paths and initMatch/renderBrowse reruns. Verified it
   FAILS on the pre-fix script (`TypeError: t is not a function`) and passes
   on the fixed one. Add to the verification chain after full_chain/smoke:
   `node extract\tools\run_app_stub.js`.
3. **Verified (done)** - stub harness ALL OK (12 tabs), `node --check` on the
   extracted inline script OK, `full_chain.py` (ASSET_LIBS 21 / assets 2207)
   and `smoke_v8.py` ALL OK. sw.js cache bumped v16 -> v17.

---

## 8f. M7 browser-pass fixes (2026-08-01, COMPLETE)

User's second browser pass surfaced 3 issues, all fixed and verified:

1. **Browse: word speaker button spoke the word AND the definition** - in
   `renderBrowse`, `sayCn` was built as `cn+'. '+def`, so the first toggle
   (`.cc-name` button) read the full concept + definition even though the
   `.cc-def` button already reads the definition separately. Fixed: `sayCn=cn`
   (word only; detail modal and flashcards already did word-only).
2. **Match: blank/unmatchable items** - 312 of 709 entries (all of topic
   `body-language-extracted`, "18. The Dictionary of Body Language") contain
   only `concept` + `definition` (no `real_world_scenario`, no `sv`, no
   `case_study_cloze`). Match renders the scenario as the right-side prompt,
   so dictionary entries produced blank sides. Same latent damage existed in
   Quiz (blank scenario box), Flash hard mode (blank front - unplayable) and
   Exam quiz-mode. Fixed with a **definition fallback** everywhere a scenario
   is rendered: `initMatch` right side, `showQuiz`, `showFlash` hard front,
   `showExam` quiz-mode (`(showSwedish&&e.sv?e.sv.real_world_scenario:
   e.real_world_scenario)||(showSwedish&&e.sv?e.sv.definition:e.definition)`).
   Sequence/Cloze/Browse were unaffected (hardcoded item lists / filtered on
   `case_study_cloze`). No content changes needed - the 100% extraction goal
   stays intact. Also hardened `data-say` attribute escaping (quotes) in
   quiz/exam speaker buttons.
3. **Layout too narrow - zoomed out 15%** - added `zoom:0.85` to the `html`
   rule (index.html:19), equivalent to browser Ctrl-; scales everything
   (nav, sidebar, 1320px shell) including px layout; supported in
   Chrome/Edge/Firefox.
4. **Harness extended (done)** - `run_app_stub.js` gained a data assertion:
   zero entries may lack `concept` AND both `real_world_scenario` +
   `definition` (guards the fallback contract).
5. **Verified (done)** - stub harness ALL OK (12 tabs, data assertion 0 bad),
   `node --check` OK, `full_chain.py` (ASSET_LIBS 21 / assets 2207) and
   `smoke_v8.py` ALL OK. sw.js cache bumped v17 -> v18.

---



Goal: eliminate all soft validator warnings except the explicitly deferred
ones (missing fields in M5 books; short key_concepts in attached/definitive/
what_every_body fixed by their Phase-2 passes).

1. **Mechanical fixes (scripted, no content loss)** â€” `Novice`â†’`Beginner`
   (58) and `Expert`â†’`Advanced` (37) difficulty renames across 6 files;
   key_concepts trimmed from >12 down to 12 (dictionary 60, glass 25, emotions
   10, telling_lies 5, reiman 3); chapters with duplicate asset_types split
   into sub-chapter entries (`re02`â†’`re02a/b/c`, `bo01`â†’`bo01a/b`, etc.),
   preserving every asset (bowden 20, reiman 10, influence 11, social_animal
   16, righteous_mind 5, mistakes 4). Chapter ids are cosmetic for the
   frontend (SRS keys use `lab:<book>: <topic>`), so stale `lab_chapter`
   localStorage values simply fall back to "All chapters".
2. **Content expansion (emotions_revealed)** â€” 30 short key_concepts lists
   (ch01a, ch01c, ch02a, ch02b, ch04b, ch05c) expanded to 8-12 items with
   book-faithful material mined from `emotions_p1.txt` (Fore people fieldwork,
   Gajdusek films, autoappraisers, refractory period mechanisms, Aristotle's
   temperate person, anticipatory vs. emerging sadness).
3. **Result** â€” 10 of 19 files now warning-free; frontend rebuilt
   (21 libs / 1,312 assets, unchanged); sw.js cache bumped v9 â†’ v10.

---

## 9. Files & Locations Index

### Durable project files (must be moved to the new machine)
- `extract\generated_assets\*.json` â€” ALL asset libraries (the deliverables)
- `Sources\<folder>\*.pdf` â€” source books (two folders, note non-ASCII folder
  names: "KroppssprÃ¥k & Icke-verbal kommunikation", "Beteendepsykologi,
  Socialpsykologi & MÃ¤nsklig Natur")
- `data.js` â€” frontend data consumed by the game PWA (repo root)
- `extract\` â€” pipeline code (config.py, run.py, pipeline\orchestrator.py,
  pipeline\classifier.py, output\*, review\, cache\, extracted_json\, etc.)
- `icons\`, `imports\` â€” frontend assets

### Reproducible / temp (not required but helpful)
- `%TEMP%\opencode\*.txt` â€” extracted book text
- `%TEMP%\opencode\gen_*.py` â€” generator scripts (legacy)
- `%TEMP%\opencode\validate.py` â€” validator (legacy)

### Durable pipeline tools (in-repo, since 2026-07-31)
- `extract\tools\extract_text.py` â€” PDFâ†’txt dumper (pdfplumber, page markers)
- `extract\tools\validate.py` â€” validator (hard errors + soft warnings)
- `extract\tools\gen_bowden_p2.py` + `bowden_p2_data_{a..f}.py` â€” Phase 2
  Bowden generator and its per-chapter content data
- `extract\tools\gen_glass_p2.py` + `glass_p2_data_{a..d}.py` â€” Phase 2
  Glass generator and its per-chapter content data
- `extract\tools\gen_reiman_p2.py` + `reiman_p2_data_{a..d}.py` â€” Phase 2
  Reiman generator and its per-chapter content data
- `extract\tools\gen_definitive_p2.py` + `definitive_p2_data_{a..e}.py` â€”
  Phase 2 Definitive generator and its per-chapter content data
- `extract\tools\gen_whatbody_p2.py` + `whatbody_p2_data_{a..c}.py` â€” Phase 2
  What Every BODY generator and its per-chapter content data
- `extract\tools\gen_attached_p2.py` + `attached_p2_data_{a..b}.py` â€” Phase 2
  Attached workbook generator and its per-chapter content data
- `extract\tools\gen_behave_p2.py` + `behave_p2_data_{a..c}.py` â€” Phase 2
  Behave generator and its per-chapter content data
- `extract\tools\gen_influence_p2.py` + `influence_p2_data_{a..b}.py` â€” Phase 2
  Influence generator and its per-chapter content data
- `extract\tools\gen_laws_p2.py` + `laws_p2_data_{a..c}.py` â€” Phase 2 Laws of
  Human Nature generator and its per-chapter content data
- `extract\tools\gen_mans_p2.py` + `mans_p2_data_a.py` â€” Phase 2 Man's Search
  for Meaning generator and its per-section content data
- `extract\tools\gen_mistakes_p2.py` + `mistakes_p2_data_{a..b}.py` â€” Phase 2
  Mistakes Were Made generator and its per-chapter content data
- `extract\tools\gen_moral_p2.py` + `moral_p2_data_{a..c}.py` â€” Phase 2 Moral
  Animal generator and its per-chapter content data
- `extract\tools\gen_predictably_p2.py` + `predictably_p2_data_{a..c}.py` â€”
  Phase 2 Predictably Irrational generator and its per-chapter content data
- `extract\tools\gen_socialanimal_p2.py` + `socialanimal_p2_data_{a..b}.py` â€”
  Phase 2 Social Animal generator and its per-chapter content data
- `extract\tools\gen_righteous_p2.py` + `righteous_p2_data_{a..c}.py` â€” Phase 2
  Righteous Mind generator and its per-chapter content data (OCR source)
- `extract\tools\gen_socialint_p2.py` + `socialint_p2_data_{a..e}.py` â€” Phase 2
  Social Intelligence generator and its per-chapter content data (OCR source)
- `extract\tools\fix_{mans,mistakes,moral,predictably,socialanimal,righteous,socialint}_legacy.py`
  â€” M5 legacy backfill scripts (player_mission <- question, difficulty per
  type, visuals from chapter data, key_concepts expanded 8-12)
- `extract\tools\split_data_js.py` â€” Phase 3: `data-full.js` â†’ `data/` + `data.js`
- `extract\tools\build_frontend_assets.py` â€” Phase 3: `extract\generated_assets\`
  â†’ `assets/assetlib-*.js` + `assets.js`
- `extract\tools\run_app_stub.js` â€” M7 bugfix: executes the inline app script
  in a node vm (DOM stubs, all-tab click-through) to catch init-time runtime
  errors that HTTP/syntax checks miss (`node extract\tools\run_app_stub.js`)

### Git note
The tree is now committed (d517f14 "Phase 3 start" snapshot includes the full
working tree incl. `extract/`). Future commits should follow per-feature.
Do NOT commit the source PDFs if licensing is a concern â€” the JSONs are derived
content.

---

## 10. Quick Start on the New Machine

1. Copy the repo folder (or clone from remote if pushed). Ensure `extract\generated_assets\` came along.
2. Python 3.x available (generators use only stdlib `json`).
3. Open an AI coding session with the workspace at the copied root.
4. Read this document, then either:
   - **Resume Phase 1 follow-up**: validate current files (Section 6 script),
   - **Start Phase 2**: ask the user which book to re-read first, re-extract
     its PDF text (needs a PDFâ†’text tool â€” reinstall if the new machine lacks
     it), then follow Section 7 steps.
5. After any generation: always re-run validation and update the running total
   in the final summary message.

---

## 11. Open Questions / Decisions Logged

- Phase 2 scope and per-session granularity: ask the user when starting.
- Whether to convert assets into the actual game JSON consumed by `data.js`
  (the pipeline under `extract\` may be intended for this; `run.py` +
  `config.py` orchestrate extraction of other sources) â€” verify with user.
- The older `truth_and_lies_assets.json` (65 assets) vs new
  `bowden_truth_lies_assets.json` (70 assets): confirm which one the frontend
  should consume (recommend the bowden one; possibly delete/rename the other).
   **RESOLVED 2026-07-31**: bowden (255 assets) is canonical; both legacy
   duplicates retired to `extract\generated_assets\legacy\` (kept, not deleted).
- **Thinking, Fast and Slow (Kahneman) - REMOVED 2026-08-01.** Source audit
   found two copies in Sources/ (identical MD5) but both are the Indonesian
   translation edition (Gramedia 2013, full text, OCR-verified). Asset content
   in this app is English, so the user chose to delete the PDFs rather than
   derive English assets from a translation. No asset library was ever
   generated for Kahneman; the ~6 concept mentions inside
   `topic-cognitive-biases.js` (Dual Process Theory, System 1/2, anchoring,
   availability) remain as the only Kahneman content. Do NOT re-flag this as
   a gap; an English copy would be needed to extract it.
- **Truth & Lies (Bowden) source PDF - DELETED 2026-08-01 (accidental).** The
   PDF (`Truth Lies What people are really thinking...pdf`) was removed by
   mistake during the Kahneman cleanup (filename contains "thinking"). Impact:
   NONE on deliverables - the 255-asset library is committed and validated,
   full book text survives in `%TEMP%\opencode\bowden.txt` (216 pp, page
   markers), the pipeline classification cache is committed at
   `extract/cache/classifications/`, and the idempotent generators + data
   modules are in-repo (`extract\tools\gen_bowden_p2.py` +
   `bowden_p2_data_{a..f}.py`). Only the raw PDF for future re-extraction is
   gone; if it is ever needed, re-download from the original source.

---

## 12. Resume Checkpoint (PROJECT COMPLETE - all phases done, deployed and verified)

If a session was interrupted, read this section first; it encodes exactly where
the M5 pass stopped. Updated after every book commit.

- 2026-08-08: PROJECT COMPLETE. Final state: 25 libraries / 2,676 Scenario Lab
  assets (BOSS_BATTLE 530, CUE_SCRUBBER_STATION 563, DECEPTION_AUDIT_FILE 539,
  DISCRIMINATION_MATRIX 523, DYNAMIC_DIALOGUE_SIM 521), 18 topics / 709
  concepts, all 312 Dictionary of Body Language entries enriched (EN + SV),
  12 tabs. Phase 6 E2E green on localhost:8765 and
  https://menglund92.github.io/Human-Behavior/ (0 console errors; screenshots
  in %TEMP%\opencode\phase6 for review). sw v23 deployed. Branches: main
  (Pages) and master in sync at 96b60c7. Remaining only: user's final visual
  review of screenshots + any desired content changes; no further automated
  steps outstanding.

- 2026-08-08: Phase 6 (final E2E) COMPLETE - real-browser CDP pass (headless
  Chrome, isolated profile) on localhost:8765 AND on the deployed Pages URL
  https://menglund92.github.io/Human-Behavior/. 12/12 tabs switch OK, 18 topics
  (19 pills incl. All), 709 concepts, Scenario Lab 25 books / 6 modes,
  EN/SV toggle OK, dark/light OK, 0 console errors; screenshots saved for user
  review. CRITICAL BUG FOUND+FIXED: the 4 new Phase 4 libraries
  (body_language, nonverbal_communication, self_presentation, snoop) were never
  added to index.html's script list, so assets.js threw ReferenceError
  (_AL_body_language not defined) and Scenario Lab crashed (ASSET_LIBS
  undefined) - fixed by adding the 4 script tags; sw v23. Also: port 8765 was
  squatted by a stale node nsprobe server (from an old session) serving a
  different project - killed; server.py is the intended server.

- 2026-08-08: Phase 5 (Dictionary enrichment) COMPLETE - all 312 entries of
  topic `body-language-extracted` (topic 18, "The Dictionary of Body Language",
  Navarro) gained `real_world_scenario` + `case_study_cloze` + full `sv` block
  (Swedish concept, definition, scenario, cloze), authored in 8 parallel-free
  sequential batches of 39 entries (1 agent per batch; `split_dict_batches.py`
  split `dictionary_entries_base.json` -> `dict_batch_01..08.json`;
  `dict_enrich_01..08.json` authored; `merge_dict_enrich.py` applied them to
  `data\topics\topic-body-language-extracted.js`; 312/312 enriched, 0 missing).
  Verification: `node --check` OK, `run_app_stub.js` ALL OK (12 tabs / 18
  topics / 25 ASSET_LIBS). sw v22. Next: Phase 6 final E2E.

- 2026-08-08: Phase 4 (final four books) COMPLETE - Body Language (Pease, 1981,
  18 ch / 90 assets, ids pease01..18), Nonverbal Communication (2nd ed., Burgoon,
  Manusov & Guerrero, 2022, 14 ch / 70 assets, ids nvc01..14), Self-Presentation
  (Leary, 1996, 9 ch / 45 assets, ids sp01..09), Snoop (Gosling, 2008, 12 ch /
  60 assets, ids snoop01..12) - 53 chapters / 265 assets total, 1 agent per
  chapter, sequential. Maps: `pease_p2_map.py` (PDF == book), `nvc_p2_map.py`
  (book = PDF - 19), `selfpres_p2_map.py` (book = PDF - 18), `snoop_p2_map.py`
  (book = PDF - 12); per-chapter files `*_p2_chNN.py`; generators
  `gen_pease_p2.py` / `gen_nvc_p2.py` / `gen_selfpres_p2.py` / `gen_snoop_p2.py`
  -> `body_language_assets.json` / `nonverbal_communication_assets.json` /
  `self_presentation_assets.json` / `snoop_assets.json`; source texts
  `%TEMP%\opencode\pease_p2.txt` (148 pp) / `nvc_p2.txt` (571 pp) /
  `selfpres_p2.txt` (268 pp) / `snoop_p2.txt` (280 pp). Verification:
  validate.py 0 warnings (TOTAL 2676 assets), build_frontend_assets.py ->
  25 libraries / 2676 assets (BOSS_BATTLE 530, CUE_SCRUBBER_STATION 563,
  DECEPTION_AUDIT_FILE 539, DISCRIMINATION_MATRIX 523, DYNAMIC_DIALOGUE_SIM 521),
  `node --check` OK, `run_app_stub.js` ALL OK (12 tabs / 18 topics / 25
  ASSET_LIBS). sw v21. Next: Phase 5 Dictionary enrichment (312 entries:
  real_world_scenario + case_study_cloze + sv), then Phase 6 final E2E.

- 2026-08-08: Handbook of Research Methods in Social and Personality Psychology
  (3rd ed., Reis, West & Judd, 2024) Phase 3 COMPLETE - 28 chapters / 140 assets
  (intro + 27 chapters, 5 per chapter, ids rm00..rm27). Old flat 28-asset
  library preserved at `extract\generated_assets\legacy\research_methods_flat_2026-08-08.json`;
  dict-style library now at `extract\generated_assets\research_methods_assets.json`.
  Map: `rmethods_p2_map.py` (book page = PDF page - 15, verified); per-chapter
  files `rmethods_p2_ch00..ch27.py` (1 agent per chapter, sequential);
  generator `gen_rmethods_p2.py`; source text `%TEMP%\opencode\rmethods_p2.txt`.
  Verification: validate.py 0 warnings (TOTAL 2411 assets), build_frontend_assets.py
  -> 21 libraries / 2411 assets, `node --check` OK, `run_app_stub.js` ALL OK
  (12 tabs / 18 topics / 21 ASSET_LIBS). sw v20. Remaining at that point:
  Pease, Nonverbal Communication, Self-Presentation, Snoop (Phase 4 - now
  complete), then Dictionary enrichment (Phase 5) and final E2E (Phase 6).

- 2026-08-08: APA Handbook of Nonverbal Communication Phase 2 COMPLETE
  (23 chapters, 115 assets, 5 per chapter). Old flat library (23 dialogue-sim
  assets) retired to `extract\generated_assets\legacy\apa_nonverbal_flat_2026-08-08.json`;
  dict-style library now at `extract\generated_assets\apa_nonverbal_assets.json`
  (ids apa01..apa23, parts I-IV, book pages from `apa_p2_map.py`). Per-chapter
  authoring files `extract\tools\apa_p2_ch01..ch23.py` (1 agent per chapter,
  sequential; template ch01; generator `gen_apa_p2.py`; page reader
  `read_pages.py` against `%TEMP%\opencode\apa_p2.txt`). Verification:
  validate.py 0 warnings, build_frontend_assets.py -> 21 libraries / 2299
  assets, `node --check` OK, `run_app_stub.js` ALL OK (12 tabs / 18 topics /
  21 ASSET_LIBS). sw v19. Remaining: research_methods_assets.json is still the
  legacy list-style 28-asset library (validate.py flags it: top level is not a
  JSON object - expected, replaced in next phase).

- 2026-08-01: source audit + cleanup - Thinking, Fast and Slow PDFs deleted at
  user request (Indonesian edition, see Section 11); Bowden PDF deleted
  accidentally during the same cleanup (see Section 11 - no deliverable
  impact). Plan A (Kahneman extraction) CANCELLED.

- Last commit at last update: `f8deb3e` (M7 t-shadowing fix, sw v17). The
  second browser-pass fix commit (voice toggle, Match fallback, zoom, sw v18)
  is described below and in section 8f.
- sw.js cache version: **v20**. Asset total: **2411** (21 libraries; validated
  grand total 2411 including retired legacy files).
- **CRITICAL BUG FIXED 2026-08-01 (M7)**: Browse showed only the static hero
  (no filter pills, no concept cards) because the app's inline script threw
  `TypeError: t is not a function` inside `initMatch` during startup. The
  init `try/catch` swallowed it, so `renderBrowse()` never ran. Root cause:
  local variables shadowed the translation function `t()` -
  `let entries=getEntries(),t=load('topic_match','')...` in `initMatch`
  (index.html), then `t('Matched: ')` was called in the same scope. The bug
  dated back to Phase 3 (`0b7f5c8`) and was never caught because all prior
  verification was HTTP/syntax/data-level - no test ever EXECUTED the inline
  script. Fix: renamed the shadowing locals in all 5 places
  (`initFlash` t/c -> ft/fc, `initQuiz` -> qt/qc, `initMatch` -> mt/mc,
  `initCloze` -> ct/cc, exam start handler -> et/ec); `initCloze` also threw
  on Easy/Hard difficulty (latent). NEW: `extract\tools\run_app_stub.js`
  executes the inline script in a node vm with DOM stubs (fires
  DOMContentLoaded, exposes `window.__app`, switches through all 12 tabs,
  exercises cloze easy/hard + initMatch/initBrowse reruns) - run it as part
  of verification:
  `node extract\tools\run_app_stub.js` (expect "ALL OK").
- M6 (apply DESIGN_SPEC.md to index.html) - COMPLETE: gap analysis of
  DESIGN_SPEC.md against the inline `<style>` block (index.html lines 14-251)
  found ZERO gaps - every token (dark `--bg:#050508` .. `--sidebar-bg:#080810`,
  light `body.light-mode` block, 5 tinted card colors + light pastels), all 7
  keyframes, all component states, typography (Inter 400-800 + Playfair
  Display 500-700 loaded line 13), layout (1320px 3-col grid, 3 responsive
  breakpoints), iOS PWA meta tags (lines 6-9), language toggle (line 272),
  theme overlay (line 457) already implemented. No CSS changes were needed.
  Verified: `full_chain.py` (ASSET_LIBS 21 / assets 2207) + `smoke_v8.py`
  ALL OK. (NOTE: `%TEMP%\opencode\verify_css.py` is STALE - it validates a
  different palette (`--accent:#7c3aed`); the manual spec diff is authoritative.)
- M7 SECOND PASS FIXES (2026-08-01, COMMITTED, sw v18) - three user-reported
  issues fixed and verified (see section 8f): (a) Browse word speaker button
  now speaks only the concept (`sayCn=cn`); (b) 312 "Dictionary of Body
  Language" entries lack `real_world_scenario`/`case_study_cloze`, so Match/
  Quiz/Flash-hard/Exam fall back to the definition as the prompt text -
  `run_app_stub.js` gained a data assertion guarding this contract (0 bad);
  (c) layout zoomed out 15% via `html{zoom:0.85}`. Verification ALL OK:
  stub harness, `node --check`, `full_chain.py` (ASSET_LIBS 21 / 2207),
  `smoke_v8.py`.
- NEXT: M7 (continues) - user browser re-verification (`python server.py`, port
  8765; hard refresh Ctrl+Shift+R twice for the new SW v18): confirm Browse
  word-only speaker, Match shows no blank sides, the new zoom feels right,
  then check PWA offline, Review mode, Scenario Lab, light/dark toggle, and
  that the design matches DESIGN_SPEC.md visually.
- M5 queue (ten secondary books) - COMPLETE:
  1. behave - DONE (126)
  2. influence - DONE (101)
  3. laws_human_nature - DONE (118)
  4. mans_search_meaning - DONE (25, mf01-mf03)
  5. mistakes - DONE (86, mk00-mk09)
  6. moral_animal - DONE (125, ma00-ma18)
  7. predictably_irrational - DONE (102, pi00-pi15)
  8. righteous_mind - DONE (104, rm00-rm12, OCR)
  9. social_animal - DONE (92, sa01-sa09)
  10. social_intelligence - DONE (137, si00-si22, OCR)
- Recipe per book: (a) extract PDF text with `extract_pdf_fitz.py` (temp script;
  pdfplumber fails on some PDFs, PyMuPDF works) to `%TEMP%\opencode\<book>_p2.txt`;
  (b) map chapter title pages from `--- PAGE N ---` markers; (c) launch authoring
  agents -> `<book>_p2_data_{a..}.py` (5 slots x 10-12 concepts, template:
  `extract\tools\whatbody_p2_data_a.py`); (d) `gen_<book>_p2.py` (clone of
  `gen_attached_p2.py`, id prefix per book); (e) `fix_<book>_legacy.py` - M5
  legacy assets ALSO miss fields (player_mission, key_concepts, difficulty_level),
  so add player_mission <- existing `question`, difficulty <- per-type default,
  expand key_concepts 8-12 from chapter pools; (f) validate 0 warnings; (g)
  `build_frontend_assets.py`, bump sw.js cache; (h) docs (Section 3 row, running
  total, Section 6, Section 8 note, Section 9 tools, README counts); (i) commit.
- Already mapped (texts may be in temp - re-extract if missing):
  - mans_search_meaning: `mans_p2.txt` (142 pp); Part I p15 (line 242), Part II
    p88 (2962), Postscript p119 (4073-4942); ids mf01-mf03; domain "Existential
    Psychology | Resilience"; 1 agent (mans_p2_data_a).
  - mistakes: `mistakes_p2.txt` (369 pp); Intro p12 (195), Ch1 p20 (519),
    Ch2 p46 (1578), Ch3 p72 (2634), Ch4 p96 (3610), Ch5 p124 (4758), Ch6 p152
    (5928), Ch7 p172 (6768), Ch8 p196 (7732), Ch9 p222 (8766-13745); ids
    mk00-mk09; domain "Self-Justification | Cognitive Dissonance"; 2 agents
    (mistakes_p2_data_a: Intro+Ch1-4, _b: Ch5-9).
  - moral_animal: `moral_p2.txt` (407 pp); Intro p9 (170), Ch1 p24 (645),
    Ch2 p38 (1119), Ch3 p61 (1932), Ch4 p100 (3325), Ch5 p115 (3860),
    Ch6 p137 (4613), Ch7 p163 (5498), Ch8 p189 (6407), Ch9 p198 (6717),
    Ch10 p220 (7477), Ch11 p238 (8090), Ch12 p245 (8317), Ch13 p273 (9314),
    Ch14 p298 (10197), Ch15 p324 (11087), Ch16 p338 (11582), Ch17 p357 (12242),
    Ch18 p377 (12941-13962); ids ma01-ma18; domain "History of Science |
    Natural Theology vs. Evolution"; 3 agents (moral_p2_data_a: Intro+Ch1-6,
    _b: Ch7-12, _c: Ch13-18).
  - predictably_irrational: `predictably_p2.txt` (326 pp); Intro p9 (65),
    Ch1 p18 (383), Ch2 p36 (946), Ch3 p58 (1720), Ch4 p72 (2211), Ch5 p93
    (2984), Ch6 p104 (3376), Ch7 p121 (3969), Ch8 p142 (4728), Ch9 p154 (5162),
    Ch10 p165 (5544), Ch11 p183 (6207), Ch12 p201 (6864), Ch13 p215 (7385),
    Ch14 p233 (8032), Ch15 p244 (8404-9914); ids pi00-pi15; domain "Behavioral
    Economics | Metacognition"; 3 agents (predictably_p2_data_a: Intro+Ch1-5,
    _b: Ch6-10, _c: Ch11-15).
  - social_animal: `socialanimal_p2.txt` (484 pp); Ch1 p19 (372), Ch2 p31
    (814), Ch3 p75 (2692), Ch4 p127 (4927), Ch5 p171 (6823), Ch6 p219 (8919),
    Ch7 p269 (11115), Ch8 p319 (13262), Ch9 p367 (15350-22935); ids sa01-sa09;
    domain "Social Psychology | Situational vs Dispositional"; 2 agents
    (socialanimal_p2_data_a: Ch1-4, _b: Ch5-9).
  - righteous_mind + social_intelligence PDFs are image scans (no text layer):
    extracted 2026-08-01 with Windows built-in OCR (temp scripts
    `render_ocr_pages.py` -> PNGs at 200dpi, `ocr_pages.ps1` -> Windows.Media.Ocr
    text) to `%TEMP%\opencode\ocr_righteous\righteous_p2.txt` (439 pp) and
    `%TEMP%\opencode\ocr_socialint\socialint_p2.txt` (413 pp). Maps:
    righteous Intro p8 (line 14), Ch1 p18 (34), Ch2 p42 (82), Ch3 p67 (132),
    Ch4 p87 (172), Ch5 p110 (218), Ch6 p127 (252), Ch7 p143 (284), Ch8 p170
    (338), Ch9 p204 (406), Ch10 p236 (470), Ch11 p261 (520), Ch12 p289 (576),
    end p439 (876); ids rm00-rm12; domain "Moral Psychology | Intuition vs
    Reason | Political Division"; 3 agents (righteous_p2_data_a: Intro+Ch1-4,
    _b: Ch5-8, _c: Ch9-12). socialint Prologue p11 (line 20), Ch1 p21 (40),
    Ch2 p35 (68), Ch3 p46 (90), Ch4 p58 (114), Ch5 p71 (140), Ch6 p90 (178),
    Ch7 p113 (224), Ch8 p125 (248), Ch9 p141 (280), Ch10 p155 (308),
    Ch11 p170 (338), Ch12 p181 (360), Ch13 p197 (392), Ch14 p206 (410),
    Ch15 p219 (436), Ch16 p231 (460), Ch17 p246 (490), Ch18 p258 (514),
    Ch19 p275 (548), Ch20 p293 (584), Ch21 p306 (610), Epilogue p320 (638),
    end p413 (824); ids si00-si22; domain "Social Neuroscience | Relationships
    | Emotional Connection"; 5 agents (socialint_p2_data_a: Prologue+Ch1-4,
    _b: Ch5-9, _c: Ch10-14, _d: Ch15-19, _e: Ch20-21+Epilogue).
    OCR notes: line-oriented files (~1KB/line, Read tool truncates at 2000
    chars - agents re-extract via PowerShell when needed); garbles corrected
    by agents (VVEIRD->WEIRD etc.).
  - behave: `behave_p2.txt` (804 pp); sections Intro p11 (line 197), Ch1 p27
    (774), Ch2 p31 (923), Ch3 p93 (3293), Ch4 p109 (3904), Ch5 p149 (5428),
    Ch6 p164 (6014), Ch7 p184 (6738), Ch8 p233 (8624), Ch9 p277 (10283),
    Ch10 p339 (12568), Ch11 p397 (14837), Ch12 p435 (16278), Ch13 p488 (18276),
    Ch14 p531 (19988), Ch15 p565 (21186), Ch16 p591 (22080), Ch17 p624 (23429),
    Epilogue p683 (25533-25627); ids bh00-bh18; domain "Behavioral Biology |
    Multilevel Analysis"; 3 agents: behave_p2_data_a (Intro+Ch1-6), _b (Ch7-12),
    _c (Ch13-17+Epilogue).
  - influence: `influence_p2.txt` (532 pp); Intro p10 (141), Ch1 p14 (281),
    Ch2 p33 (922), Ch3 p76 (2443), Ch4 p123 (4043), Ch5 p185 (6203), Ch6 p221
    (7453), Ch7 p263 (8968), Ch8 p324 (11180), Ch9 p389 (13484-16632); ids
    in00-in09; domain "Influence & Persuasion | Cognitive Heuristics"; 2 agents:
    influence_p2_data_a (Intro+Ch1-4), _b (Ch5-9).
  - laws: `laws_p2.txt` (689 pp); Intro p11 (163), L1 p23 (612), L2 p54 (1772),
    L3 p88 (3029), L4 p120 (4245), L5 p152 (5426), L6 p172 (6178), L7 p196
    (7051), L8 p229 (8294), L9 p260 (9469), L10 p293 (10705), L11 p326 (11941),
    L12 p358 (13137), L13 p397 (14622), L14 p435 (16049), L15 p486 (17978),
    L16 p524 (19417), L17 p574 (21280), L18 p622 (23078); ids lh00-lh18; domain
    "Human Nature | Self-Knowledge"; 3 agents: laws_p2_data_a (Intro+L1-6),
    _b (L7-12), _c (L13-18).
  - Source PDFs: `Sources\Beteendepsykologi, Socialpsykologi & Mänsklig Natur\`.
- After M5 (now COMPLETE) and M6 (design verified, no changes needed): M7 =
  user browser verification (manual pass on localhost:8765). M7 found and
  fixed the t-shadowing init bug (see checkpoint above); re-verify in browser:
  Browse grid + pills, all tabs, offline PWA, light/dark toggle.
