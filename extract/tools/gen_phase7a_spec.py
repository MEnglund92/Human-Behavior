"""Generate Phase 7A asset-authoring specs from extracted chapter text.

Reads extract/generated_assets/phase7a/<book_key>/ (chapter_*.txt, toc.json,
concept_inventory.json) and emits one spec JSON per batch of ~2-4 chapters,
scaling asset density by chapter word count and applying the book's modality
weights.

Usage:
    python extract/tools/gen_phase7a_spec.py <book_key> [--chapters A-B] [--all]

Output: extract/generated_assets/phase7a/<book_key>/specs/spec_<book>_b<NN>.json
"""

import argparse
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(HERE, "..", "generated_assets", "phase7a")

# Back-matter titles to skip for every book.
GLOBAL_SKIP = ("cover", "title page", "copyright", "dedication", "contents",
               "table of contents", "acknowledg", "notes", "index",
               "about the author", "newsletter", "bibliography", "references",
               "sources and notes", "a note on sources", "further reading",
               "about this book", "about the author", "also by")

# Per-book domain profile: title, topic binding, credibility profile,
# modality weights (percent, must sum to 100), and the asset 'domain' string.
BOOK_PROFILES = {
    "kahneman": {
        "title": "Thinking, Fast and Slow (Daniel Kahneman)",
        "topic": "cognitive-biases",
        "domain": "Dual-Process Theory | Heuristics & Statistical Biases",
        "credibility": {"level": "High", "consensus": "Broad", "basis": "Empirical behavioral economics research (Kahneman & Tversky; Nobel 2002)"},
        "weights": {
            "DISCRIMINATION_MATRIX": 40,
            "DECEPTION_AUDIT_FILE": 30,
            "BOSS_BATTLE": 30,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "dedication",
                          "contents", "table of contents"],
    },
    "power_of_habit": {
        "title": "The Power of Habit (Charles Duhigg)",
        "topic": "choice-architecture",
        "domain": "Habit Loops | Behavioral Friction & Choice Architecture",
        "credibility": {"level": "Medium", "consensus": "Emerging", "basis": "Popular-science journalism with research synthesis (habit loops, keystone habits)"},
        "weights": {
            "DISCRIMINATION_MATRIX": 40,
            "BOSS_BATTLE": 40,
            "DYNAMIC_DIALOGUE_SIM": 20,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "contents",
                          "table of contents"],
    },
    "mindset": {
        "title": "Mindset (Carol S. Dweck)",
        "topic": "personality",
        "domain": "Growth vs. Fixed Mindset | Attribution Theory",
        "credibility": {"level": "Medium", "consensus": "Emerging", "basis": "Empirical education psychology (Dweck's mindset research; replication nuance)"},
        "weights": {
            "DISCRIMINATION_MATRIX": 40,
            "DYNAMIC_DIALOGUE_SIM": 40,
            "BOSS_BATTLE": 20,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "contents",
                          "table of contents"],
    },
    "lucifer_effect": {
        "title": "The Lucifer Effect (Philip Zimbardo)",
        "topic": "social-psych",
        "domain": "Situational Power | Deindividuation & Authority Compliance",
        "credibility": {"level": "High", "consensus": "Broad", "basis": "Classic experimental social psychology (Stanford Prison Experiment, Milgram)"},
        "weights": {
            "BOSS_BATTLE": 40,
            "DECEPTION_AUDIT_FILE": 30,
            "DISCRIMINATION_MATRIX": 30,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "contents",
                          "table of contents"],
    },
    "emotional_intelligence": {
        "title": "Emotional Intelligence (Daniel Goleman)",
        "topic": "interpersonal-dynamics",
        "domain": "Affective Regulation | Amygdala Hijack & Empathy",
        "credibility": {"level": "Medium", "consensus": "Contested", "basis": "Popular synthesis of affective research; EI construct scope debated"},
        "weights": {
            "DYNAMIC_DIALOGUE_SIM": 50,
            "BOSS_BATTLE": 30,
            "DECEPTION_AUDIT_FILE": 20,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "contents",
                          "table of contents", "introduction", "acknowledg"],
    },
    "drive": {
        "title": "Drive (Daniel H. Pink)",
        "topic": "personality",
        "domain": "Intrinsic Motivation | Self-Determination Theory",
        "credibility": {"level": "Medium", "consensus": "Emerging", "basis": "Popular science synthesis (Deci & Ryan self-determination research)"},
        "weights": {
            "DISCRIMINATION_MATRIX": 40,
            "BOSS_BATTLE": 40,
            "DYNAMIC_DIALOGUE_SIM": 20,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "contents",
                          "table of contents"],
    },
    "gift_of_fear": {
        "title": "The Gift of Fear (Gavin de Becker)",
        "topic": "reading-people",
        "domain": "Threat Detection | Pre-Incident Indicators & Intuition",
        "credibility": {"level": "Medium", "consensus": "Emerging", "basis": "Observational case-based expertise (de Becker's violence-prevention practice)"},
        "weights": {
            "CUE_SCRUBBER_STATION": 40,
            "DECEPTION_AUDIT_FILE": 40,
            "BOSS_BATTLE": 20,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "contents",
                          "table of contents"],
    },
    "dark_psychology": {
        "title": "Dark Psychology 7 in 1 (Compilation)",
        "topic": "dark-triad",
        "domain": "Covert Manipulation | Dark Triad Tactics & Boundary Testing",
        "credibility": {"level": "Low", "consensus": "Contested", "basis": "Self-published compilation; untested popular claims; treat as technique taxonomy only"},
        "weights": {
            "DECEPTION_AUDIT_FILE": 50,
            "BOSS_BATTLE": 30,
            "DYNAMIC_DIALOGUE_SIM": 20,
        },
        "skip_prefixes": ["cover", "title page", "copyright", "contents",
                          "table of contents"],
    },
}

