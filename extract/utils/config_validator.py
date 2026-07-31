import importlib
import subprocess
import sys
import shutil


def check_module(name, pip_name=None):
    try:
        importlib.import_module(name)
        return True, None
    except ImportError as e:
        return False, str(e)


def check_spacy_model(model_name):
    r = subprocess.run(
        [sys.executable, "-m", "spacy", "info", model_name],
        capture_output=True, text=True
    )
    return r.returncode == 0, r.stderr[:100] if r.returncode != 0 else None


def check_tesseract():
    path = shutil.which("tesseract")
    if path:
        r = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        return True, r.stdout.split("\n")[0] if r.returncode == 0 else path
    return False, None


def check_ghostscript():
    for cmd in ["gswin64c", "gswin32c", "gs"]:
        path = shutil.which(cmd)
        if path:
            r = subprocess.run([cmd, "--version"], capture_output=True, text=True)
            if r.returncode == 0:
                return True, r.stdout.strip()
    return False, None


def validate_all():
    checks = {
        "pdfplumber": check_module("pdfplumber"),
        "pdf2image": check_module("pdf2image"),
        "pytesseract": check_module("pytesseract"),
        "PIL": check_module("PIL"),
        "spacy": check_module("spacy"),
        "deep_translator": check_module("deep_translator", "deep-translator"),
        "camelot": check_module("camelot", "camelot-py"),
        "langdetect": check_module("langdetect"),
        "PyPDF2": check_module("PyPDF2"),
    }

    model_checks = {
        "en_core_web_sm": check_spacy_model("en_core_web_sm"),
        "sv_core_news_sm": check_spacy_model("sv_core_news_sm"),
    }

    binary_checks = {
        "tesseract": check_tesseract(),
        "ghostscript": check_ghostscript(),
    }

    all_ok = True
    print("=" * 50)
    print("Dependency Check Report")
    print("=" * 50)

    for name, (ok, detail) in checks.items():
        status = "OK" if ok else "MISSING"
        if not ok:
            all_ok = False
        print(f"  {name:20s} [{status}]")
        if detail and not ok:
            print(f"    -> {detail[:100]}")

    print()
    for name, (ok, detail) in model_checks.items():
        status = "OK" if ok else "MISSING"
        if not ok:
            all_ok = False
        print(f"  {name:20s} [{status}]")

    print()
    for name, (ok, detail) in binary_checks.items():
        status = "OK" if ok else "MISSING"
        if not ok:
            all_ok = False
        print(f"  {name:20s} [{status}]")
        if detail:
            print(f"    -> {detail[:80]}")

    print("=" * 50)
    if all_ok:
        print("All dependencies met.")
    else:
        print("Some dependencies missing. Run python setup_deps.py")
    print("=" * 50)
    return all_ok


if __name__ == "__main__":
    validate_all()
