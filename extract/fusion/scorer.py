from extract.config import CONFIG


class ConfidenceScorer:
    STRATEGY_TRUST = {
        "s1_regex": 0.90,
        "s2_nlp": 0.80,
        "s3_examples": 0.70,
        "s4_cloze": 0.60,
        "s5_glossary": 0.60,
        "s6_tables": 0.85,
        "s7_crossref": 0.80,
    }

    def __init__(self):
        cfg_weights = CONFIG.get("strategy_weights", {})
        for key, val in cfg_weights.items():
            self.STRATEGY_TRUST[key] = val

    CONCEPT_KEYWORDS = [
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
        "proximity", "posture", "mirroring", "synchrony", "turn-taking",
        "territory", "zone", "distance", "touch", "eye contact", "gaze",
        "smile", "facial", "handshake", "foot", "leg", "arm", "hand",
        "habit", "reflex", "drive", "motive", "goal", "reward",
        "punishment", "avoidance", "escape", "approach", "inhibition",
        "activation", "arousal", "stress", "coping", "defense",
    ]

    LOWERCASE_VERBS = {
        "is", "are", "was", "were", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "can", "could", "shall", "should",
        "may", "might", "must",
    }

    BAD_CONCEPT_PATTERNS = [
        r"^(?:a|an|the)\s+(?:behavior|action|response|signal|gesture|emotion|expression)",
        r"^(?:most\s+of|some\s+of|all\s+of|many\s+of)",
        r"\b(?:study|analysis|investigation|research|survey|review)\s+of\b",
        r"\b(?:role|impact|effect|influence)\s+of\b",
    ]

    STOPWORDS = {
        "the", "this", "that", "these", "those", "it", "they", "we", "a", "an",
        "there", "here", "what", "which", "who", "whom", "whose",
        "when", "where", "why", "how", "all", "some", "any", "many", "much",
        "more", "most", "few", "several", "each", "every", "both", "no", "none",
        "not", "only", "just", "also", "very", "too", "so", "such", "same",
        "people", "person", "thing", "things", "way", "ways", "time", "times",
        "one", "two", "three", "other", "another", "others",
    }

    def score(self, candidates):
        scored = []
        for c in candidates:
            strategy = c.get("strategy", "")
            base_confidence = c.get("confidence", 0.5)
            trust = self.STRATEGY_TRUST.get(strategy, 0.5)
            final_confidence = base_confidence * trust
            has_definition = bool(c.get("definition", "").strip())
            has_scenario = bool(c.get("real_world_scenario", "").strip())
            has_cloze = bool(c.get("case_study_cloze", "").strip())
            if not has_definition:
                final_confidence -= 0.15
            if has_definition:
                final_confidence += 0.05
            if has_scenario:
                final_confidence += 0.03
            if has_cloze:
                final_confidence += 0.02
            concept_text = c.get("concept", "").strip()
            concept_lower = concept_text.lower()
            concept_len = len(concept_lower)

            if concept_lower in self.STOPWORDS:
                final_confidence -= 0.3

            keyword_match = any(kw in concept_lower for kw in self.CONCEPT_KEYWORDS) or any(
                kw in c.get("definition", "").lower() for kw in self.CONCEPT_KEYWORDS
            )
            if keyword_match:
                final_confidence += 0.05

            if 8 <= concept_len <= 40:
                final_confidence += 0.02
            else:
                final_confidence -= 0.05

            if concept_lower and concept_lower[0] not in "abcdefghijklmnopqrstuvwxyz":
                pass
            elif concept_lower and concept_lower[0].islower() and len(concept_lower) > 3:
                final_confidence -= 0.15

            concept_words_set = set(concept_lower.split())
            if self.LOWERCASE_VERBS & concept_words_set:
                final_confidence -= 0.25

            import re
            for pat in self.BAD_CONCEPT_PATTERNS:
                if re.search(pat, concept_lower):
                    final_confidence -= 0.15
                    break

            if concept_text.startswith(tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")):
                final_confidence += 0.02

            content_words = [w for w in concept_lower.split() if len(w) > 2
                            and w not in {"the", "this", "that", "these", "those", "a", "an"}]
            if len(content_words) < 2:
                final_confidence -= 0.1

            def_text = c.get("definition", "").strip()
            if def_text:
                def_len = len(def_text)
                if 30 <= def_len <= 200:
                    final_confidence += 0.05
                if def_text[-1] in (".", "!", "?"):
                    final_confidence += 0.02

                def_words = def_text.lower().split()
                if len(def_words) < 6:
                    final_confidence -= 0.1

                def_first = def_words[0] if def_words else ""
                if def_first in ("a", "an", "the") and keyword_match:
                    final_confidence += 0.03
            final_confidence = max(0.0, min(1.0, final_confidence))
            c["confidence"] = round(final_confidence, 3)
            c["score_breakdown"] = {
                "base": round(base_confidence, 3),
                "trust": trust,
                "has_definition": has_definition,
                "has_scenario": has_scenario,
                "has_cloze": has_cloze,
            }
            scored.append(c)
        return scored
