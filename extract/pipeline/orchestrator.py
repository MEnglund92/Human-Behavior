import os
import json
import time
from datetime import datetime

from extract.config import CONFIG, OUTPUT_DIR, CACHE_DIR, DATA_JS_PATH, SOURCE_DIRS, PENDING_RENAME_DIR
from extract.utils.pdf_path_handler import get_all_pdf_paths, handle_problem_pdfs, suggest_rename_commands
from extract.utils.config_validator import validate_all
from extract.engines.text_engine import TextEngine
from extract.engines.ocr_engine import OCREngine
from extract.engines.hybrid_engine import HybridEngine
from extract.engines.table_engine import TableEngine
from extract.pipeline.classifier import PageClassifier
from extract.strategies.s1_regex_definitions import RegexDefinitionExtractor
from extract.strategies.s2_nlp_concepts import NLPConceptExtractor
from extract.strategies.s3_examples import ExampleExtractor
from extract.strategies.s4_cloze import ClozeGenerator
from extract.strategies.s5_glossary import GlossaryExtractor
from extract.strategies.s6_tables import TableExtractor
from extract.strategies.s7_crossref import CrossReferenceMapper
from extract.strategies.s8_dictionary import DictionaryExtractor
from extract.fusion.scorer import ConfidenceScorer
from extract.fusion.deduplicator import Deduplicator
from extract.fusion.voter import Voter
from extract.fusion.quality_filter import filter_entries
from extract.translation.deepl_client import DeepLClient
from extract.translation.alignment import AlignmentEngine
from extract.output.json_writer import JSONWriter
from extract.output.merger import DataMerger


class ExtractionPipeline:
    def __init__(self, skip_validation=False):
        if not skip_validation:
            validate_all()
        self.classifier = PageClassifier()
        self.text_engine = TextEngine()
        self.ocr_engine = OCREngine()
        self.hybrid_engine = HybridEngine(self.text_engine, self.ocr_engine)
        self.table_engine = TableEngine()
        self.strategies = [
            RegexDefinitionExtractor(),
            NLPConceptExtractor(),
            GlossaryExtractor(),
            TableExtractor(),
            CrossReferenceMapper(),
            DictionaryExtractor(),
        ]
        self.scorer = ConfidenceScorer()
        self.deduplicator = Deduplicator()
        self.voter = Voter()
        self.translator = DeepLClient()
        self.aligner = AlignmentEngine()
        self.writer = JSONWriter()
        self.merger = DataMerger()
        self.session = {
            "start_time": datetime.now().isoformat(),
            "pdfs_processed": 0,
            "total_candidates": 0,
            "auto_accepted": 0,
            "flagged_review": 0,
            "errors": [],
        }

    def run(self, pdf_subset=None, max_pages=None):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(CACHE_DIR, exist_ok=True)
        problems = handle_problem_pdfs(SOURCE_DIRS, PENDING_RENAME_DIR)
        if problems:
            suggest_rename_commands(problems)
        all_pdfs = get_all_pdf_paths(SOURCE_DIRS, PENDING_RENAME_DIR)
        if pdf_subset:
            all_pdfs = [p for p in all_pdfs if any(s in os.path.basename(p) for s in pdf_subset)]
        print(f"\nPipeline starting — {len(all_pdfs)} PDFs to process\n")
        all_entries = []
        for idx, pdf_path in enumerate(all_pdfs):
            fname = os.path.basename(pdf_path)
            print(f"[{idx+1}/{len(all_pdfs)}] Processing: {fname[:60]}...")
            try:
                entries = self._process_single_pdf(pdf_path, max_pages)
                all_entries.extend(entries)
                self.session["pdfs_processed"] += 1
                print(f"  -> {len(entries)} entries extracted")
            except Exception as e:
                self.session["errors"].append({"pdf": fname, "error": str(e)})
                print(f"  ERROR: {e}")
        if all_entries:
            merged = self.merger.merge(all_entries)
            self.writer.write(merged, OUTPUT_DIR)
            self.voter.summary_report(self.session, OUTPUT_DIR)
        print(f"\nPipeline complete. {self.session['pdfs_processed']}/{len(all_pdfs)} PDFs processed.")
        print(f"Total entries: {len(all_entries)}")
        return all_entries

    def _process_single_pdf(self, pdf_path, max_pages=None):
        fname = os.path.basename(pdf_path)
        cache_dir = os.path.join(CACHE_DIR, "extractions")
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, fname + ".cache.json")
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        raw_pages = self.hybrid_engine.extract(pdf_path)
        if not raw_pages:
            return []
        if max_pages:
            raw_pages = raw_pages[:max_pages]
        raw_pages = [p for p in raw_pages if p.get("page_num", 0) > 3]
        if not raw_pages:
            return []
        pages_text = [p.get("text", "") for p in raw_pages]
        pages_images = [p.get("num_images", 0) for p in raw_pages]
        classification = self.classifier.classify(pdf_path, pages_text, pages_images)
        all_candidates = []
        for strategy in self.strategies:
            try:
                candidates = strategy.extract(pdf_path, raw_pages, classification)
                all_candidates.extend(candidates)
            except Exception as e:
                print(f"    Strategy {strategy.__class__.__name__} error: {e}")
        filtered = filter_entries(all_candidates)
        if len(filtered) < len(all_candidates):
            print(f"    Quality filter removed {len(all_candidates) - len(filtered)} candidates")
        scored = self.scorer.score(filtered)
        deduped = self.deduplicator.deduplicate(scored)
        voted = self.voter.classify(deduped)
        translated = self.translator.translate_batch(voted)
        aligned = self.aligner.align(translated)
        for entry in aligned:
            entry["source_file"] = fname
        # Cache result
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(aligned, f, indent=2, ensure_ascii=False)
        return aligned
