import re
from extract.utils.text_cleaner import normalize_whitespace


class GlossaryExtractor:
    GLOSSARY_HEADINGS = [
        "glossary", "key terms", "key concepts", "terms to know",
        "vocabulary", "definitions", "important terms",
        "index", "about the author",
    ]

    def extract(self, pdf_path, pages, classification):
        candidates = []
        glossary_pages = self._find_glossary_pages(pages)
        if not glossary_pages:
            return []
        for page in glossary_pages:
            text = page.get("text", "")
            page_num = page.get("page_num", 0)
            if not text:
                continue
            candidates.extend(self._parse_glossary(text, page_num))
        return candidates

    REJECT_GLOSSARY_PATTERNS = [
        r"\bcontents?\b", r"\bindex\b", r"\breferences?\b", r"\bbibliography\b",
        r"\bnotes?\b", r"\bforeword\b", r"\bpreface\b", r"\bappendix\b",
        r"\bintroduction\b", r"\backnowledg", r"\babout the author\b",
        r"part\s+(one|two|three|four|five|i|ii|iii|iv|v)",
        r"chapter\s+\d+", r"page\b",
    ]

    def _find_glossary_pages(self, pages):
        glossary_pages = []
        for page in pages:
            text = page.get("text", "").strip()
            if not text:
                continue
            first_line = text.split("\n")[0].strip().lower()
            if any(heading in first_line for heading in self.GLOSSARY_HEADINGS):
                if any(re.search(pat, first_line) for pat in self.REJECT_GLOSSARY_PATTERNS):
                    continue
                glossary_pages.append(page)
                continue
            page_lines = [l for l in text.split("\n") if l.strip()]
            if len(page_lines) < 5:
                continue
            short_lines = [l for l in page_lines if 3 < len(l.strip()) < 80]
            if len(short_lines) < 5:
                continue
            ratio = len(short_lines) / len(page_lines)
            if ratio < 0.5 or ratio > 0.95:
                continue
            full_text_lower = text.lower()
            if any(re.search(pat, full_text_lower) for pat in self.REJECT_GLOSSARY_PATTERNS):
                continue
            glossary_pages.append(page)
        return glossary_pages

    def _parse_glossary(self, text, page_num):
        candidates = []
        lines = text.strip().split("\n")
        seen = set()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            match = re.match(r"^([A-Z][a-zA-Z\s\-]+?)\s{3,}(.+)$", line)
            if match:
                concept = match.group(1).strip()
                definition = match.group(2).strip()
                if self._is_valid_entry(concept, definition, seen):
                    seen.add(concept.lower())
                    candidates.append(self._make_entry(concept, definition, page_num))
                i += 1
                continue
            match = re.match(r"^([A-Z][a-zA-Z\s\-]+?)\s*[.:]\s+(.+)$", line)
            if match:
                concept = match.group(1).strip()
                definition = match.group(2).strip()
                if self._is_valid_entry(concept, definition, seen):
                    seen.add(concept.lower())
                    candidates.append(self._make_entry(concept, definition, page_num))
                i += 1
                continue
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if re.match(r"^[A-Z][a-z][A-Za-z\s\-]{2,30}$", line) and len(line) < 40:
                    if re.match(r"^[a-z]", next_line) and len(next_line) > 25:
                        concept = line.strip()
                        definition = next_line
                        if self._is_valid_entry(concept, definition, seen):
                            seen.add(concept.lower())
                            candidates.append(self._make_entry(concept, definition, page_num))
                            i += 2
                            continue
            i += 1
        return candidates

    REJECT_CONCEPTS = {
        "all rights reserved", "printed in", "copyright", "cataloguing",
        "publication data", "isbn", "library of congress", "first published",
        "second impression", "third impression", "fourth impression",
        "fifth impression", "sixth impression", "seventh impression",
        "eighth impression", "ninth impression", "tenth impression",
        "acknowledgments", "acknowledgements", "preface", "introduction",
        "about the author", "contents", "table of contents", "index",
        "foreword", "prologue", "epilogue", "appendix", "references",
        "bibliography", "further reading", "notes", "glossary",
        "part one", "part two", "part three", "part four", "part five",
        "chapter one", "chapter two", "chapter three", "chapter four",
        "conclusion", "summary", "introduction", "preface",
    }

    PRONOUNS = {
        "i", "we", "you", "he", "she", "it", "they", "me", "us", "him", "her", "them",
        "my", "our", "your", "his", "its", "their", "mine", "yours", "hers", "theirs",
    }

    AUX_VERBS = {
        "is", "are", "was", "were", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "can", "could", "shall", "should",
        "may", "might", "must",
    }

    SUBORDINATORS = {
        "although", "because", "since", "unless", "while", "whereas",
        "however", "therefore", "thus", "furthermore", "moreover",
    }

    def _is_valid_entry(self, concept, definition, seen):
        if concept.lower() in seen:
            return False
        if len(concept) < 4 or len(concept) > 55:
            return False
        if len(definition) < 15 or len(definition) > 400:
            return False
        if re.search(r"\d", concept):
            return False
        concept_lower = concept.lower().strip()
        if concept_lower in self.REJECT_CONCEPTS:
            return False
        if any(kw in concept_lower for kw in self.REJECT_CONCEPTS):
            return False

        if not concept[0].isupper():
            return False

        c_words = concept_lower.split()
        if not c_words:
            return False

        first_word = c_words[0]
        if first_word in {"the", "this", "that", "these", "those", "a", "an", "its", "our", "my", "your", "his", "her"}:
            return False
        if first_word in self.PRONOUNS:
            return False
        if self.AUX_VERBS & set(c_words):
            return False
        if self.SUBORDINATORS & set(c_words):
            return False

        if re.search(r"\b[A-Z]\.?$", concept):
            return False

        if concept == concept.upper() and len(concept.split()) > 2:
            return False

        if re.search(r"\d+\s*$", definition):
            return False
        if re.search(r"(?:page|p\.|pp\.|vol|isbn|doi|www|fax|phone|director|assistant|publisher)", definition, re.I):
            return False
        if re.search(r"\b(?:pp?\.\s*\d+|pages?\s+\d+|ch\.\s*\d+|fig\.\s*\d+|table\s+\d+)", definition, re.I):
            return False

        if re.search(r"^(?:[A-Z][a-z]+(?:\s+[A-Z]\.)+)", definition):
            return False

        if re.search(r"\(.*?(?:edition|ed\.|vol\.|volume).*?\)", definition, re.I):
            return False

        if re.search(r"(?:copyright|ISBN|published by|printed in|library of congress)", definition, re.I):
            return False

        if definition[0].isupper() and len(definition.split()) <= 4:
            return False

        if not definition[-1] in (".", "!", "?"):
            return False

        d_words = definition.lower().split()
        if len(d_words) < 4:
            return False

        return True

    def _make_entry(self, concept, definition, page_num):
        return {
            "strategy": "s5_glossary",
            "concept": concept,
            "definition": definition,
            "real_world_scenario": "",
            "case_study_cloze": "",
            "related_concepts": [],
            "page_ref": page_num,
            "confidence": 0.55,
        }
