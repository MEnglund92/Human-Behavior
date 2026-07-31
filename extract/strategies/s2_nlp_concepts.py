import re
import spacy
from extract.utils.text_cleaner import extract_sentences, normalize_whitespace


class NLPConceptExtractor:
    def __init__(self):
        self.nlp = None
        self._load_model()

    def _load_model(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("    WARNING: en_core_web_sm not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None

    def extract(self, pdf_path, pages, classification):
        if not self.nlp:
            return []
        candidates = []
        for page in pages:
            text = page.get("text", "")
            page_num = page.get("page_num", 0)
            if len(text.strip()) < 50:
                continue
            candidates.extend(self._extract_from_text(text, page_num))
        return candidates

    def _extract_from_text(self, text, page_num):
        candidates = []
        text_chunks = self._chunk_text(text)
        seen_concepts = set()
        for chunk in text_chunks:
            doc = self.nlp(chunk)
            for sent in doc.sents:
                sent_text = sent.text.strip()
                if not sent_text or len(sent_text) < 20:
                    continue
                concepts = self._extract_concepts(sent, sent_text)
                for concept in concepts:
                    key = concept["concept"].lower()
                    if key in seen_concepts:
                        continue
                    seen_concepts.add(key)
                    concept["page_ref"] = page_num
                    concept["strategy"] = "s2_nlp"
                    candidates.append(concept)
        return candidates

    def _chunk_text(self, text, max_chars=50000):
        chunks = []
        paragraphs = text.split("\n\n")
        current = ""
        for para in paragraphs:
            if len(current) + len(para) > max_chars:
                if current:
                    chunks.append(current)
                current = para
            else:
                current += "\n\n" + para if current else para
        if current:
            chunks.append(current)
        return chunks

    KEYWORD_BOOST = {
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
        "adaptor", "emblem", "illustrator", "regulator",
        "proximity", "posture", "mirroring", "synchrony",
        "territory", "zone", "distance", "touch",
        "smile", "facial", "handshake",
    }

    STOPWORDS = {
        "the", "this", "that", "these", "those", "it", "they", "we", "a", "an",
        "there", "here", "what", "which", "who", "whom", "whose",
        "when", "where", "why", "how", "all", "some", "any", "many", "much",
        "more", "most", "few", "several", "each", "every", "both", "no", "none",
        "not", "only", "just", "also", "very", "too", "so", "such", "same",
        "people", "person", "thing", "things", "way", "ways", "time", "times",
        "one", "two", "three", "other", "another", "others",
    }

    def _extract_concepts(self, sent, sent_text):
        results = []
        for chunk in sent.noun_chunks:
            phrase = chunk.text.strip()
            if not phrase:
                continue
            phrase_lower = phrase.lower()
            if len(phrase.split()) < 2 or len(phrase) > 50:
                continue
            if len(phrase) < 5:
                continue
            if phrase_lower in self.STOPWORDS:
                continue
            first_word = phrase_lower.split()[0]
            if first_word in self.STOPWORDS and len(phrase_lower.split()) < 4:
                continue
            if first_word in {"i", "we", "you", "he", "she", "it", "they"}:
                continue
            if not phrase[0].isupper():
                continue
            keyword_match = any(kw in phrase_lower for kw in self.KEYWORD_BOOST)
            if not keyword_match:
                continue
            definition = self._extract_copular_definition(sent, chunk.root)
            scenario = self._extract_example_context(sent, sent_text, phrase)
            confidence = 0.4
            if definition:
                confidence = max(confidence, 0.55)
            if keyword_match:
                confidence = max(confidence, 0.65)
            if definition and keyword_match:
                confidence = max(confidence, 0.70)
            if scenario and definition:
                confidence = max(confidence, 0.75)
            results.append({
                "concept": phrase,
                "definition": definition or "",
                "real_world_scenario": scenario or "",
                "case_study_cloze": "",
                "related_concepts": [],
                "confidence": confidence,
            })
        return results

    def _extract_copular_definition(self, sent, root_token):
        copula_verbs = {"is", "are", "was", "were", "refers", "means", "involves", "describes"}
        for token in sent:
            if token.lower_ in copula_verbs and token.pos_ == "VERB":
                if root_token is None:
                    continue
                is_subject = False
                for child in token.children:
                    if child == root_token and child.dep_ in ("nsubj", "nsubjpass"):
                        is_subject = True
                        break
                if not is_subject:
                    continue
                verb_text = token.text
                verb_pos = sent.text.lower().find(verb_text.lower())
                if verb_pos < 0:
                    continue
                after = sent.text[verb_pos + len(verb_text):].strip().rstrip(".;, ")
                if not after:
                    continue
                after = re.sub(r"\s+", " ", after)
                if 8 < len(after) < 300:
                    return after
        return ""

    def _extract_example_context(self, sent, sent_text, concept):
        signal_words = ["for example", "for instance", "such as", "e.g.", "like", "consider", "imagine"]
        for signal in signal_words:
            if signal in sent_text.lower():
                return sent_text
        return ""
