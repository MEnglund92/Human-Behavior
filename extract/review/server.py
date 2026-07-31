import os
import json
import http.server
import socketserver
import webbrowser
import threading
import time
from urllib.parse import urlparse, unquote

from extract.config import OUTPUT_DIR


PORT = 8080
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class ReviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/entries":
            self._serve_entries()
        elif parsed.path == "/api/entry":
            self._serve_entry(unquote(parsed.query))
        elif parsed.path == "/api/stats":
            self._serve_stats()
        elif parsed.path == "/api/export":
            self._serve_export(unquote(parsed.query))
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        parsed = urlparse(self.path)
        if parsed.path == "/api/approve":
            self._handle_approve(json.loads(body))
        elif parsed.path == "/api/reject":
            self._handle_reject(json.loads(body))
        elif parsed.path == "/api/update":
            self._handle_update(json.loads(body))
        elif parsed.path == "/api/export-approved":
            self._handle_export_approved(json.loads(body))
        else:
            self._send_json({"error": "unknown endpoint"}, 404)

    def _serve_entries(self):
        entries = self._load_all_entries()
        self._send_json({"entries": entries, "count": len(entries)})

    def _serve_entry(self, entry_id):
        entries = self._load_all_entries()
        for e in entries:
            if e.get("_id") == entry_id or e.get("concept") == entry_id:
                self._send_json(e)
                return
        self._send_json({"error": "not found"}, 404)

    def _serve_stats(self):
        entries = self._load_all_entries()
        stats = {"total": len(entries), "auto_accepted": 0, "flag_yellow": 0, "flag_red": 0, "reviewed": 0}
        for e in entries:
            vote = e.get("_vote", "flag_red")
            if vote in stats:
                stats[vote] += 1
            if e.get("_reviewed"):
                stats["reviewed"] += 1
        self._send_json(stats)

    def _serve_export(self, vote_filter):
        entries = self._load_all_entries()
        if vote_filter:
            entries = [e for e in entries if e.get("_vote") == vote_filter]
        self._send_json({"entries": entries, "count": len(entries)})

    def _handle_approve(self, data):
        entry_id = data.get("_id", data.get("concept"))
        entries = self._load_all_entries()
        for e in entries:
            if e.get("_id") == entry_id or e.get("concept") == entry_id:
                e["_vote"] = "auto_accepted"
                e["_reviewed"] = True
                self._save_entries(entries)
                self._send_json({"success": True})
                return
        self._send_json({"error": "not found"}, 404)

    def _handle_reject(self, data):
        entry_id = data.get("_id", data.get("concept"))
        entries = self._load_all_entries()
        for e in entries:
            if e.get("_id") == entry_id or e.get("concept") == entry_id:
                e["_vote"] = "rejected"
                e["_reviewed"] = True
                self._save_entries(entries)
                self._send_json({"success": True})
                return
        self._send_json({"error": "not found"}, 404)

    def _handle_update(self, data):
        entry_id = data.get("_id", data.get("concept"))
        entries = self._load_all_entries()
        for e in entries:
            if e.get("_id") == entry_id or e.get("concept") == entry_id:
                for key in ["concept", "definition", "real_world_scenario", "case_study_cloze", "category"]:
                    if key in data:
                        e[key] = data[key]
                if "sv" in data:
                    if "sv" not in e:
                        e["sv"] = {}
                    for skey in ["concept", "definition", "real_world_scenario", "case_study_cloze"]:
                        if skey in data["sv"]:
                            e["sv"][skey] = data["sv"][skey]
                e["_reviewed"] = True
                self._save_entries(entries)
                self._send_json({"success": True})
                return
        self._send_json({"error": "not found"}, 404)

    def _handle_export_approved(self, data):
        approved = [e for e in self._load_all_entries() if e.get("_vote") == "auto_accepted"]
        export_path = os.path.join(OUTPUT_DIR, "_approved_for_merge.json")
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump({"entries": approved, "count": len(approved)}, f, indent=2, ensure_ascii=False)
        self._send_json({"success": True, "path": export_path, "count": len(approved)})

    def _load_all_entries(self):
        all_entries = []
        for fname in sorted(os.listdir(OUTPUT_DIR)):
            if fname.startswith("_") or not fname.endswith(".json"):
                continue
            try:
                with open(os.path.join(OUTPUT_DIR, fname), "r", encoding="utf-8") as f:
                    data = json.load(f)
                entries = data.get("entries", [])
                for e in entries:
                    if "_id" not in e:
                        e["_id"] = f"{e.get('source_file', 'unknown')}_{e.get('concept', 'unknown')}"
                    if "_vote" not in e:
                        e["_vote"] = "flag_yellow"
                    if "_reviewed" not in e:
                        e["_reviewed"] = False
                    e["_source_file"] = fname
                all_entries.extend(entries)
            except Exception:
                pass
        return all_entries

    def _save_entries(self, entries):
        by_file = {}
        for e in entries:
            source = e.get("_source_file", "unknown.json")
            if source not in by_file:
                by_file[source] = []
            by_file[source].append(e)
        for fname, file_entries in by_file.items():
            fpath = os.path.join(OUTPUT_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                existing["entries"] = file_entries
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump(existing, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))


def start_review_server(open_browser=True):
    handler = ReviewHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Review UI: http://localhost:{PORT}")
        if open_browser:
            threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == "__main__":
    start_review_server()
