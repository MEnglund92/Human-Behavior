from extract.engines.text_engine import TextEngine
from extract.engines.ocr_engine import OCREngine
from extract.utils.pdf_path_handler import is_path_accessible


class HybridEngine:
    def __init__(self, text_engine=None, ocr_engine=None):
        self.text_engine = text_engine or TextEngine()
        self.ocr_engine = ocr_engine or OCREngine()

    def extract(self, pdf_path):
        if not is_path_accessible(pdf_path):
            raise IOError(f"Cannot access PDF: {pdf_path}")

        text_pages = []
        try:
            text_pages = self.text_engine.extract(pdf_path)
        except Exception as e:
            print(f"    Text engine failed, falling back to full OCR: {e}")
            return self.ocr_engine.extract(pdf_path)

        if not text_pages:
            return self.ocr_engine.extract(pdf_path)

        total_chars = sum(len(p["text"]) for p in text_pages)
        if total_chars < 50:
            return self.ocr_engine.extract(pdf_path)

        avg_chars = total_chars / len(text_pages) if text_pages else 0
        if avg_chars < 20:
            return self.ocr_engine.extract(pdf_path)

        # Per-page hybrid: OCR low-text pages individually
        ocr_pages = []
        ocr_needed = 0
        for i, page in enumerate(text_pages):
            if len(page["text"].strip()) < 30:
                ocr_needed += 1
                try:
                    ocr_text = self.ocr_engine.extract_page(pdf_path, page["page_num"])
                    page["text"] = ocr_text
                    page["ocr_fallback"] = True
                except Exception:
                    page["ocr_fallback"] = False
            else:
                page["ocr_fallback"] = False

        if ocr_needed > len(text_pages) * 0.8:
            return self.ocr_engine.extract(pdf_path)

        return text_pages
