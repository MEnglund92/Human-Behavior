# Human Behavior Study App

An interactive **progressive web app (PWA)** for exploring the science of human behavior — from classical conditioning to cognitive biases. Browse concepts, test your knowledge, and track your progress. Built with vanilla HTML, CSS, and JavaScript paired with a local Python TTS server powered by Piper.

## Features

| Tab | What it does |
|---|---|
| **Library** | Browse and filter all 20 topics by course and category, with concept detail modals |
| **Retrieval Cards** | Flip through cards with SRS (Hard/Good/Easy), text-to-speech, and keyboard navigation |
| **Diagnostic Quiz** | Scenario-based multiple-choice quizzes with difficulty levels |
| **Concept Matching** | Match concepts to their real-world scenarios |
| **Case Reconstruction** | Cloze-style fill-in-the-blank exercises with word bank support |
| **Process Sequencing** | Order steps of psychological frameworks from first to last |
| **Comprehensive Assessment** | Mixed-mode exam (quiz, cloze, sequence questions) with configurable question count |
| **Behavioral Simulation Engine** | Interactive scenario trainer: 33 scenario libraries (4,125 assets, 5 game modes) — pick a library + chapter, filter by mode/difficulty, and work through briefing → mission → verification, feeding results into SRS |
| **Spaced Review** | Dedicated SRS review queue: all due cards (flashcards + Scenario Lab) in one 3D-flip session with Hard/Good/Easy ratings and session summary |
| **Deep Dive** | In-depth concept articles with expandable sections, framework descriptions, evidence tiers, and key takeaways |
| **Concept Map** | Interactive radial map of core concepts with a guided tour |
| **Resources** | Reference material cards — PDFs, images, audio, websites, journals |
| **Analytics** | Overall stats, per-course progress bars, SRS due count, streak tracking, module progress |

### Interactive Features

- **Language Toggle** — Switch between English and Swedish on the fly; all UI, data, and speech update instantly
- **Text-to-Speech (TTS)** — Local neural TTS via Piper (English + Swedish voices, ~70ms latency)
- **Spaced Repetition (SRS)** — Rate concepts Hard/Good/Easy; due items tracked globally on the sidebar and Analytics tab
- **Evidence Tiers** — Scenario Lab credibility badges and Deep Dive sections show the empirical evidence class (Empirical / Observational-Tactical / Contested-Low)
- **Calibration Engine** — Tracks your prediction confidence vs. actual results and surfaces a Calibration Index
- **Streaks** — Consecutive study days tracked and displayed
- **Dark/Light Mode** — Toggle in the sidebar
- **PWA Offline Support** — Installable as a standalone app; works offline after first visit
- **Keyboard Shortcuts** — Alt+1 through Alt+0 to switch tabs, Space to flip flashcards

## How to Run / Start

The app requires the Python TTS server to be running for text-to-speech. The server also serves the static files.

### Prerequisites

- Python 3.9+ with `piper-tts` installed: `pip install piper-tts`
- Voice models downloaded to `../tts-models/`

### Quick start

```powershell
cd "C:\Users\Matt\Desktop\Education\Human Behavior"
python server.py
```

Wait ~4 seconds for `Ready`, then open **http://localhost:8766** in your browser.

The server handles both static file serving and TTS synthesis — one command, one port.

Port is configurable via the `PORT` environment variable if 8766 is taken:

```powershell
$env:PORT=8767; python server.py
```

### PWA Installation

After opening the app in a supported browser (Chrome, Edge, Brave):

1. Look for the **Install** button in the address bar (or the browser menu → "Install Human Behavior Study App")
2. The app will launch in its own standalone window with no browser chrome

## File Structure

