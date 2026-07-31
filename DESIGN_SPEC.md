# DESIGN_SPEC.md — Visual Design Specification

A pure-prose description of the app's look and feel: colors, typography, layout, and every UI component with its states. Use this to recreate the design in another project.

---

## 1. Design concept

"Dark glassy study lab" aesthetic: a near-black backdrop with subtle blue-tinted translucent surfaces, one luminous sky-blue accent used sparingly for emphasis and glow, and warm deep-saturated tinted cards that give the layout color without breaking the dark mood. Headings and hero text use a serif display font (Playfair Display) for a classic, scholarly feel; all UI text uses Inter. Light mode inverts the same token set to a clean slate/white variant with a deeper blue accent.

---

## 2. Color palette

### 2.1 Dark theme (default)

| Token | Value | Used for |
|---|---|---|
| Background | `#050508` | Page backdrop (near-black) |
| Surface | `#0f0f18` | Cards, panels, select backgrounds, collapsible headers |
| Surface-2 | `#181825` | Sequence item chips, scrollbar thumb, progress tracks |
| Text | `#f1f5f9` | Primary text |
| Text secondary | `#cbd5e1` | Body/descriptions |
| Text tertiary | `#94a3b8` | Labels, hints, muted UI |
| Accent | `#7dd3fc` | Sky blue — active states, links, titles, highlights |
| Accent soft | `rgba(125,211,252,0.12)` | Hover fills, tags, icon boxes, block backgrounds |
| Accent glow | `0 0 30px rgba(125,211,252,0.18)` | Selected elements, primary button hover |
| Card background | `rgba(15,15,24,0.92)` | Translucent card bodies |
| Card border | `rgba(125,211,252,0.10)` | Card outlines |
| Border | `rgba(125,211,252,0.10)` | Dividers, control outlines |
| Hover border | `rgba(125,211,252,0.30)` | Hover state outlines |
| Tag background | `rgba(125,211,252,0.08)` | Tag pills, badges |
| Tag text | `#7dd3fc` | Tag pill text |
| Success | `#4ade80` | Correct answers, positive feedback |
| Error | `#f87171` | Wrong answers, destructive hover |
| Info | `#60a5fa` | Hint badges |
| Shadow | `0 4px 24px rgba(0,0,0,0.35)` | Card elevation |
| Nav background | `#0f0f18` | Left column |
| Sidebar background | `#080810` | Right column (darker than nav) |

### 2.2 Tinted card colors (dark)

Five deep, muted tints cycle through cards via nth-child (every 5th card repeats), so the grid shows a gentle rainbow of blues/greens without breaking the dark theme:

- Pink-blue `#1e2a4a`
- Teal-green `#1a3a4a`
- Lavender `#2a2a3a`
- Mint `#1a3a3a`
- Peach-olive `#2a3a2a`

Used on: concept cards and quiz answer options. In light mode these become pastels (`#dbeafe`, `#dbe8f0`, `#e2e8f0`, `#ccfbf1`, `#dcfce7`) and the cards drop their backdrop blur, using plain white surfaces with a light shadow instead.

### 2.3 Light theme (`body.light-mode`)

| Token | Value |
|---|---|
| Background | `#e2e8f0` (slate) |
| Surface | `#ffffff` |
| Surface-2 | `#cbd5e1` |
| Text | `#020617` |
| Text secondary | `#1e293b` |
| Text tertiary | `#475569` |
| Accent | `#0369a1` (deep blue) |
| Accent soft | `rgba(3,105,161,0.12)` |
| Accent glow | `0 0 20px rgba(3,105,161,0.18)` |
| Card background | `#ffffff` |
| Border | `rgba(0,0,0,0.14)` |
| Hover border | `rgba(3,105,161,0.45)` |
| Tag background | `rgba(3,105,161,0.06)` |
| Success / Error / Info | `#15803d` / `#b91c1c` / `#1d4ed8` |
| Nav / Sidebar | `#ffffff` / `#f1f5f9` |

---

## 3. Typography

- **UI font:** Inter (fallback: system sans stack — Segoe UI, Roboto, Oxygen, Ubuntu)
- **Display font:** Playfair Display (fallback: Georgia, Times New Roman) for brand, hero, module titles, card titles
- **Base size:** 16px; body line-height 1.6

Size/weight hierarchy:

| Element | Size | Weight | Face |
|---|---|---|---|
| Hero title | 2rem | 700 | Serif |
| Modal concept title | 1.4rem | 800 | Sans |
| Flashcard concept | 1.5rem | 800 | Sans, accent color |
| Scenario Lab card title | 1.25rem | 700 | Serif |
| Brand | 1.25rem | 700 | Serif, accent color |
| Deep-dive title | 1.2rem | 700 | Serif |
| Module title | 1.1rem | 700 | Serif |
| Concept card name | 0.95rem | 700 | Sans |
| Body/buttons | 0.83–0.95rem | 400–600 | Sans |
| Small labels | 0.65–0.72rem | 600, UPPERCASE, letter-spacing ~0.04–0.05em | Sans (micro-captions: stat labels, section titles, card categories) |
| Tag text | 0.62–0.7rem | 400–600 | Sans |

