# Human Behavior Study App

An interactive **progressive web app (PWA)** for exploring the science of human behavior â€” from classical conditioning to cognitive biases. Browse concepts, test your knowledge, and track your progress. Built with vanilla HTML, CSS, and JavaScript paired with a local Python TTS server powered by Piper.

## Features

| Tab | What it does |
|---|---|
| **Browse** | Browse and filter all concepts by course and category, with concept detail modals |
| **Flashcards** | Flip through cards with SRS (Hard/Good/Easy), text-to-speech, and keyboard navigation |
| **Quiz** | Scenario-based multiple-choice quizzes with difficulty levels |
| **Match** | Match concepts to their real-world scenarios |
| **Fill in blank** | Cloze-style fill-in-the-blank exercises with word bank support |
| **Sequence** | Order steps of psychological frameworks from first to last |
| **Exam** | Mixed-mode exam (quiz, cloze, sequence questions) with configurable question count |
| **Scenario Lab** | Interactive scenario trainer: 21 scenario libraries (2,027 assets, 5 game modes) from the extracted books â€” pick a library + chapter, filter by mode/difficulty, and work through briefing â†’ mission â†’ verification, feeding results into SRS |
| **Review** | Dedicated SRS review queue: all due cards (flashcards + Scenario Lab) in one 3D-flip session with Hard/Good/Easy ratings and session summary |
| **Deep Dive** | In-depth concept articles with expandable sections, framework descriptions, and key takeaways |
| **Resources** | Reference material cards â€” PDFs, images, audio, websites, journals |
| **Dashboard** | Overall stats, per-course progress bars, SRS due count, streak tracking, module progress |

### Interactive Features

- **Language Toggle** â€” Switch between English and Swedish on the fly; all UI, data, and speech update instantly
- **Text-to-Speech (TTS)** â€” Local neural TTS via Piper (English + Swedish voices, ~70ms latency)
- **Spaced Repetition (SRS)** â€” Rate concepts Hard/Good/Easy; due items tracked globally on the sidebar and Dashboard
- **Streaks** â€” Consecutive study days tracked and displayed
- **Dark/Light Mode** â€” Toggle in the sidebar
- **PWA Offline Support** â€” Installable as a standalone app; works offline after first visit
- **Keyboard Shortcuts** â€” Alt+1 through Alt+0 to switch tabs, Space to flip flashcards

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

Wait ~4 seconds for `Ready`, then open **http://localhost:8765** in your browser.

The server handles both static file serving and TTS synthesis â€” one command, one port.

### PWA Installation

After opening the app in a supported browser (Chrome, Edge, Brave):

1. Look for the **Install** button in the address bar (or the browser menu â†’ "Install Human Behavior Study App")
2. The app will launch in its own standalone window with no browser chrome

## File Structure

```
Human Behavior/
â”œâ”€â”€ index.html            â€” The entire app (HTML + CSS + JS)
â”œâ”€â”€ data.js               â€” Aggregator: reassembles topics/deepDives/resources from data/
â”œâ”€â”€ data-full.js          â€” Monolithic data source (18 topics + deep dives + resources)
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ topics/topic-*.js â€” One file per topic (const _t_<id>)
â”‚   â”œâ”€â”€ deep-dives.js     â€” const _deepDives
â”‚   â””â”€â”€ resources.js      â€” const _resources
â”œâ”€â”€ assets.js             â€” Aggregator: const ASSET_LIBS from assets/ (Scenario Lab)
â”œâ”€â”€ assets/               â€” One file per scenario library (const _AL_<book>, 21 libraries, 2,027 assets)
â”œâ”€â”€ server.py             â€” Python HTTP server with Piper TTS endpoint
â”œâ”€â”€ imports/
â”‚   â”œâ”€â”€ __init__.py       â€” Package marker
â”‚   â””â”€â”€ tts.py            â€” Piper TTS wrapper (lazy-loading, synthesis)
â”œâ”€â”€ manifest.json         â€” PWA manifest for installable app
â”œâ”€â”€ sw.js                 â€” Service worker for offline caching (cache v8)
â”œâ”€â”€ icons/                â€” PWA app icons (192Ã—192, 512Ã—512)
â”œâ”€â”€ extract/
â”‚   â”œâ”€â”€ generated_assets/ â€” Canonical asset JSONs (per book); legacy/ holds retired duplicates
â”‚   â””â”€â”€ tools/
â”‚       â”œâ”€â”€ split_data_js.py         â€” Split data-full.js â†’ data/ (re-runnable)
â”‚       â”œâ”€â”€ build_frontend_assets.py â€” generated_assets/ â†’ assets/ + assets.js (re-runnable)
â”‚       â”œâ”€â”€ gen_bowden_p2.py         â€” Phase 2 Bowden generator (255 assets)
â”‚       â”œâ”€â”€ gen_glass_p2.py          â€” Phase 2 Glass generator (120 assets)
â”‚       â”œâ”€â”€ gen_reiman_p2.py         â€” Phase 2 Reiman generator (105 assets)
â”‚       â”œâ”€â”€ gen_definitive_p2.py     â€” Phase 2 Definitive generator (200 assets)
â”‚       â”œâ”€â”€ gen_whatbody_p2.py       â€” Phase 2 What Every BODY generator (95 assets)
│       ├── gen_attached_p2.py       — Phase 2 Attached workbook generator (90 assets)
│       ├── gen_behave_p2.py         — Phase 2 Behave generator (126 assets)
│       ├── gen_influence_p2.py      — Phase 2 Influence generator (101 assets)
│       ├── gen_laws_p2.py           — Phase 2 Laws of Human Nature generator (118 assets)
│       ├── gen_mans_p2.py           — Phase 2 Man's Search for Meaning generator (25 assets)
│       ├── gen_mistakes_p2.py       — Phase 2 Mistakes Were Made generator (86 assets)
│       ├── gen_moral_p2.py          — Phase 2 Moral Animal generator (125 assets)
│       ├── gen_predictably_p2.py    — Phase 2 Predictably Irrational generator (102 assets)
│       ├── gen_socialanimal_p2.py   — Phase 2 Social Animal generator (92 assets)
â”‚       â””â”€â”€ validate.py              â€” Asset JSON validator
â””â”€â”€ README.md              â€” This file
```

Regenerating the data split and the Scenario Lab libraries:

```powershell
python extract\tools\split_data_js.py          # data-full.js â†’ data/ + data.js
python extract\tools\build_frontend_assets.py  # extract\generated_assets â†’ assets/ + assets.js
```

Voice models (stored one level up, shared across projects):
```
tts-models/
â”œâ”€â”€ en_US-lessac-medium.onnx       â€” English voice model
â”œâ”€â”€ en_US-lessac-medium.onnx.json
â”œâ”€â”€ sv_SE-nst-medium.onnx          â€” Swedish voice model (NST)
â”œâ”€â”€ sv_SE-nst-medium.onnx.json
â”œâ”€â”€ sv_SE-alma-medium.onnx         â€” Swedish voice model (Alma)
â””â”€â”€ sv_SE-alma-medium.onnx.json
```

## Tech Stack

- **Frontend:** Vanilla HTML, CSS, JavaScript (PWA with service worker)
- **Backend:** Python 3 + `http.server` + `piper-tts` (Piper TTS engine)
- **TTS Engine:** [Piper](https://github.com/rhasspy/piper) â€” fast, local neural TTS (VITS + ONNX Runtime)
- **Storage:** `localStorage` for all user progress
- **CSS Custom Properties** â€” Dark/light theme switching
