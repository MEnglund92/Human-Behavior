import re


def detect_columns(page_text, page_width=612, page_height=792):
    lines = page_text.split("\n")
    if len(lines) < 5:
        return 1
    x_positions = []
    for line in lines[:50]:
        stripped = line.strip()
        if stripped:
            indent = len(line) - len(line.lstrip())
            x_positions.append(indent)
    if not x_positions:
        return 1
    avg_indent = sum(x_positions) / len(x_positions)
    gaps = 0
    for i in range(1, len(x_positions)):
        if abs(x_positions[i] - x_positions[i - 1]) > 20:
            gaps += 1
    if gaps > len(x_positions) * 0.3 and avg_indent > 10:
        return 2
    return 1


def detect_headers(page_text):
    lines = page_text.strip().split("\n")
    candidates = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        is_upper = stripped.isupper() and len(stripped) > 3
        is_title = stripped.istitle() and len(stripped) < 80
        is_short = len(stripped.split()) <= 6 and len(stripped) > 3
        if (is_upper or is_title) and is_short:
            candidates.append({
                "text": stripped,
                "line": i,
                "is_upper": is_upper,
            })
    return candidates


def detect_footers(page_text):
    lines = page_text.strip().split("\n")
    footers = []
    for line in lines[-5:]:
        stripped = line.strip()
        if re.match(r"^\d+$", stripped):
            footers.append({"type": "page_num", "text": stripped})
        elif re.match(r"^[A-Z\s-]+$", stripped) and len(stripped) < 60:
            footers.append({"type": "chapter", "text": stripped})
    return footers


def strip_headers_footers(page_text):
    lines = page_text.split("\n")
    if len(lines) < 5:
        return page_text
    candidates = detect_headers(page_text)
    for c in candidates:
        if c["line"] < 3:
            lines[c["line"]] = ""
    footer_indices = []
    for i in range(max(0, len(lines) - 5), len(lines)):
        stripped = lines[i].strip()
        if re.match(r"^\d+$", stripped):
            footer_indices.append(i)
        elif re.match(r"^[A-Z\s-]{5,}$", stripped) and len(stripped) < 80:
            footer_indices.append(i)
    for i in footer_indices:
        lines[i] = ""
    return "\n".join(line for line in lines if line.strip() or line == "")
