import os
import json
from extract.config import CONFIG, CACHE_DIR


class PageClassifier:
    PAGE_CLASS_TEXT = "TEXT"
    PAGE_CLASS_TEXT_SPARSE = "TEXT_SPARSE"
    PAGE_CLASS_SCANNED = "SCANNED"
    PAGE_CLASS_MIXED = "MIXED"
    PAGE_CLASS_TABLE = "TABLE"
    PAGE_CLASS_MULTI_COL = "MULTI_COL"

    def __init__(self):
        self.cache_dir = os.path.join(CACHE_DIR, "classifications")
        os.makedirs(self.cache_dir, exist_ok=True)

    def classify(self, pdf_path, pages_text, pages_images=None):
        cache_key = os.path.basename(pdf_path) + ".json"
        cache_path = os.path.join(self.cache_dir, cache_key)
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        results = []
        for i, text in enumerate(pages_text):
            char_count = len(text.strip())
            word_count = len(text.split())
            img_count = pages_images[i] if pages_images else 0
            col_count = self._detect_columns(text)
            has_tables = self._detect_table_pattern(text)
            classification = self._classify_page(char_count, word_count, img_count, col_count, has_tables)
            results.append({
                "page": i + 1,
                "class": classification,
                "char_count": char_count,
                "word_count": word_count,
                "image_count": img_count,
                "columns": col_count,
                "has_tables": has_tables,
            })
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        return results

    def _classify_page(self, char_count, word_count, img_count, columns, has_tables):
        if has_tables:
            return self.PAGE_CLASS_TABLE
        if columns > 1:
            return self.PAGE_CLASS_MULTI_COL
        if char_count > 500:
            return self.PAGE_CLASS_TEXT
        if char_count > 50:
            return self.PAGE_CLASS_TEXT_SPARSE
        if img_count > 0:
            return self.PAGE_CLASS_MIXED
        return self.PAGE_CLASS_SCANNED

    def _detect_columns(self, text):
        lines = text.split("\n")
        if len(lines) < 5:
            return 1
        x_positions = []
        for line in lines[:60]:
            stripped = line.strip()
            if stripped:
                indent = len(line) - len(line.lstrip())
                x_positions.append(indent)
        if not x_positions:
            return 1
        clusters = {}
        for x in x_positions:
            key = round(x / 15) * 15
            clusters[key] = clusters.get(key, 0) + 1
        significant = {k: v for k, v in clusters.items() if v > len(x_positions) * 0.05}
        return min(len(significant), 3)

    def _detect_table_pattern(self, text):
        lines = text.strip().split("\n")
        if len(lines) < 3:
            return False
        pipe_count = sum(1 for l in lines if "|" in l)
        tab_count = sum(1 for l in lines if "\t" in l)
        space_cols = 0
        for l in lines:
            parts = [p for p in l.split("  ") if p.strip()]
            if len(parts) >= 3:
                space_cols += 1
        total_score = pipe_count + tab_count + space_cols
        return total_score > len(lines) * 0.3
