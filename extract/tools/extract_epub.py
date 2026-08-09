"""Extract per-chapter plain text + TOC from an EPUB.

Usage:
    python extract/tools/extract_epub.py <input.epub> <book_key> <out_dir>

Writes <out_dir>/<book_key>/chapter_XXXX.txt (one per TOC entry, spine order)
and <out_dir>/<book_key>/toc.json. Content is DOM-sanitized: <aside>, <nav>,
<footer>, <sup> and CSS classes matching page-break|footnote|caption|header|
sidebar|publisher-notes are stripped so downstream concept scanning sees only
the prose.
"""

import json
import os
import re
import sys

from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub

STRIP_TAGS = {"aside", "nav", "footer", "sup", "script", "style", "img"}
STRIP_CLASS = re.compile(
    r"(page[-_]?break|footnote|caption|header|sidebar|publisher[-_]?notes|notes|"
    r"table[-_]of[-_]contents|endnote)", re.I
)
BLOCK_TAGS = {
    "p", "div", "section", "article", "li", "ul", "ol", "blockquote",
    "h1", "h2", "h3", "h4", "h5", "h6", "table", "tr", "figcaption",
}
JUNK_LINE = re.compile(r"^\s*(copyright|first published|all rights reserved|"
                       r"isbn|printed in|www\.|e?pub|kindle edition|version \d|"
                       r"illustrations?|translated by|translation ©|©|"
                       r"xml version=|<!doctype|<html|<\/html>|<body|</body>|"
                       r"^html$)\b", re.I)


def _text_of(el, out):
    for child in el.children:
        name = getattr(child, "name", None)
        if name is None:
            if isinstance(child, str):
                out.append(child)
            continue
        if name in BLOCK_TAGS:
            out.append("\n")
            _text_of(child, out)
            out.append("\n")
        elif name == "br":
            out.append("\n")
        else:
            _text_of(child, out)


def sanitize(el):
    for tag in el.find_all(STRIP_TAGS):
        tag.decompose()
    for tag in el.find_all(class_=STRIP_CLASS):
        tag.decompose()
    for tag in el.find_all(style=lambda v: v and "display:none" in (v or "").lower()):
        tag.decompose()
    buf = []
    _text_of(el, buf)
    text = "".join(buf)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    lines = [ln for ln in lines if not JUNK_LINE.match(ln)]
    return lines


def resolve_href(book, href, doc_names):
    """Map a TOC href to an actual document name in the EPUB.

    Some EPUBs ship absolute hrefs ('OEBPS/foo.xhtml'), others relative
    ('../OEBPS/foo.xhtml' or 'foo.xhtml'). Normalize and match against the
    real document list; fall back to urljoin for relative paths.
    """
    href = href.split("#")[0]
    if not href:
        return None
    from urllib.parse import urljoin

    norm = href.lstrip("/")
    by_name = {d.lstrip("/").lower(): d for d in doc_names}
    if norm.lower() in by_name:
        return by_name[norm.lower()]
    # try to resolve relative path against each document dir
    for d in doc_names:
        joined = urljoin(d, href)
        joined_norm = joined.lstrip("/")
        if joined_norm.lower() in by_name:
            return by_name[joined_norm.lower()]
    return None


def walk_toc(entries, level=1):
    """Yield (level, title, href) for every Link in ebooklib's TOC.

    ebooklib TOCs mix plain Link objects, nested (Link, children) tuples,
    and (Section, children) tuples where Section has no href of its own.
    """
    for entry in entries:
        if isinstance(entry, epub.Link):
            yield (level, entry.title, entry.href)
        elif isinstance(entry, tuple) and len(entry) == 2:
            item, children = entry
            if isinstance(item, epub.Link):
                yield (level, item.title, item.href)
            for sub in walk_toc(children, level + 1):
                yield sub
        elif isinstance(entry, (list, tuple)):
            for sub in walk_toc(entry, level):
                yield sub


def _norm(name):
    return name.lstrip("/").replace("\\", "/")


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    epub_path, book_key, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    book = epub.read_epub(epub_path)

    doc_map = {}
    order = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            name = item.get_name()
            doc_map[name] = item
            order.append(name)
    doc_names = list(doc_map.keys())

    toc_entries = []
    for lvl, title, href in walk_toc(book.toc):
        title = re.sub(r"\s+", " ", title or "").strip()
        href = resolve_href(book, href, doc_names)
        toc_entries.append({"level": lvl, "title": title, "href": href})

    # Collapse deep TOC levels: sub-items map to the same doc file, so keep the
    # first title per unique href and track level for structure.
    seen = {}
    flat = []
    for e in toc_entries:
        if not e["href"]:
            continue
        key = _norm(e["href"])
        if key not in seen:
            seen[key] = e
            flat.append(e)
        else:
            # prefer the shallowest (top-level) title for this file
            if e["level"] < seen[key]["level"]:
                seen[key]["title"] = e["title"]
                seen[key]["level"] = e["level"]

    chapters = []
    for e in flat:
        key = _norm(e["href"])
        item = doc_map.get(key)
        if item is None:
            continue
        soup = BeautifulSoup(item.get_content(), "html.parser")
        lines = sanitize(soup)
        if not lines:
            continue
        chapters.append({"title": e["title"], "href": e["href"], "lines": lines})

    out = os.path.join(out_dir, book_key)
    os.makedirs(out, exist_ok=True)
    meta = {"book_key": book_key, "source": os.path.basename(epub_path),
            "chapters": []}
    for i, ch in enumerate(chapters, 1):
        fname = f"chapter_{i:04d}.txt"
        with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
            f.write(f"# {ch['title']}\n\n")
            f.write("\n".join(ch["lines"]))
        meta["chapters"].append({"index": i, "file": fname,
                                 "title": ch["title"], "href": ch["href"]})

    with open(os.path.join(out, "toc.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    words = sum(len(c["lines"]) for c in chapters)
    print(f"{book_key}: {len(chapters)} chapters, ~{words} lines -> {out}")
    for i, ch in enumerate(chapters[:6], 1):
        print(f"  {i:3d}. {ch['title'][:80]}")


if __name__ == "__main__":
    main()
