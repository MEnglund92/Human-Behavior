import os
import json
import getpass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SOURCE_DIRS = [
    os.path.join(PROJECT_ROOT, "Beteendepsykologi, Socialpsykologi & Mänsklig Natur"),
    os.path.join(PROJECT_ROOT, "Kroppsspråk & Icke-verbal kommunikation"),
]

PENDING_RENAME_DIR = os.path.join(BASE_DIR, "pending_rename")
OUTPUT_DIR = os.path.join(BASE_DIR, "extracted_json")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
DATA_JS_PATH = os.path.join(PROJECT_ROOT, "data.js")

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "deepl_api_key": "",
    "ghostscript_path": "",
    "tesseract_path": "",
    "confidence_thresholds": {
        "auto_accept": 0.70,
        "flag_yellow": 0.40,
        "flag_red": 0.0,
    },
    "strategy_weights": {
        "s1_regex": 0.9,
        "s2_nlp": 0.8,
        "s3_examples": 0.7,
        "s4_cloze": 0.6,
        "s5_glossary": 0.95,
        "s6_tables": 0.85,
        "s7_crossref": 0.75,
    },
    "ocr_dpi": 300,
    "translation_batch_size": 50,
    "spacy_models": {
        "en": "en_core_web_sm",
        "sv": "sv_core_news_sm",
    },
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            merged = dict(DEFAULT_CONFIG)
            merged.update(json.load(f))
            return merged
    except Exception:
        return dict(DEFAULT_CONFIG)


def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def prompt_deepl_key():
    cfg = load_config()
    if cfg.get("deepl_api_key"):
        return cfg["deepl_api_key"]
    print("\n=== DeepL API Configuration ===")
    print("DeepL provides the best Swedish translations for this pipeline.")
    print("Get your free API key at: https://www.deepl.com/pro-api\n")
    key = getpass.getpass("Enter your DeepL API key (or press Enter to skip translation): ").strip()
    if key:
        cfg["deepl_api_key"] = key
        save_config(cfg)
        print("API key saved to config.json\n")
    return key


CONFIG = load_config()
