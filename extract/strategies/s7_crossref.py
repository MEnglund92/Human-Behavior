import os
import json
from difflib import SequenceMatcher


class CrossReferenceMapper:
    def __init__(self):
        self.cache = {}

    def extract(self, pdf_path, pages, classification):
        fname = os.path.basename(pdf_path)
        return []

    def process_all(self, all_candidates_by_pdf):
        concept_map = {}
        for pdf_name, candidates in all_candidates_by_pdf.items():
            for c in candidates:
                concept = c.get("concept", "").lower().strip()
                if not concept:
                    continue
                if concept not in concept_map:
                    concept_map[concept] = []
                concept_map[concept].append({
                    "pdf": pdf_name,
                    "candidate": c,
                })
        results = []
        seen_pairs = set()
        concepts = list(concept_map.keys())
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                similarity = SequenceMatcher(None, concepts[i], concepts[j]).ratio()
                if similarity > 0.85:
                    pair = (min(concepts[i], concepts[j]), max(concepts[i], concepts[j]))
                    if pair not in seen_pairs:
                        seen_pairs.add(pair)
                        merged = self._merge_candidates(
                            concept_map[concepts[i]],
                            concept_map[concepts[j]],
                            similarity,
                        )
                        if merged:
                            results.append(merged)
        return results

    def _merge_candidates(self, group_a, group_b, similarity):
        all_candidates = group_a + group_b
        if not all_candidates:
            return None
        best = max(all_candidates, key=lambda x: x["candidate"].get("confidence", 0))
        merged = {
            "strategy": "s7_crossref",
            "concept": best["candidate"]["concept"],
            "definition": best["candidate"].get("definition", ""),
            "real_world_scenario": best["candidate"].get("real_world_scenario", ""),
            "case_study_cloze": best["candidate"].get("case_study_cloze", ""),
            "related_concepts": [],
            "page_ref": best["candidate"].get("page_ref", 0),
            "confidence": min(0.95, best["candidate"].get("confidence", 0) + 0.1 * similarity),
            "source_files": list(set(c["pdf"] for c in all_candidates)),
            "merged_from": len(all_candidates),
        }
        return merged
