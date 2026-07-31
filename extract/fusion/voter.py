import os
import json
from datetime import datetime
from extract.config import CONFIG


class Voter:
    def __init__(self):
        thresholds = CONFIG.get("confidence_thresholds", {})
        self.auto_accept = thresholds.get("auto_accept", 0.85)
        self.flag_yellow = thresholds.get("flag_yellow", 0.50)
        self.flag_red = thresholds.get("flag_red", 0.0)

    def classify(self, candidates):
        classified = {
            "auto_accepted": [],
            "flag_yellow": [],
            "flag_red": [],
        }
        for c in candidates:
            confidence = c.get("confidence", 0)
            if confidence >= self.auto_accept:
                c["vote"] = "auto_accept"
                classified["auto_accepted"].append(c)
            elif confidence >= self.flag_yellow:
                c["vote"] = "flag_yellow"
                classified["flag_yellow"].append(c)
            else:
                c["vote"] = "flag_red"
                classified["flag_red"].append(c)
        return classified

    def summary_report(self, session, output_dir):
        report = {
            "session": session,
            "summary": {
                "total_pdfs": session.get("pdfs_processed", 0),
                "total_candidates": session.get("total_candidates", 0),
                "auto_accepted": session.get("auto_accepted", 0),
                "flagged_review": session.get("flagged_review", 0),
                "errors": len(session.get("errors", [])),
            },
        }
        report_path = os.path.join(output_dir, "_pipeline_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nPipeline report saved to: {report_path}")
        return report
