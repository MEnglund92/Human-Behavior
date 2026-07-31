import re


def clean_text(text):
    if not text:
        return ""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"(\n)\1{2,}", r"\1\1", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\u2022|\u2023|\u25E6|\u2043|\u2219", "-", text)
    text = re.sub(r"\u2018|\u2019|\u201A|\u201B", "'", text)
    text = re.sub(r"\u201C|\u201D|\u201E|\u201F", '"', text)
    text = re.sub(r"\u2013|\u2014", "-", text)
    text = re.sub(r"\u00A0", " ", text)
    text = re.sub(r"\uf0b7|\uf0d8|\uf0a7|\uf0a8", "", text)
    text = re.sub(r"[^\x00-\x7F]+", lambda m: _clean_non_ascii(m.group(0)), text)
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned.append(line)
    return "\n".join(cleaned)


def _clean_non_ascii(s):
    common = {
        "\u00e4": "a", "\u00c4": "A", "\u00e5": "a", "\u00c5": "A",
        "\u00f6": "o", "\u00d6": "O", "\u00e9": "e", "\u00c9": "E",
        "\u00e8": "e", "\u00e0": "a", "\u00fc": "u", "\u00dc": "U",
        "\u00f1": "n", "\u00d1": "N",
    }
    result = []
    for ch in s:
        if ch in common:
            result.append(common[ch])
        elif ord(ch) >= 0x2000 and ord(ch) <= 0x206F:
            result.append(" ")
        else:
            result.append(" ")
    return "".join(result)


def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_sentences(text):
    text = normalize_whitespace(text)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def extract_paragraphs(text):
    blocks = re.split(r"\n\s*\n", text)
    return [b.strip() for b in blocks if len(b.strip()) > 20]
