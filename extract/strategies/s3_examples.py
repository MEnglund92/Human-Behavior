import re
from extract.utils.text_cleaner import extract_sentences, normalize_whitespace, extract_paragraphs


class ExampleExtractor:
    EXAMPLE_SIGNALS = [
        "for example", "for instance", "such as", "e.g.", "like when",
        "consider", "imagine", "suppose", "in one study", "in a study",
        "research shows", "studies show", "research has shown",
        "in an experiment", "in a famous experiment", "in a classic study",
        "a classic example", "a well-known example", "one example",
        "another example", "to illustrate", "case in point",
        "takes the example", "consider the case", "in practice",
        "real-world example", "real world example", "everyday example",
        "think about", "picture this", "say you", "for instance, if",
    ]

    def extract(self, pdf_path, pages, classification):
        candidates = []
        for page in pages:
            text = page.get("text", "")
            page_num = page.get("page_num", 0)
            if not text:
                continue
            candidates.extend(self._extract_from_text(text, page_num))
        return candidates

    def _extract_from_text(self, text, page_num):
        candidates = []
        paragraphs = extract_paragraphs(text)
        seen = set()
        for para in paragraphs:
            para_lower = para.lower()
            signals_found = []
            for signal in self.EXAMPLE_SIGNALS:
                if signal in para_lower:
                    signals_found.append(signal)
            if not signals_found:
                continue
            concepts = self._find_concepts_in_paragraph(para)
            for concept in concepts:
                key = f"{concept}:{para[:50]}".lower()
                if key in seen:
                    continue
                seen.add(key)
                scenario = self._extract_scenario(para, concept, signals_found)
                candidates.append({
                    "strategy": "s3_examples",
                    "concept": concept,
                    "definition": "",
                    "real_world_scenario": scenario,
                    "case_study_cloze": "",
                    "related_concepts": [],
                    "page_ref": page_num,
                    "confidence": 0.6 + (len(signals_found) * 0.05),
                })
        return candidates

    def _find_concepts_in_paragraph(self, para):
        concepts = set()
        title_candidates = re.findall(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,4})", para)
        for c in title_candidates:
            if 3 < len(c) < 60 and not c.endswith((".", "!", "?")):
                if not re.search(r"(?:Chapter|Figure|Table|Section)\s+\d", c):
                    concepts.add(c.strip())
        common_terms = re.findall(r"([a-z][a-z\s\-]+?(?:bias|effect|theory|principle|fallacy|heuristic|paradigm|experiment|study|phenomenon))", para.lower())
        for t in common_terms:
            t = t.strip()
            if len(t) > 4:
                concepts.add(t.title())
        return list(concepts)[:3] if concepts else ["(unknown concept)"]

    def _extract_scenario(self, para, concept, signals):
        sentences = re.split(r"(?<=[.!?])\s+", para)
        scenario_sentences = []
        for sent in sentences:
            sent_lower = sent.lower()
            if any(s in sent_lower for s in signals):
                scenario_sentences.append(sent)
        if scenario_sentences:
            scenario = " ".join(scenario_sentences)
        else:
            scenario = para[:300]
        scenario = normalize_whitespace(scenario)
        return scenario[:500]
