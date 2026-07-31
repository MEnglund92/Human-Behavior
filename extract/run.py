#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.config import CONFIG, prompt_deepl_key
from extract.utils.config_validator import validate_all
from extract.pipeline.orchestrator import ExtractionPipeline
from extract.review.server import start_review_server


def main():
    parser = argparse.ArgumentParser(
        description="Advanced PDF Extraction Pipeline for Human Behavior study materials"
    )
    parser.add_argument("--setup", action="store_true",
                        help="Run dependency setup and exit")
    parser.add_argument("--validate", action="store_true",
                        help="Validate dependencies and exit")
    parser.add_argument("--review", action="store_true",
                        help="Start the review UI server")
    parser.add_argument("--pdfs", nargs="+", default=None,
                        help="Process only specific PDFs (substring match on filename)")
    parser.add_argument("--max-pages", type=int, default=None,
                        help="Max pages per PDF (for testing)")
    parser.add_argument("--skip-validation", action="store_true",
                        help="Skip dependency validation")
    parser.add_argument("--prompt-key", action="store_true",
                        help="Prompt for DeepL API key")

    args = parser.parse_args()

    if args.prompt_key:
        prompt_deepl_key()
        return

    if args.setup:
        from extract.setup_deps import check_pip_packages, check_spacy_models, check_tesseract, check_ghostscript
        print("=" * 60)
        print("  Extraction Pipeline - Dependency Setup")
        print("=" * 60)
        check_pip_packages()
        check_spacy_models()
        check_tesseract()
        check_ghostscript()
        print("\nSetup complete.")
        return

    if args.validate:
        validate_all()
        return

    if args.review:
        start_review_server()
        return

    print("-" * 52)
    print("  Human Behavior PDF -> JSON Extraction Pipeline")
    print("-" * 52)

    if not CONFIG.get("deepl_api_key"):
        print("[INFO] No DeepL API key configured. Swedish translations will be English placeholders.")
        print("      Run 'python run.py --prompt-key' to set one.\n")

    pipeline = ExtractionPipeline(skip_validation=args.skip_validation)
    results = pipeline.run(
        pdf_subset=args.pdfs,
        max_pages=args.max_pages,
    )

    print(f"\nDone. {len(results)} total entries extracted.")
    print(f"Output directory: {os.path.join(os.path.dirname(__file__), 'extracted_json')}")
    print(f"Run 'python run.py --review' to review and approve entries.\n")


if __name__ == "__main__":
    main()
