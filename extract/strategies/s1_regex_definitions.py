import re
from extract.utils.text_cleaner import normalize_whitespace, extract_sentences


class RegexDefinitionExtractor:
    CONCEPT_KEYWORDS = (
        "bias", "effect", "theory", "principle", "fallacy", "heuristic",
        "paradigm", "experiment", "phenomenon", "response", "stimulus",
        "behavior", "learning", "conditioning", "reinforcement", "punishment",
        "communication", "gesture", "expression", "emotion", "signal",
        "language", "perception", "cognition", "memory", "attention",
        "personality", "intelligence", "motivation", "attitude", "belief",
        "norm", "role", "identity", "group", "influence", "persuasion",
        "compliance", "obedience", "conformity", "dissonance", "attribution",
        "stereotype", "prejudice", "discrimination", "aggression", "attachment",
        "empathy", "trust", "power", "status", "dominance", "submission",
        "deception", "lying", "truth", "leakage", "microexpression",
        "proxemics", "kinesics", "haptics", "chronemics", "paralanguage",
        "adaptor", "emblem", "illustrator", "regulator", "affect",
    )

    REJECT_CONCEPT_PATTERNS = [
        r"handbook\s+of", r"manual(\s+for|\s+of)", r"introduction\s+to",
        r"guide\s+to", r"psychology\s+of", r"science\s+of",
        r"volume\s+\d", r"edition\b", r"vol\.?\s*\d",
        r"chapter\s+\d", r"part\s+\d",
    ]

    DEFINITION_PATTERNS = [
        (r"([A-Z][a-zA-Z\s\-]{3,40}?)\s+(?:is|was|are|refers to|means|can be defined as)\s+(?:a|an|the|any)\s+(.+?)(?:\.\s|\.$|;|, and)", 0.85),
        (r"(?:the\s+)?([A-Z][a-zA-Z\s\-]{3,40}?)\s+is\s+(?:the\s+)?(?:tendency|process|act|practice|phenomenon|belief|theory|approach|method|technique|ability|capacity|field|science)\s+(?:of|to|by|in|whereby)\s+(.+?)(?:\.\s|\.$|;)", 0.85),
        (r"(?:[Tt]he\s+)?([A-Z][a-zA-Z\s\-]{3,40}?)\s+is\s+a\s+(.+?)\s+that\s+(?:is|refers|occurs|happens|involves|describes|explains|affects|influences|helps|allows|enables|causes|leads|results)\s+(.+?)(?:\.\s|\.$|;)", 0.80),
        (r"(?:term|concept|notion|phenomenon)\s+[\"']([A-Za-z][a-zA-Z\s\-]{2,40}?)[\"']\s+(?:is|refers to|means|describes)\s+(.+?)(?:\.\s|\.$|;)", 0.90),
        (r"([A-Z][a-zA-Z\s\-]{3,40}?)\s+is\s+(?:often|typically|generally|usually)\s+(?:described as|defined as|understood as|called|referred to as)\s+(.+?)(?:\.\s|\.$|;)", 0.75),
        (r"([A-Z][a-zA-Z\s\-]{3,40}?)\s*[—–-]\s*(.+?)(?:\.\s|\.$|;)", 0.60),
    ]

    SECONDARY_PATTERNS = [
        (r"([A-Z][a-zA-Z\s\-]{3,40}?)\s*[,:]?\s*(?:also known as|called|termed|denoted)\s+(.+?)(?:\.\s|\.$|;)", 0.70),
        (r"([A-Z][a-zA-Z\s\-]{3,40}?)\s*\(([A-Za-z][a-zA-Z\s\-]{2,40}?)\)\s*[-–—]\s*(.+?)(?:\.\s|\.$|;)", 0.70),
        (r"([A-Za-z][a-zA-Z\s\-]{3,40}?)\s*[,;]\s+(?:or\s+)?([A-Za-z][a-zA-Z\s\-]{2,40}?)\s*,\s+(?:is|the)\s+(.+?)(?:\.\s|\.$|;)", 0.70),
    ]

    def extract(self, pdf_path, pages, classification):
        candidates = []
        for page in pages:
            text = page.get("text", "")
            page_num = page.get("page_num", 0)
            if not text or len(text.strip()) < 30:
                continue
            candidates.extend(self._extract_from_text(text, page_num))
        return candidates

    def _extract_from_text(self, text, page_num):
        candidates = []
        text = normalize_whitespace(text)
        seen = set()

        # High-precision patterns first
        for pattern, weight in self.DEFINITION_PATTERNS:
            for match in re.finditer(pattern, text, re.MULTILINE):
                concept = match.group(1).strip()
                definition = match.group(2).strip()
                definition = re.sub(r"\s+", " ", definition)
                if not self._is_valid_concept(concept) or not self._is_good_definition(concept, definition):
                    continue
                key = concept.lower()
                if key in seen:
                    continue
                seen.add(key)
                candidates.append(self._make_candidate(concept, definition, page_num, weight, text))

        # Secondary patterns with concept keyword boost
        for pattern, weight in self.SECONDARY_PATTERNS:
            for match in re.finditer(pattern, text, re.MULTILINE):
                concept = match.group(1).strip()
                definition = match.group(2).strip() if match.lastindex and match.lastindex >= 2 else ""
                if not definition and match.lastindex >= 3:
                    definition = match.group(3).strip()
                definition = re.sub(r"\s+", " ", definition)
                if not self._is_valid_concept(concept) or not self._is_good_definition(concept, definition):
                    continue
                key = concept.lower()
                if key in seen:
                    continue
                has_keyword = any(kw in concept.lower() for kw in self.CONCEPT_KEYWORDS)
                final_weight = min(0.95, weight + 0.1) if has_keyword else weight
                seen.add(key)
                candidates.append(self._make_candidate(concept, definition, page_num, final_weight, text))

        # Final pass: glossary-style format "Concept: definition"
        for match in re.finditer(r"^([A-Z][a-zA-Z\s\-]{3,50}?)\s{3,}([A-Z][a-zA-Z].+?)(?:\.\s|\.$|;)", text, re.MULTILINE):
            concept = match.group(1).strip()
            definition = match.group(2).strip()
            definition = re.sub(r"\s+", " ", definition)
            if self._is_valid_concept(concept) and len(definition) > 15 and concept.lower() not in seen:
                if re.search(r"\d+\s*$", definition):
                    continue
                if re.search(r"\b[A-Z]\.?$", concept):
                    continue
                seen.add(concept.lower())
                candidates.append(self._make_candidate(concept, definition, page_num, 0.65, text))

        return candidates

    def _is_valid_concept(self, concept):
        words = concept.split()
        if len(words) > 6 or len(concept) < 4 or len(concept) > 50:
            return False
        stopwords = {"the", "this", "that", "these", "those", "it", "they", "we", "a", "an",
                     "there", "here", "what", "which", "who", "whom", "whose", "when", "where", "why", "how"}
        if concept.lower() in stopwords:
            return False
        if concept[0].islower():
            return False
        if re.match(r"^(Chapter|Figure|Table|Section|Part|Appendix)\s", concept):
            return False
        if re.match(r"^\d", concept):
            return False
        if not re.match(r"^[A-Za-z]", concept):
            return False
        if concept.endswith((",", ".", ";", ":", "-", "(", "[")):
            return False
        concept_lower = concept.lower()
        for pat in self.REJECT_CONCEPT_PATTERNS:
            if re.search(pat, concept_lower):
                return False
        if not any(kw in concept_lower for kw in self.CONCEPT_KEYWORDS):
            return False
        return True

    def _is_good_definition(self, concept, definition):
        if len(definition) < 15 or len(definition) > 400:
            return False
        if definition[0].islower():
            return False
        concept_words = set(concept.lower().split())
        def_words = set(definition.lower().split())
        overlap = concept_words & def_words
        if len(overlap) == len(concept_words) and len(concept_words) > 2:
            return False
        if definition.lower().startswith(concept.lower()[:10]):
            return False
        definition_lower = definition.lower()
        junk_patterns = r"(?:copyright|isbn|www\.|http|e-?mail|phone|fax|printed|reserved)"
        if re.search(junk_patterns, definition_lower):
            return False
        if re.search(r"\d{4}\)", definition):
            return False
        return True

    def _make_candidate(self, concept, definition, page_num, weight, text):
        return {
            "strategy": "s1_regex",
            "concept": concept,
            "definition": definition,
            "page_ref": page_num,
            "confidence": weight,
            "real_world_scenario": "",
            "case_study_cloze": "",
            "related_concepts": self._extract_related(text, concept),
        }

    def _extract_related(self, text, concept):
        related = set()
        sentences = extract_sentences(text)
        concept_lower = concept.lower()
        for sent in sentences:
            if concept_lower not in sent.lower():
                continue
            for match in re.finditer(r"([A-Z][a-zA-Z\s\-]+?)(?:\s*,?\s*and|\s*,?\s*or)", sent):
                candidate = match.group(1).strip()
                if candidate.lower() != concept_lower and self._is_valid_concept(candidate):
                    related.add(candidate)
        for match in re.finditer(r"(?:related\s+(?:to|concepts?)|see\s+(?:also|above|below)|similar\s+(?:to|concepts?))\s*:?\s*(.+?)(?:\.|$)", text, re.IGNORECASE):
            refs = re.findall(r"([A-Z][a-zA-Z\s\-]{3,30}?)(?:\s*,|\s+and|\s*$)", match.group(1))
            for r in refs:
                r = r.strip().rstrip(".")
                if r and r.lower() != concept_lower:
                    related.add(r)
        return list(related)[:5]
