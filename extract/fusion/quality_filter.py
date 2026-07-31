import re

KNOWN_UNWANTED = [
    "copyright", "all rights reserved", "isbn", "published by",
    "printed in", "library of congress", "cataloging-in-publication",
    "www\\.", "http", "e-?mail", "phone", "fax", "tel\\b",
    "editor(s)?\\b", "director", "assistant", "publisher",
    "acknowledgments", "references", "index", "about the author",
    "cover design", "production manager",
]

REJECT_CONCEPT_PATTERNS = [
    r"handbook\s+of", r"manual(\s+for|\s+of)", r"introduction\s+to",
    r"guide\s+to", r"psychology\s+of", r"science\s+of",
    r"volume\s+\d", r"edition\b", r"vol\.?\s*\d",
    r"chapter\s+\d", r"part\s+\d", r"section\s+\d",
]

AUX_VERBS = {
    "is", "are", "was", "were", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "can", "could", "shall", "should",
    "may", "might", "must", "need", "dare", "ought",
}

PRONOUNS = {
    "i", "we", "you", "he", "she", "it", "they", "me", "us", "him", "her", "them",
    "my", "our", "your", "his", "its", "their", "mine", "yours", "hers", "theirs",
}

SUBORDINATORS = {
    "although", "because", "since", "unless", "while", "whereas",
    "however", "therefore", "thus", "furthermore", "moreover",
    "nevertheless", "nonetheless", "meanwhile", "consequently",
}

BOOK_METADATA_PATTERNS = [
    r"^\d+(?:st|nd|rd|th)\s+(?:edition|ed\.)",
    r"\(.*?(?:edition|ed\.|vol\.|volume).*?\)",
    r"(?:a\s+)?(?:social\s+)?(?:psychological\s+)?(?:approach|perspective)",
    r"published\s+by",
    r"^\s*(?:reprinted|reprint|transferred|digitally)",
    r"British\s+Library",
    r"CIP\s+data",
]

AUTHOR_NAME_PATTERN = re.compile(
    r"^[A-Z][a-z]+\s+(?:[A-Z]\.\s*)+(?:[A-Z][a-z]+)$"  
)

BOOK_TITLE_DEF_PATTERN = re.compile(
    r"^(?:A|An|The)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,4}(?:\s*[,.:]\s*(?:[A-Z][a-z]+\s*)+)?$"
)

TRUNCATED_DEF_PATTERN = re.compile(
    r"(?:the\s+problem\s+was|the\s+issue\s+is|this\s+means\s+that|it\s+is\s+a)\s*$",
    re.IGNORECASE,
)

REF_PATTERN = re.compile(
    r"\b(?:pp?\.\s*\d+|pages?\s+\d+|ch\.\s*\d+|fig\.\s*\d+|table\s+\d+)",
    re.IGNORECASE,
)

def passes(e):
    concept = e.get("concept", "").strip()
    definition = e.get("definition", "").strip()

    if len(concept) < 4 or len(concept) > 50:
        return False
    if len(definition) < 15 or len(definition) > 800:
        return False

    concept_lower = concept.lower()
    def_lower = definition.lower()

    for pat in KNOWN_UNWANTED:
        if re.search(pat, concept_lower):
            return False
        if re.search(pat, def_lower):
            return False

    for pat in REJECT_CONCEPT_PATTERNS:
        if re.search(pat, concept_lower):
            return False

    if re.search(r"(?:ISBN|DOI|pages?\s+\d)", def_lower, re.I):
        return False
    if re.search(r"\d{3,}[-–]\d{3,}", concept):
        return False
    if re.search(r"^(?:Copyright|ISBN|Printed|Published|Acknowledg)", definition, re.I):
        return False
    for pat in BOOK_METADATA_PATTERNS:
        if re.search(pat, def_lower, re.I):
            return False
    if AUTHOR_NAME_PATTERN.match(definition):
        return False
    if REF_PATTERN.search(def_lower):
        return False
    if TRUNCATED_DEF_PATTERN.search(def_lower):
        return False

    if not concept[0].isupper():
        return False

    if re.match(r"^(Chapter|Figure|Table|Section|Part|Appendix|Preface|Foreword)\s", concept):
        return False

    if re.match(r"^\d", concept):
        return False

    if not re.match(r"^[A-Za-z]", concept):
        return False

    if concept[-1] in (",", ".", ";", ":", "-", "(", "["):
        return False

    if concept == concept.upper() and len(concept.split()) > 4:
        return False

    c_words = concept_lower.split()
    if c_words[0] in PRONOUNS:
        return False

    if c_words[0] in ("a", "an", "the") and len(c_words) > 2:
        if c_words[1] in PRONOUNS:
            return False
        the_x_of_y = re.match(r"^the\s+(?:\w+)\s+of\s", concept_lower)
        if the_x_of_y:
            return False

    verb_overlap = AUX_VERBS & set(c_words)
    if verb_overlap:
        return False

    subordinator_overlap = SUBORDINATORS & set(c_words)
    if subordinator_overlap:
        return False

    if re.search(r"[\"']", concept):
        return False

    if re.search(r"[„“”‚‘’]", concept):
        return False

    content_words = [w for w in c_words if len(w) > 2 and w not in ("the", "this", "that", "these", "those", "a", "an")]
    if len(content_words) < 1:
        return False

    d_words = definition.split()
    if len(d_words) < 4:
        return False

    if re.search(r"\d{4}\)", definition):
        return False

    if BOOK_TITLE_DEF_PATTERN.match(definition.strip()):
        return False

    first_def_word = d_words[0] if d_words else ""
    first_def_lower = first_def_word.lower()
    if first_def_lower in ("the", "this", "that", "these", "those", "a", "an", "its", "our", "my", "your", "his", "her", "to"):
        pass
    elif first_def_word[0].isupper() if first_def_word else True:
        pass
    else:
        return False

    return True

def filter_entries(entries):
    return [e for e in entries if passes(e)]