```
Human Behavior/
├── .gitignore                  # Ignores Sources/, book folders, caches, OS junk
├── .opencode/
│   └── plans/
│       └── concept-map-v2.md   # Working notes for the Concept Map v2 build
├── DESIGN_SPEC.md              # Visual design specification (look & feel reference)
├── PROJECT_STATUS_AND_PLAN.md  # Progress & continuation plan (full handoff doc)
├── README.md                   # This file
├── index.html                  # The entire app (HTML + CSS + JS)
├── data.js                     # Aggregator: reassembles topics/deepDives/resources from data/
├── data-full.js                # Monolithic data source (18 topics + deep dives + resources)
├── data/
│   ├── deep-dives.js           # const _deepDives
│   ├── resources.js            # const _resources
│   └── topics/                 # One file per topic (const _t_<id>)
│       ├── topic-intro-behavior.js
│       ├── topic-behavioral-psych.js
│       └── ... 20 topic files total
├── assets.js                   # Aggregator: const ASSET_LIBS from assets/ (Scenario Lab)
├── assets/                     # Scenario Lab libraries (33 libraries, 4,125 assets)
│   ├── assetlib-kahneman.js            # const _AL_<book> — one file per library
│   ├── assetlib-influence.js
│   └── ... 33 library files total
├── imports/
│   ├── __init__.py             # Package marker
│   └── tts.py                  # Piper TTS wrapper (lazy-loading, synthesis)
├── server.py                   # Python HTTP server with Piper TTS endpoint (default port 8766)
├── manifest.json               # PWA manifest for installable app
├── sw.js                       # Service worker for offline caching (cache v32)
├── icons/                      # PWA app icons
│   ├── icon-180.png
│   ├── icon-192.png
│   └── icon-512.png
└── extract/                    # Book extraction pipeline (PDF/EPUB → scenario assets)
    ├── __init__.py             # Package marker
    ├── config.py               # Extraction pipeline configuration
    ├── run.py                  # Pipeline entry point
    ├── setup_deps.py           # Dependency setup helper
    ├── engines/                # OCR, text, table, and hybrid extraction engines
    ├── extracted_json/         # Raw per-book extraction output (source of truth for builds)
    ├── fusion/                 # Deduplicator, quality filter, scorer, voter
    ├── generated_assets/       # Canonical asset JSONs (one per book)
    │   ├── legacy/             # Retired duplicates (kept for reference)
    │   ├── phase7a/            # Phase 7A deep-dive specs, outputs, and merges
    │   ├── phase7b/            # Phase 7B deep-dive specs and outputs
    │   └── *_assets.json       # Canonical assets, e.g. kahneman_assets.json
    ├── output/                 # JSON writers and merger
    ├── pending_rename/         # Files awaiting rename/merge
    ├── pipeline/               # Classifier and orchestrator
    ├── review/                 # Web review tool for extraction results
    │   └── static/             # app.js, index.html, style.css
    ├── strategies/             # s1–s8 extraction strategies (regex, NLP, cloze, glossary…)
    ├── tools/                  # Generators and build scripts (see below)
    ├── translation/            # Alignment + DeepL client
    └── utils/                  # Config validator, layout analyzer, text cleaner, path helpers
```

Not tracked in git: `Sources/` (the original PDF/EPUB books) and the shared `../tts-models/` voice models — both are excluded via `.gitignore`.

### extract/tools/ — key scripts

| Script | Purpose |
|---|---|
| `split_data_js.py` | Split `data-full.js` → `data/` + `data.js` (re-runnable) |
| `build_frontend_assets.py` | `generated_assets/` → `assets/` + `assets.js` (re-runnable) |
| `validate.py` | Asset JSON validator |
| `gen_*_p2.py`, `*_p2_*.py` | Per-book Phase 2 asset generators (e.g. `gen_glass_p2.py`, `apa_p2_ch01.py`) |
| `merge_*.py` | Phase 7A/B merges (dives, maps, credibility, dictionary enrichment) |
| `run_app_stub.js` | Headless app test stub (browser-less smoke test) |

Regenerating the data split and the Scenario Lab libraries:

```powershell
python extract\tools\split_data_js.py          # data-full.js → data/ + data.js
python extract\tools\build_frontend_assets.py  # extract\generated_assets → assets/ + assets.js
```

## Voice Models

Stored one level up from the project root, shared across projects:

```
tts-models/
├── en_US-lessac-medium.onnx        # English voice model
├── en_US-lessac-medium.onnx.json
├── sv_SE-nst-medium.onnx           # Swedish voice model (NST)
├── sv_SE-nst-medium.onnx.json
├── sv_SE-alma-medium.onnx          # Swedish voice model (Alma)
└── sv_SE-alma-medium.onnx.json
```

## Tech Stack

- **Frontend:** Vanilla HTML, CSS, JavaScript (PWA with service worker)
- **Backend:** Python 3 + `http.server` + `piper-tts` (Piper TTS engine)
- **TTS Engine:** [Piper](https://github.com/rhasspy/piper) — fast, local neural TTS (VITS + ONNX Runtime)
- **Storage:** `localStorage` for all user progress
- **CSS Custom Properties** — Dark/light theme switching