Micro-labels are uppercase with wide letter-spacing; this "caption" voice appears on stat labels, card categories, sidebar section titles, matrix headers.

---

## 4. Layout

Three-column shell centered in a 1320px max-width grid:

```
+------------------+---------------------------+----------------+
|   LEFT NAV 160px |      MAIN CONTENT 1fr     | RIGHT SIDEBAR  |
|  (sticky, full   |  (panels, min 100vh,      |  280px (sticky)|
|   height, scroll |   scrollable)             |  full height)  |
|   vertically)    |                           |                |
+------------------+---------------------------+----------------+
```

- **Left nav:** vertical column with a serif brand at top (underlined by a border), stacked nav items, and a language toggle pinned to the bottom (separated by a top border).
- **Main content:** panels appear/disappear with a fade + slight slide-up (10px). One panel is active at a time.
- **Right sidebar:** avatar header, stats, quick actions, review list, action buttons, stacked with 16px gaps.

### Responsive behavior

| Breakpoint | Change |
|---|---|
| ≤1024px | Right sidebar hidden entirely; nav collapses to a 56px icon-only rail; brand shrinks to a 2-letter badge ("BS") |
| ≤768px | All multi-column grids become single column (concept grid, quiz options, dashboards, resources) |
| ≤640px | Nav becomes a fixed **bottom tab bar**: horizontal icon row, full width, content gets 70px bottom padding; brand and avatar hidden |
| Always | Safe-area insets honored (`env(safe-area-inset-*)`); touch targets use `touch-action: manipulation` |

---

## 5. Left navigation

- **Brand:** serif, accent-colored, 2 lines, ~20px padding-bottom, bottom border.
- **Nav item:** emoji icon (22px wide, centered) + 0.83rem label, left-aligned, 10px radius, transparent background, tertiary text.
  - Hover: secondary text, accent-soft background fill
  - Active: solid accent background, white text (the accent-filled item is the strongest color moment in the UI)
- **Language toggle** (bottom): globe emoji + label, separated by a top border.

---

## 6. Right sidebar

- **Avatar block:** 48px circle with accent-soft fill, 2px accent-tinted border ring; below it a name (0.95rem, semibold) and a small tertiary "role" line.
- **Stat boxes:** 3-column grid; each box is a small card (card background, border, 10px radius, centered): big accent-colored value (1.2rem, bold) over a tiny uppercase label.
- **Quick Actions:** 2-column grid of small text buttons (card background, border, 10px radius, 0.72rem). Hover: accent-soft fill, brighter border/text.
- **Section titles:** tiny uppercase, letter-spaced, tertiary.
- **Needs Review list:** full-width rows with a small accent dot (6px circle) + 0.78rem text; hover brightens the border.
- **Reset button:** ghost button; hover turns the border AND text error-red.
- **Theme button:** filled card-style button ("🌙 Dark" / "☀️ Light"); a full-screen overlay smooths the theme switch.

---

## 7. Cards & components

### 7.1 Concept card (Browse)
- 20px radius, 18px padding, one of the 5 tinted backgrounds cycling by position
- Contents: category micro-label (uppercase, accent), bold name, definition (secondary, 0.78rem), related-concept tag pills (accent-soft bg, accent text)
- Hover: lifts 3px with shadow (disabled on touch devices); click opens the detail modal

### 7.2 Module card (exercise containers)
- The "frame" for exercises: translucent card background, hairline accent-tinted border, soft shadow, 20px radius, 20px padding, serif module title at top

### 7.3 Buttons
- **Default (.btn):** pill (40px radius), card background + border, secondary text; hover: brighter border, text → primary, lifts 1px
- **Primary (.btn-accent):** solid accent background, white text; hover: accent glow halo
- **Small (.btn-sm):** reduced padding/font for compact rows
- **Filter pills:** pill-shaped, transparent, tertiary text; active: solid accent fill + white text

### 7.4 Flashcard
- 3D flip card (1200px perspective), 320px tall, flips on rotation Y 180°
- **Front:** concept name (1.5rem, 800, accent) + "tap to reveal" prompt (tertiary)
- **Back:** definition (1rem) + scenario block (italic, secondary text, accent-soft background, 3px accent left border)
- Below: previous/next buttons and three SRS rating buttons (🤔 Hard / 😊 Good / 🌟 Easy)

### 7.5 Quiz options
- 2-column grid of tinted buttons (same 5-color cycling), 16px padding, 10px radius
- States: hover = accent border; selected = accent border + glow; correct = green border/text with translucent green fill; wrong = red + shake animation

