"""Dump all pages of a PDF to a plain-text file.

Usage:
    python extract/tools/extract_text.py <input.pdf> <output.txt>

Uses pdfplumber; falls back to PyPDF2 if pdfplumber fails.
Page breaks are emitted as "\f" (form feed) so downstream TOC/heading
scanning can split by page.
"""

import sys

import pdfplumber


def extract(pdf_path):
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
    except Exception as e:
        print(f"pdfplumber failed ({e}); trying PyPDF2...", file=sys.stderr)
        from PyPDF2 import PdfReader

        reader = PdfReader(pdf_path)
        pages = [p.extract_text() or "" for p in reader.pages]
    return pages


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    pages = extract(src)
    with open(dst, "w", encoding="utf-8") as f:
        for i, text in enumerate(pages, 1):
            f.write(f"\n\f\n--- PAGE {i} ---\n")
            f.write(text)
    print(f"wrote {len(pages)} pages -> {dst}")


if __name__ == "__main__":
    main()
