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

- Workspace root: `C:\Users\Matt\Desktop\Education\Human Behavior`
- OS: Windows, PowerShell 5.1 (commands in this doc are PowerShell)
- Git repo: yes (branch default), only `data.js` and a few commits; `extract/`
  is currently **untracked** (`git status` shows `?? extract/`) â€” commit or copy
  it before moving machines.
- Temp work dir used by the AI sessions: `C:\Users\Matt\AppData\Local\Temp\opencode\`
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
| 1 | Workbook of Attached (adult attachment) | Levine & Heller | DONE | 45 |
| 2 | The Definitive Book of Body Language | Pease & Pease | DONE (Phase 2: 200) | 200 |
| 3 | What Every BODY Is Saying | Navarro | DONE (Phase 2: 95) | 95 |
| 4 | Emotions Revealed | Ekman | DONE (deep pass) | 135 |
| 5 | Telling Lies | Ekman | DONE (deep pass) | 65 |
| 6 | The Dictionary of Body Language | Navarro | DONE (deep pass) | 75 |
| 7 | **The Body Language of Liars** | Lillian Glass | **DONE (Phase 2: 120)** | 120 |
| 8 | **The Power of Body Language** | Tonya Reiman | **DONE (Phase 2: 105)** | 105 |
| 9 | **Truth & Lies** | Bowden & Thomson | **DONE (Phase 1 new)** | 70 |

**Running total: 890 assets, all validated (see Section 6).**

### Marked `(Not)` / skip â€” do NOT generate assets for these
- Body Language (Allan Pease)
- Nonverbal Communication (general textbook)
- Self-Presentation (Leary)
- Snoop: What Your Stuff Says About You (Gosling)
- SAOL (Swedish dictionary â€” "skip SAOL for now")

### Other books with assets in generated_assets (from earlier/other tracks)
Not part of the 660 total above: Behave (31), Influence (51), Laws of Human
Nature (23), Man's Search for Meaning (10), Mistakes Were Made (36), Moral
Animal (30), Predictably Irrational (22), Righteous Mind (39), Social Animal
(47), Social Intelligence (22), Truth & Lies (65) â€” NOTE: there are TWO files
with similar names: `truth_and_lies_assets.json` (65, older/different) and
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

Latest run results (2026-07-31, after M1 warning cleanup):
- glass_liars_assets.json â€” 120 assets, ALL VALID (0 warnings)
- bowden_truth_lies_assets.json â€” 255 assets, ALL VALID (0 warnings)
- reiman_power_body_language_assets.json â€” 105 assets, ALL VALID (0 warnings)
- emotions_revealed_assets.json â€” 135 assets, ALL VALID (0 warnings; 30 short
  concept lists expanded to 8-12 items from the book text)
- dictionary_body_language_assets.json â€” 75 assets, ALL VALID (0 warnings)
- telling_lies_assets.json â€” 65 assets, ALL VALID (0 warnings)
- influence (51), social_animal (47), righteous_mind (39), mistakes (36) â€”
  ALL VALID (0 warnings; duplicate-type chapters split into sub-chapters)

Also valid (earlier passes, still with only SHORT key_concepts warnings to be
fixed in their Phase-2 passes): attached_workbook (45).
M5 books (behave, laws_human_nature, mans_search_meaning, moral_animal,
predictably_irrational, social_intelligence) still carry the legacy
missing-field warnings â€” fixed by their Phase 2 pass.
- **Grand total: 1331 assets, ALL VALID** (excluding the two known placeholder
  files `apa_nonverbal_assets.json` and `research_methods_assets.json`, which
  are not JSON objects and have 0 assets - intentionally left alone). After
  retiring the two legacy duplicates (truth_and_lies 65, power_body_language
  50), the frontend pipeline (`build_frontend_assets.py`) consumes **21
  libraries / 1,312 assets**.

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

## 8d. M1 Warning Cleanup (2026-07-31, COMPLETE)

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
- `extract\tools\split_data_js.py` â€” Phase 3: `data-full.js` â†’ `data/` + `data.js`
- `extract\tools\build_frontend_assets.py` â€” Phase 3: `extract\generated_assets\`
  â†’ `assets/assetlib-*.js` + `assets.js`

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