### 7.6 Match rows
- Concept and scenario sides in pairs; click a concept then its match
- Selected: accent glow tint; matched: dimmed (50% opacity) with faint green tint, unclickable; wrong: red tint + shake

### 7.7 Sequence items & slots
- Pool chips: surface-2 background, pill-ish (8px radius); placed: accent-soft fill + accent border; correct: green tint; wrong: red tint + shake
- Slots: full-width dashed border boxes; filled: solid accent border + accent-soft fill

### 7.8 Cloze blanks
- Inline inputs with dashed accent border, 120px min-width, centered text; focus: solid accent border + soft glow ring; filled: accent-soft fill; correct: green; wrong: red

### 7.9 Progress bar
- 4px track (surface-2) with accent fill that animates width (0.35s ease-out curve); labels flank the bar ("2 / 10" left, "5 correct" right)

### 7.10 Scenario Lab cards
- Serif title; "visual frame" descriptive text (secondary); **mission** block (accent-soft bg, accent left border); **dossier** separated by a dashed top border containing: pre-wrapped dialogue, nonverbal log, subject baseline, and a **matrix table** (hairline borders, accent-soft header row)
- **Insight cards:** bordered cards with tiny uppercase accent labels ("KEY CONCEPTS", "INSIGHTS"); feedback line below (bold, green "Correct!" / red "Not quite.")

### 7.11 Resource cards
- Row cards: 38px icon box (accent-soft, 8px radius) + name (0.82rem, 600) + description (tertiary); hover: lift 1px + shadow; actions row with link + speaker buttons

### 7.12 Dashboard cards
- Stat card: uppercase micro-label + huge value (1.5rem, bold); module cards: name + count + 3px progress bar with accent fill

### 7.13 Deep-dive collapsibles
- Bordered rows with a toggle header (surface bg, ▶ indicator rotating 90° when open); content expands (max-height animation); **takeaway** = accent-soft block with accent left border; source links render as tag pills; SVG diagrams sit in a surface-2 panel with 10px radius

### 7.14 Badges & speaker buttons
- **Badges:** tag-background pills (0.68rem, semibold)
- **Speaker buttons:** 26px accent-soft circles with accent icon; hover: solid accent fill + white + slight scale; while speaking: pulse animation

### 7.15 Modals & overlays
- **Concept modal:** fixed full-screen backdrop `rgba(0,0,0,0.6)`, centered 560px card (surface bg, border, 28px padding, 85vh max-height, scrollable), scales in
- **Result overlay:** darker backdrop `rgba(0,0,0,0.7)`, 420px box, huge score (3rem, 800, accent), label + detail text, scale-in
- **Confetti:** full-screen, click-through; 8px colored squares fall 350px while spinning 1080° over 1.2s

---

## 8. States & micro-interactions

| Interaction | Effect |
|---|---|
| Hover on cards/buttons | Border brightens (30% accent), text lightens, cards lift 1–3px, buttons get accent glow |
| Wrong answer | Red tint + 0.4s shake (translateX ±8px) |
| Correct answer | Green tint + border; ≥70% session: confetti burst |
| Tab switch | 0.35s fade + 10px slide-up (cubic-bezier 0.22, 1, 0.36, 1) |
| Flashcard flip | 0.5s 3D rotation with same easing |
| Progress bars | Animated width transitions |
| Text-to-speech | Speaker button pulses while playing |
| Reset progress | Button border/text turn error-red on hover |
| Active nav item | Solid accent fill, white text |

---

## 9. Animations (keyframes)

| Name | Purpose |
|---|---|
| scaleIn | Modals/overlays (0.92 → 1 scale) |
| fadeIn | Overlays, modal backdrop |
| slideUp | Hero, panels (24px rise) |
| shake | Wrong answers (0.4s, ±8px) |
| confettiFall | Result celebration (350px drop + 1080° spin + fade) |
| accentPulse | Accent glow breathing on key elements |
| pulse | Speaker buttons while speaking (opacity) |

---

## 10. Scrollbar & misc

- 6px-wide scrollbar, transparent track, surface-2 thumb (hover: tertiary)
- Font smoothing enabled; `overflow-x` hidden on body
- iOS PWA support: apple-mobile-web-app meta tags, black-translucent status bar, 180px touch icon

---

## 11. Quick mental checklist

- Dark near-black backdrop, translucent blue-tinted surfaces, one sky-blue accent that only fills fully on active/primary elements
- Serif titles, Inter body, tiny uppercase letter-spaced captions
- 5-color tinted card cycle everywhere cards repeat
- Left icon nav + right stat sidebar on desktop; icon-only rail → bottom tab bar on mobile
- Everything is a soft-edged card (10/20/40px radius ladder), hairline borders, soft shadows, subtle glow
- Feedback is always color-coded green/red with shake/confetti micro-animations
