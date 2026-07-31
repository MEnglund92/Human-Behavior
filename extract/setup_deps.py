import subprocess
import sys
import os


def run(cmd, check=True):
    print(f"  Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"  WARNING: {result.stderr.strip()[:200]}")
    return result


def check_pip_packages():
    required = [
        "pdfplumber",
        "pdf2image",
        "pytesseract",
        "pillow",
        "spacy",
        "deep-translator",
        "camelot-py[cv]",
        "langdetect",
        "PyPDF2",
        "pdfminer.six",
    ]
    print("\n[1/4] Installing pip packages...")
    for pkg in required:
        run(f"{sys.executable} -m pip install -q {pkg}", check=False)


def check_spacy_models():
    models = [
        ("en_core_web_sm", "English"),
        ("sv_core_news_sm", "Swedish"),
    ]
    print("\n[2/4] Checking spaCy models...")
    for model, label in models:
        r = run(f"{sys.executable} -m spacy info {model}", check=False)
        if r.returncode != 0:
            print(f"  Downloading {label} model ({model})...")
            run(f"{sys.executable} -m spacy download {model}", check=False)
        else:
            print(f"  {label} model ({model}) - OK")


def check_tesseract():
    print("\n[3/4] Checking Tesseract OCR...")
    r = run("tesseract --version 2>&1", check=False)
    if r.returncode == 0:
        print(f"  Tesseract found: {r.stdout.split(chr(10))[0][:80]}")
    else:
        print("  Tesseract NOT FOUND in PATH.")
        print("  Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Install with English + Swedish language packs.")
        print("  Then add to PATH or set tesseract_path in config.json")

    r2 = run("tesseract --list-langs 2>&1", check=False)
    if r2.returncode == 0:
        langs = [l.strip() for l in r2.stdout.split("\n") if l.strip() and not l.startswith("List")]
        print(f"  Languages: {langs}")
        if "swe" not in langs:
            print("  WARNING: Swedish language pack (swe) not found!")
    else:
        print("  Could not list languages.")


def check_ghostscript():
    print("\n[4/4] Checking Ghostscript (required by camelot-py)...")
    r = run("gswin64c --version", check=False)
    if r.returncode == 0:
        print(f"  Ghostscript found: {r.stdout.strip()[:40]}")
    else:
        r2 = run("gs --version", check=False)
        if r2.returncode == 0:
            print(f"  Ghostscript found: {r2.stdout.strip()[:40]}")
        else:
            print("  Ghostscript NOT FOUND in PATH.")
            print("  Download from: https://www.ghostscript.com/releases/gsdnld.html")
            print("  Required by camelot-py for table extraction.")


if __name__ == "__main__":
    print("=" * 60)
    print("  Extraction Pipeline - Dependency Setup")
    print("=" * 60)
    check_pip_packages()
    check_spacy_models()
    check_tesseract()
    check_ghostscript()
    print("\n" + "=" * 60)
    print("  Setup complete. Run 'python run.py' to start.")
    print("=" * 60)
