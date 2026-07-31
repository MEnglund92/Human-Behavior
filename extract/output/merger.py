import os
import json
import re
from difflib import SequenceMatcher


class DataMerger:
    def __init__(self):
        self.data_js_path = ""

    def merge(self, new_entries):
        merged = list(new_entries)
        return merged

    def merge_with_existing(self, new_entries, existing_path):
        if not os.path.exists(existing_path):
            print(f"    No existing data.js found at {existing_path}")
            return new_entries
        try:
            with open(existing_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"    Cannot read existing data.js: {e}")
            return new_entries
        existing_concepts = self._extract_existing_concepts(content)
        merged = list(new_entries)
        for n_entry in new_entries:
            n_concept = n_entry.get("concept", "").lower().strip()
            n_confidence = n_entry.get("confidence", 0)
            if not n_concept:
                continue
            for e_concept, e_line, e_entry_text in existing_concepts:
                similarity = SequenceMatcher(None, n_concept, e_concept.lower()).ratio()
                if similarity > 0.85:
                    if n_confidence > 0.85:
                        print(f"    OVERWRITE (confidence {n_confidence}): {n_entry['concept']}")
        return merged

    def _extract_existing_concepts(self, content):
        concepts = []
        pattern = re.compile(r'concept:\s*"([^"]+)"')
        for match in pattern.finditer(content):
            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 300)
            context = content[start:end]
            line_num = content[:match.start()].count("\n") + 1
            concepts.append((match.group(1), line_num, context))
        return concepts
