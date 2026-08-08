#!/usr/bin/env python3
"""Print a page range (as separate pages) from a --- PAGE n --- marked text file.

Usage:
    python extract/tools/read_pages.py <file> <page_start> <page_end>
"""
import re
import sys


def main():
    src, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    txt = open(src, encoding="utf-8").read()
    parts = re.split(r"--- PAGE (\d+) ---", txt)
    idx = {}
    for i in range(1, len(parts), 2):
        idx[int(parts[i])] = parts[i + 1]
    for n in range(a, b + 1):
        if n not in idx:
            print(f"(page {n} missing)")
            continue
        print(f"\n---------------- PAGE {n} ----------------")
        print(idx[n])


if __name__ == "__main__":
    main()