"""Pre-extraction concept inventory for a Phase 7A book.

Scans per-chapter text and records every named model / law / heuristic /
behavior mentioned, matching against a lexicon built from
extract/generated_assets/phase7d_topics_ref.txt plus a curated domain list.
Output: <out_dir>/concept_inventory.json

Usage:
    python extract/tools/pre_extract_concepts.py <book_key> [--topics <ref.txt>]

Book text is read from extract/generated_assets/phase7a/<book_key>/chapter_*.txt.
"""

import argparse
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(HERE, "..", "generated_assets", "phase7a")
TOPICS_REF = os.path.join(HERE, "..", "generated_assets", "phase7d_topics_ref.txt")

# Curated named mechanisms that appear across the 8 target books.
DOMAIN_LEXICON = [
    "system 1", "system 2", "dual process", "dual-process", "anchoring effect",
    "anchoring and adjustment", "availability heuristic", "representativeness",
    "base rate neglect", "base-rate neglect", "law of small numbers",
    "conjunction fallacy", "hindsight bias", "outcome bias", "planning fallacy",
    "optimism bias", "loss aversion", "risk aversion", "prospect theory",
    "value function", "reference point", "endowment effect", "sunk cost",
    "sunk cost fallacy", "framing effect", "certainty effect", "possibility effect",
    "fourfold pattern", "regression to the mean", "regression to mean",
    "halo effect", "priming", "cognitive ease", "cognitive strain", "wysiati",
    "what you see is all there is", "confirmation bias", "ego depletion",
    "peak-end rule", "duration neglect", "focusing illusion", "affect heuristic",
    "substitution", "attribute substitution", "mental shotgun", "thinking fast",
    "narrow framing", "mental accounting", "status quo bias", "default effect",
    "choice architecture", "nudge", "habit loop", "cue routine reward",
    "reward loop", "keystone habit", "small wins", "willpower",
    "grit", "flow", "autotelic", "mastery", "autonomy", "purpose",
    "self-determination theory", "intrinsic motivation", "extrinsic motivation",
    "carrot and stick", "motivation 2.0", "motivation 3.0", "i-type goals",
    "x-type goals", "golden rule", "ocean", "big five", "personality types",
    "fixed mindset", "growth mindset", "incremental theory", "entity theory",
    "learning goal", "performance goal", "praise", "effort praise",
    "intelligence praise", "attribution theory", "self-handicapping",
    "amygdala hijack", "emotional intelligence", "eq", "empathy",
    "social awareness", "self-regulation", "self-awareness", "motivation",
    "interpersonal", "marshmallow test", "delay of gratification",
    "stanford prison experiment", "lucifer effect", "deindividuation",
    "dehumanization", "authority", "obedience", "milgram", "bystander effect",
    "diffusion of responsibility", "situational power", "dispositional attribution",
    "fundamental attribution error", "role playing", "conformity", "zimbardo",
    "foot-in-the-door", "gateway", "banality of evil", "good apple in a bad barrel",
    "gift of fear", "threat detection", "pre-incident indicators", "pins",
    "intuition", "gut feeling", "tyranny of positive thinking", "denial",
    "survival signals", "warning signs", "boundary", "stalking", "counterfeit",
    "dark triad", "narcissism", "machiavellianism", "psychopathy",
    "gaslighting", "manipulation", "covert manipulation", "social engineering",
    "persuasion", "hypnosis", "nlp", "neuro linguistic programming",
    "anchoring (nlp)", "mirroring", "rapport", "compliance", "influence",
    "reciprocity", "scarcity", "authority principle", "liking principle",
    "consensus principle", "commitment and consistency", "sociopath",
    "psychopath", "boundary testing", "love bombing", "trauma bonding",
    "intermittent reinforcement", "breadcrumbing", "silent treatment",
    "triangulation", "projection", "splitting", "emotional abuse",
    "mind reading", "body language", "microexpressions", "leakage",
    "baseline", "gesture clusters", "eye contact", "proxemics", "pupil dilation",
    "high context", "low context", "power pose", "posture",
    "drive theory", "curiosity", "tolerance for ambiguity", "experimenter bias",
    "replication", "ecological validity", "demand characteristics",
]

WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z' -]+[a-zA-Z]")


def load_lexicon(topics_ref):
    terms = set()
    if topics_ref and os.path.exists(topics_ref):
        with open(topics_ref, encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip().lstrip("*").strip()
                if not ln or ln.startswith("--") or ln.startswith("TOPICS="):
                    continue
                terms.add(ln.lower())
    for t in DOMAIN_LEXICON:
        terms.add(t.lower())
    return sorted(terms)


def _ordered_terms(low):
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_key", nargs="?")
    ap.add_argument("--topics", default=TOPICS_REF)
    ap.add_argument("--all", action="store_true",
                    help="run for every book dir in phase7a/")
    args = ap.parse_args()

    lexicon = load_lexicon(args.topics)
    # multi-word first so 'system 1' matches before 'system'
    lexicon_sw = sorted(lexicon, key=len, reverse=True)

    keys = []
    if args.all:
        keys = [os.path.basename(d) for d in glob.glob(os.path.join(BOOKS_DIR, "*"))
                if os.path.isdir(d)]
    else:
        keys = [args.book_key]

    for key in keys:
        book_dir = os.path.join(BOOKS_DIR, key)
        if not os.path.isdir(book_dir):
            print(f"missing dir: {book_dir}")
            continue
        inventory = {"book_key": key, "chapters": []}
        matcher = re.compile(
            r"\b(" + "|".join(re.escape(t) for t in lexicon_sw) + r")\b", re.I)
        for txt in sorted(glob.glob(os.path.join(book_dir, "chapter_*.txt"))):
            with open(txt, encoding="utf-8") as f:
                text = f.read()
            title = re.sub(r"^#\s*", "", text.splitlines()[0]) if text else ""
            counts = {}
            examples = {}
            for m in matcher.finditer(text):
                term = m.group(1).lower()
                counts[term] = counts.get(term, 0) + 1
                if term not in examples:
                    idx = m.start()
                    ctx = re.sub(r"\s+", " ", text[max(0, idx - 80):idx + len(term) + 120]).strip()
                    examples[term] = ctx
            inventory["chapters"].append({
                "file": os.path.basename(txt),
                "title": title,
                "concepts": [
                    {"term": t, "count": counts[t], "context": examples[t]}
                    for t in sorted(counts, key=lambda x: -counts[x])
                ],
            })
        out_path = os.path.join(book_dir, "concept_inventory.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(inventory, f, ensure_ascii=False, indent=2)
        total_concepts = sum(len(c["concepts"]) for c in inventory["chapters"])
        print(f"{key}: {len(inventory['chapters'])} chapters, "
              f"{total_concepts} concept mentions")


if __name__ == "__main__":
    main()
