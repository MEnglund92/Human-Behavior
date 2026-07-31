import re
from extract.utils.text_cleaner import normalize_whitespace, extract_sentences
from difflib import SequenceMatcher


class ClozeGenerator:
    def extract(self, pdf_path, pages, classification):
        candidates = []
        for page in pages:
            text = page.get("text", "")
            page_num = page.get("page_num", 0)
            if not text:
                continue
            candidates.extend(self._generate_clozes(text, page_num))
        return candidates

    def _generate_clozes(self, text, page_num):
        candidates = []
        sentences = extract_sentences(text)
        seen = set()
        for sent in sentences:
            if len(sent) < 30 or len(sent) > 400:
                continue
            concepts = self._find_cloze_candidates(sent)
            for concept, confidence in concepts:
                key = concept.lower()
                if key in seen:
                    continue
                cloze_text = self._create_cloze(sent, concept)
                if not cloze_text:
                    continue
                seen.add(key)
                candidates.append({
                    "strategy": "s4_cloze",
                    "concept": concept,
                    "definition": "",
                    "real_world_scenario": "",
                    "case_study_cloze": cloze_text,
                    "related_concepts": [],
                    "page_ref": page_num,
                    "confidence": confidence,
                })
        return candidates

    def _find_cloze_candidates(self, sentence):
        candidates = []
        concepts = re.findall(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,4})", sentence)
        for c in concepts:
            if len(c) < 4 or len(c) > 50:
                continue
            if re.search(r"(?:Chapter|Figure|Table|Section)\s+\d", c):
                continue
            if c.endswith((".", "!", "?")):
                c = c[:-1]
            if c:
                candidates.append((c, 0.7))
        phrases = re.findall(r"(?:the|a|an)\s+([a-z][a-z\s\-]{3,40}?(?:theory|effect|bias|principle|fallacy|heuristic|paradigm|experiment|study|phenomenon|response|stimulus|behavior|learning|conditioning|reinforcement|punishment))", sentence.lower())
        for p in set(phrases):
            p = p.strip()
            if len(p) > 4:
                candidates.append((p.title(), 0.5))
        return candidates

    def _create_cloze(self, sentence, concept):
        variations = [
            concept.lower(),
            concept,
            concept.lower().rstrip("s"),
            concept.rstrip("s"),
        ]
        for var in variations:
            if var in sentence:
                cloze = sentence.replace(var, "____", 1)
                if cloze != sentence:
                    return normalize_whitespace(cloze)
        words = concept.split()
        if len(words) > 1:
            for word in words:
                if len(word) > 4 and word.lower() in sentence.lower():
                    pattern = re.compile(re.escape(word), re.IGNORECASE)
                    cloze = pattern.sub("____", sentence, 1)
                    if cloze != sentence:
                        return normalize_whitespace(cloze)
        return None