# Cap per chapter to keep batches bounded even for 16k-word chapters.
DENSITY = [
    (1500, 3),
    (3000, 5),
    (5000, 8),
    (float("inf"), 12),
]


def density_for(words):
    for threshold, count in DENSITY:
        if words < threshold:
            return count
    return 12


def pick_types(n, weights, topic):
    """Distribute n assets across types per the book's modality weights."""
    names = sorted(weights, key=lambda x: -weights[x])
    out = []
    for i in range(n):
        r = (i * 100) % 100
        acc = 0
        for name in names:
            acc += weights[name]
            if r < acc:
                out.append(name)
                break
        else:
            out.append(names[0])
    # guard: never emit a 5th type when weights only name 3
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_key")
    ap.add_argument("--chapters", default=None,
                    help="e.g. 2-5 to restrict to a chapter range (1-based)")
    args = ap.parse_args()

    profile = BOOK_PROFILES[args.book_key]
    book_dir = os.path.join(BOOKS_DIR, args.book_key)
    toc = json.load(open(os.path.join(book_dir, "toc.json"), encoding="utf-8"))
    inventory = {}
    inv_path = os.path.join(book_dir, "concept_inventory.json")
    if os.path.exists(inv_path):
        inv = json.load(open(inv_path, encoding="utf-8"))
        inventory = {c["file"]: c["concepts"] for c in inv["chapters"]}

    chapters = []
    for m in toc["chapters"]:
        title = m["title"]
        tlow = title.lower()
        if any(tlow.startswith(p) for p in profile["skip_prefixes"]) or \
           any(tlow.startswith(p) for p in GLOBAL_SKIP):
            continue
        path = os.path.join(book_dir, m["file"])
        with open(path, encoding="utf-8") as f:
            text = f.read()
        words = len(text.split())
        chapters.append({**m, "words": words, "text": text})

    if args.chapters:
        lo, hi = (int(x) for x in args.chapters.split("-"))
        # map global chapter index (1-based) to filtered list order
        chapters = [c for c in chapters if lo <= c["index"] <= hi]

    if not chapters:
        print("no chapters selected")
        return

    # split into batches of at most 4 chapters or ~9000 words
    batches = []
    cur = []
    cur_words = 0
    for c in chapters:
        if cur and (len(cur) >= 4 or cur_words + c["words"] > 9000):
            batches.append(cur)
            cur = []
            cur_words = 0
        cur.append(c)
        cur_words += c["words"]
    if cur:
        batches.append(cur)

    spec_dir = os.path.join(book_dir, "specs")
    os.makedirs(spec_dir, exist_ok=True)
    for bi, batch in enumerate(batches, 1):
        chapter_meta = []
        for c in batch:
            concepts = inventory.get(c["file"], [])
            chapter_meta.append({
                "index": c["index"],
                "title": c["title"],
                "words": c["words"],
                "asset_count": density_for(c["words"]),
                "text_path": f"extract/generated_assets/phase7a/{args.book_key}/{c['file']}",
                "top_concepts": [
                    {"term": k["term"], "context": k["context"]}
                    for k in concepts[:15]
                ],
            })
        spec = {
            "spec_file": f"spec_{args.book_key}_b{bi:02d}.json",
            "book_key": args.book_key,
            "book_title": profile["title"],
            "topic": profile["topic"],
            "domain": profile["domain"],
            "credibility_profile": profile["credibility"],
            "modality_weights": profile["weights"],
            "chapter_count": len(batch),
            "chapters": chapter_meta,
        }
        out_path = os.path.join(spec_dir, spec["spec_file"])
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False, indent=2)
        counts = [c["asset_count"] for c in chapter_meta]
        print(f"{spec['spec_file']}: chapters {[c['index'] for c in batch]} "
              f"-> assets {counts} (total {sum(counts)})")


if __name__ == "__main__":
    main()
