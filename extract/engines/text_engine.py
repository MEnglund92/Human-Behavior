import pdfplumber
from extract.utils.text_cleaner import clean_text, normalize_whitespace
from extract.utils.layout_analyzer import strip_headers_footers


class TextEngine:
    def extract(self, pdf_path):
        pages = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text() or ""
                    page_text = strip_headers_footers(page_text)
                    page_text = clean_text(page_text)
                    words = page.extract_words()
                    num_images = len(page.images) if page.images else 0
                    tables = page.extract_tables()
                    pages.append({
                        "page_num": i + 1,
                        "text": page_text,
                        "words": words,
                        "num_images": num_images,
                        "tables": tables,
                        "width": page.width,
                        "height": page.height,
                    })
        except Exception as e:
            print(f"    pdfplumber failed on {pdf_path}, trying PyPDF2...")
            pages = self._fallback_extract(pdf_path)
        return pages

    def _fallback_extract(self, pdf_path):
        from PyPDF2 import PdfReader
        pages = []
        try:
            reader = PdfReader(pdf_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                text = clean_text(text)
                pages.append({
                    "page_num": i + 1,
                    "text": text,
                    "words": [],
                    "num_images": 0,
                    "tables": [],
                    "width": 612,
                    "height": 792,
                })
        except Exception as e2:
            raise RuntimeError(f"All text engines failed on {pdf_path}: {e2}")
        return pages

    def extract_page_text_only(self, pdf_path, page_num):
        pages = self.extract(pdf_path)
        for p in pages:
            if p["page_num"] == page_num:
                return p["text"]
        return ""

    def extract_raw(self, pdf_path):
        results = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    results.append(page.extract_text() or "")
        except Exception:
            reader = PdfReader(pdf_path)
            results = [p.extract_text() or "" for p in reader.pages]
        return results
