# Human Behavior Study App

An interactive **progressive web app (PWA)** for exploring the science of human behavior — from classical conditioning to cognitive biases. Browse concepts, test your knowledge, and track your progress. Built with vanilla HTML, CSS, and JavaScript paired with a local Python TTS server powered by Piper.

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
| **Deep Dive** | In-depth concept articles with expandable sections, framework descriptions, and key takeaways |
| **Resources** | Reference material cards — PDFs, images, audio, websites, journals |
| **Dashboard** | Overall stats, per-course progress bars, SRS due count, streak tracking, module progress |

### Interactive Features

- **Language Toggle** — Switch between English and Swedish on the fly; all UI, data, and speech update instantly
- **Text-to-Speech (TTS)** — Local neural TTS via Piper (English + Swedish voices, ~70ms latency)
- **Spaced Repetition (SRS)** — Rate concepts Hard/Good/Easy; due items tracked globally on the sidebar and Dashboard
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

Wait ~4 seconds for `Ready`, then open **http://localhost:8765** in your browser.

The server handles both static file serving and TTS synthesis — one command, one port.

### PWA Installation

After opening the app in a supported browser (Chrome, Edge, Brave):

1. Look for the **Install** button in the address bar (or the browser menu → "Install Human Behavior Study App")
2. The app will launch in its own standalone window with no browser chrome

## File Structure

```
Human Behavior/
├── index.html       — The entire app (HTML + CSS + JS, ~90 KB)
├── data.js          — All course entries, topics, categories, deep dives, and resources
├── server.py        — Python HTTP server with Piper TTS endpoint
├── imports/
│   ├── __init__.py  — Package marker
│   └── tts.py       — Piper TTS wrapper (lazy-loading, synthesis)
├── manifest.json    — PWA manifest for installable app
├── sw.js            — Service worker for offline caching
├── icons/           — PWA app icons (192×192, 512×512)
└── README.md        — This file
```

Voice models (stored one level up, shared across projects):
```
tts-models/
├── en_US-lessac-medium.onnx       — English voice model
├── en_US-lessac-medium.onnx.json
├── sv_SE-nst-medium.onnx          — Swedish voice model (NST)
├── sv_SE-nst-medium.onnx.json
├── sv_SE-alma-medium.onnx         — Swedish voice model (Alma)
└── sv_SE-alma-medium.onnx.json
```

## Tech Stack

- **Frontend:** Vanilla HTML, CSS, JavaScript (PWA with service worker)
- **Backend:** Python 3 + `http.server` + `piper-tts` (Piper TTS engine)
- **TTS Engine:** [Piper](https://github.com/rhasspy/piper) — fast, local neural TTS (VITS + ONNX Runtime)
- **Storage:** `localStorage` for all user progress
- **CSS Custom Properties** — Dark/light theme switching
