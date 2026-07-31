import os
import json
from datetime import datetime


class JSONWriter:
    def __init__(self):
        pass

    def write(self, entries, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        by_source = {}
        for entry in entries:
            source = entry.get("source_file", "unknown").replace(".pdf", "")
            if source not in by_source:
                by_source[source] = []
            vote = entry.get("_vote", "flag_red")
            confidence = entry.get("confidence", 0)
            entry_out = {
                "concept": entry["concept"],
                "definition": entry["definition"],
                "category": entry.get("category", "general"),
                "real_world_scenario": entry.get("real_world_scenario", ""),
                "case_study_cloze": entry.get("case_study_cloze", ""),
                "related_concepts": entry.get("related_concepts", []),
                "sv": entry.get("sv", {
                    "concept": entry["concept"],
                    "definition": entry["definition"],
                    "real_world_scenario": entry.get("real_world_scenario", ""),
                    "case_study_cloze": entry.get("case_study_cloze", ""),
                }),
                "confidence": confidence,
                "_vote": vote,
                "_metadata": {
                    "page_ref": entry.get("page_ref", 0),
                    "strategy": entry.get("strategy", ""),
                    "merged_strategies": entry.get("merged_strategies", []),
                    "source_file": entry.get("source_file", ""),
                },
            }
            by_source[source].append(entry_out)
        all_entries = []
        for source, source_entries in sorted(by_source.items()):
            fname = f"{source}_{timestamp}.json"
            fpath = os.path.join(output_dir, fname)
            output = {
                "source": source,
                "extracted_at": timestamp,
                "entry_count": len(source_entries),
                "entries": source_entries,
            }
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            all_entries.extend(source_entries)
            print(f"    Wrote {fname} ({len(source_entries)} entries)")
        combined = {
            "extracted_at": timestamp,
            "total_entries": len(all_entries),
            "entries": all_entries,
        }
        combined_path = os.path.join(output_dir, f"_all_extracted_{timestamp}.json")
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        print(f"    Combined output: {combined_path}")
        return by_source
