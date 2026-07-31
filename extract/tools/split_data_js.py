#!/usr/bin/env python3
"""Split the monolithic root data.js into organized per-topic files.

Input : root data.js (const topics = [...]; const deepDives = {...}; const resources = {...};)
Output: data/topics/topic-<id>.js   (one file per topic, const _t_<id>)
        data/deep-dives.js          (const _deepDives)
        data/resources.js           (const _resources)
        data.js                     (new aggregator that concatenates the above)

Re-runnable: regenerates every file from the original monolithic source.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "data.js")
DATA_DIR = os.path.join(ROOT, "data")
TOPICS_DIR = os.path.join(DATA_DIR, "topics")

PAIRS = {"{": "}", "[": "]", "(": ")"}
OPENERS = set(PAIRS.keys())
CLOSERS = set(PAIRS.values())


def find_decl(text, name):
    """Return (start, open_idx, end, close_idx) of '<name> = <literal>;' using string-aware scanning.
    close_idx points at the literal's final closing bracket (excluded from slicing)."""
    m = re.search(r"const\s+" + name + r"\s*=\s*", text)
    if not m:
        raise SystemExit(f"Declaration 'const {name}' not found in {SRC}")
    start = m.start()
    open_idx = m.end()
    opener = text[open_idx]
    closer = PAIRS[opener]
    depth = 0
    i = open_idx
    in_str = None
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in "\"'`":
            in_str = ch
            i += 1
            continue
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                close_idx = i
                j = i + 1
                while j < len(text) and text[j] in " \t\r\n":
                    j += 1
                if j < len(text) and text[j] == ";":
                    return start, open_idx, j + 1, close_idx
                raise SystemExit(f"Missing ';' after 'const {name}'")
        i += 1
    raise SystemExit(f"Unbalanced literal for 'const {name}'")


def split_top_objects(array_text):
    """Split a top-level array literal text into its depth-1 object spans.
    array_text starts at the opening '['. Returns list of (rel_start, rel_end) spans."""
    assert array_text[0] == "["
    objects = []
    depth = 0
    obj_start = None
    i = 0
    in_str = None
    while i < len(array_text):
        ch = array_text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in "\"'`":
            in_str = ch
            i += 1
            continue
        if ch == "[":
            depth += 1
            if depth == 1:
                obj_start = i + 1
        elif ch == "]":
            if depth == 1:
                break
            depth -= 1
        elif ch == "{":
            if depth == 1 and obj_start is None:
                obj_start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 1:
                objects.append((obj_start, i + 1))
                obj_start = None
        i += 1
    return objects


def main():
    # The monolith is the input. If a previous run already converted data.js into
    # the aggregator, regenerate from the preserved monolith copy (data-full.js).
    src = os.path.join(ROOT, "data-full.js")
    if not os.path.exists(src):
        src = SRC
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    if "const topics = [].concat(" in text:
        raise SystemExit(
            f"{src} looks like the aggregator, not the monolithic source; "
            f"recover the monolith first (git show <rev>:data.js > data-full.js)"
        )

    _, topics_open, _, topics_close = find_decl(text, "topics")
    _, deep_open, _, deep_close = find_decl(text, "deepDives")
    _, res_open, _, res_close = find_decl(text, "resources")

    topics_array = text[topics_open : topics_close + 1]
    spans = split_top_objects(topics_array)
    if not spans:
        raise SystemExit("No topic objects found in topics array")

    os.makedirs(TOPICS_DIR, exist_ok=True)
    topics_ids = []
    topics_entries = 0
    for rel_start, rel_end in spans:
        obj = topics_array[rel_start:rel_end]
        idm = re.search(r'id:\s*"([^"]+)"', obj)
        if not idm:
            raise SystemExit("Topic object without id: " + obj[:120])
        tid = idm.group(1)
        var = "_t_" + re.sub(r"[^A-Za-z0-9_]", "_", tid)
        topics_ids.append((tid, var))
        path = os.path.join(TOPICS_DIR, f"topic-{tid}.js")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"const {var} = [\n{obj}\n];\n")
        topics_entries += obj.count("{ concept: ")
        print(f"wrote {path}")

    deep_obj = text[deep_open + 1 : deep_close]
    res_obj = text[res_open + 1 : res_close]
    with open(os.path.join(DATA_DIR, "deep-dives.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("const _deepDives = {\n" + deep_obj + "\n};\n")
    with open(os.path.join(DATA_DIR, "resources.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("const _resources = {\n" + res_obj + "\n};\n")

    with open(os.path.join(ROOT, "data-full.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    aggr = [
        "// Aggregator — data.js is now assembled from the split files below.",
        "// Load order in index.html: data/topics/*.js, data/deep-dives.js,",
        "// data/resources.js, then this file. Regenerate with:",
        "//   python extract\\tools\\split_data_js.py",
        "const topics = [].concat(",
        *[f"  {var}," for _, var in topics_ids],
        ")",
        "const deepDives = _deepDives",
        "const resources = _resources",
        "",
    ]
    with open(SRC, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(aggr))

    print(f"topics: {len(topics_ids)} files, {topics_entries} entries")
    print("deepDives/resources split; aggregator data.js written")


if __name__ == "__main__":
    main()
