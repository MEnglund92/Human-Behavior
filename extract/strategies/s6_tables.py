from extract.engines.table_engine import TableEngine


class TableExtractor:
    def __init__(self):
        self.table_engine = TableEngine()

    def extract(self, pdf_path, pages, classification):
        candidates = []
        tables = self.table_engine.extract_tables(pdf_path, page_classifications=classification)
        for table in tables:
            rows = table.get("rows", [])
            page_num = table.get("page", 0)
            if not rows or len(rows) < 2:
                continue
            headers = rows[0]
            if self._is_glossary_table(headers):
                for row in rows[1:]:
                    if len(row) >= 2:
                        concept = self._clean_cell(row[0])
                        definition = self._clean_cell(row[1])
                        if concept and definition and len(concept) > 2:
                            candidates.append({
                                "strategy": "s6_tables",
                                "concept": concept,
                                "definition": definition,
                                "real_world_scenario": "",
                                "case_study_cloze": "",
                                "related_concepts": [],
                                "page_ref": page_num,
                                "confidence": 0.90,
                            })
            else:
                table_candidates = self._parse_table_for_concepts(rows, page_num)
                candidates.extend(table_candidates)
        return candidates

    def _is_glossary_table(self, headers):
        header_lower = " ".join(h.lower() for h in headers if h)
        keywords = ["term", "definition", "concept", "meaning", "description", "word"]
        return any(k in header_lower for k in keywords)

    def _parse_table_for_concepts(self, rows, page_num):
        candidates = []
        for row in rows[1:]:
            cells = [self._clean_cell(c) for c in row]
            cells = [c for c in cells if c]
            if len(cells) < 2:
                continue
            for i in range(len(cells) - 1):
                if cells[i][0].isupper() and len(cells[i]) > 2 and len(cells[i]) < 50:
                    concept = cells[i]
                    definition = cells[i + 1]
                    if len(definition) > 10:
                        candidates.append({
                            "strategy": "s6_tables",
                            "concept": concept,
                            "definition": definition,
                            "real_world_scenario": "",
                            "case_study_cloze": "",
                            "related_concepts": [],
                            "page_ref": page_num,
                            "confidence": 0.80,
                        })
                        break
        return candidates

    def _clean_cell(self, cell):
        if not cell:
            return ""
        cleaned = cell.strip()
        cleaned = cleaned.replace("\n", " ")
        cleaned = " ".join(cleaned.split())
        return cleaned
