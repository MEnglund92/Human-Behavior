import re

class DictionaryExtractor:
    def extract(self, pdf_path, pages, classification):
        candidates = []
        for page in pages:
            text = page.get("text", "")
            page_num = page.get("page_num", 0)
            if not text or len(text.strip()) < 100:
                continue
            candidates.extend(self._parse_entries(text, page_num))
        return candidates

    def _parse_entries(self, text, page_num):
        candidates = []
        lines = text.split("\n")
        entries = []
        current = None

        for line in lines:
            stripped = line.strip()
            if not stripped:
                if current:
                    entries.append(current)
                    current = None
                continue

            match = re.match(r"^(\d+)\.\s+([A-Z][A-Za-z\s,()/-]+?)\s*[-–—](.*)", stripped)
            if match:
                if current:
                    entries.append(current)
                num = int(match.group(1))
                concept = match.group(2).strip()
                rest = match.group(3)
                current = {"num": num, "concept": concept, "definition": rest}
            elif current:
                current["definition"] += " " + stripped

        if current:
            entries.append(current)

        seen = set()
        for entry in entries:
            concept = entry["concept"]
            definition = entry["definition"]
            definition = re.sub(r"\s+", " ", definition).strip()
            if concept.lower() in seen:
                continue
            seen.add(concept.lower())
            if len(concept) < 4 or len(concept) > 60:
                continue
            if len(definition) < 20:
                continue
            if concept[0].islower():
                continue
            candidates.append({
                "strategy": "s8_dictionary",
                "concept": concept,
                "definition": definition,
                "real_world_scenario": "",
                "case_study_cloze": "",
                "related_concepts": [],
                "page_ref": page_num,
                "confidence": 0.85,
            })

        return candidates
