import os
import tempfile
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from pdf2image import convert_from_path
import pytesseract

from extract.config import CONFIG
from extract.utils.text_cleaner import clean_text


class OCREngine:
    def __init__(self):
        tesseract_path = CONFIG.get("tesseract_path", "")
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.dpi = CONFIG.get("ocr_dpi", 300)

    def extract(self, pdf_path):
        pages = []
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt="png",
                thread_count=2,
            )
            for i, img in enumerate(images):
                processed = self._preprocess_image(img)
                text = pytesseract.image_to_string(
                    processed,
                    lang="eng+swe",
                    config="--oem 3 --psm 6"
                )
                text = clean_text(text)
                pages.append({
                    "page_num": i + 1,
                    "text": text,
                    "num_images": 1,
                    "image": processed,
                })
        except Exception as e:
            print(f"    OCR engine unavailable: {e}")
            return []
        return pages

    def extract_page(self, pdf_path, page_num):
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=page_num,
                last_page=page_num,
                fmt="png",
            )
            if images:
                processed = self._preprocess_image(images[0])
                text = pytesseract.image_to_string(
                    processed,
                    lang="eng+swe",
                    config="--oem 3 --psm 6"
                )
                return clean_text(text)
        except Exception:
            return ""
        return ""

    def _preprocess_image(self, img):
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = ImageOps.grayscale(img)
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = ImageEnhance.Sharpness(img).enhance(2.0)
        img = img.filter(ImageFilter.MedianFilter(size=3))
        img = ImageOps.autocontrast(img, cutoff=5)
        img = img.point(lambda x: 0 if x < 140 else 255 if x > 200 else x)
        return img

    def extract_text_from_image(self, image):
        processed = self._preprocess_image(image)
        text = pytesseract.image_to_string(
            processed,
            lang="eng+swe",
            config="--oem 3 --psm 6"
        )
        return clean_text(text)
