import re
from difflib import SequenceMatcher


class AlignmentEngine:
    def align(self, classified):
        all_entries = []
        for key in ["auto_accepted", "flag_yellow", "flag_red"]:
            entries = classified.get(key, [])
            for entry in entries:
                aligned = self._align_entry(entry)
                aligned["_vote"] = key
                all_entries.append(aligned)
        return all_entries

    def _align_entry(self, entry):
        sv = entry.get("sv", {})
        if not sv:
            sv = {
                "concept": entry.get("concept", ""),
                "definition": entry.get("definition", ""),
                "real_world_scenario": entry.get("real_world_scenario", ""),
                "case_study_cloze": entry.get("case_study_cloze", ""),
            }
        aligned = {
            "concept": entry.get("concept", ""),
            "definition": entry.get("definition", ""),
            "category": entry.get("category", "general"),
            "real_world_scenario": entry.get("real_world_scenario", ""),
            "case_study_cloze": entry.get("case_study_cloze", ""),
            "related_concepts": entry.get("related_concepts", []),
            "sv": {
                "concept": sv.get("concept", entry.get("concept", "")),
                "definition": sv.get("definition", entry.get("definition", "")),
                "real_world_scenario": sv.get("real_world_scenario", entry.get("real_world_scenario", "")),
                "case_study_cloze": sv.get("case_study_cloze", entry.get("case_study_cloze", "")),
            },
            "confidence": entry.get("confidence", 0),
            "source_file": entry.get("source_file", ""),
            "page_ref": entry.get("page_ref", 0),
            "strategy": entry.get("strategy", ""),
            "merged_strategies": entry.get("merged_strategies", []),
        }
        if not aligned["sv"]["concept"]:
            aligned["sv"]["concept"] = aligned["concept"]
        if not aligned["sv"]["definition"]:
            aligned["sv"]["definition"] = aligned["definition"]
        if not aligned["sv"]["real_world_scenario"]:
            aligned["sv"]["real_world_scenario"] = aligned["real_world_scenario"]
        if not aligned["sv"]["case_study_cloze"]:
            aligned["sv"]["case_study_cloze"] = aligned["case_study_cloze"]
        return aligned
