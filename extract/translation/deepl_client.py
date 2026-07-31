import json
import os
from extract.config import CONFIG, CACHE_DIR, prompt_deepl_key


class DeepLClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or CONFIG.get("deepl_api_key", "")
        self.translator = None
        self.cache_dir = os.path.join(CACHE_DIR, "translations")
        os.makedirs(self.cache_dir, exist_ok=True)

    def translate_batch(self, classified):
        if not self.api_key:
            print("    No DeepL API key — skipping Swedish translation")
            return self._fill_english(classified)
        all_entries = []
        for key in ["auto_accepted", "flag_yellow", "flag_red"]:
            all_entries.extend(classified.get(key, []))
        if not all_entries:
            return classified
        texts_to_translate = []
        entry_map = []
        for i, entry in enumerate(all_entries):
            texts_to_translate.append(entry.get("concept", ""))
            entry_map.append((i, "concept"))
            texts_to_translate.append(entry.get("definition", ""))
            entry_map.append((i, "definition"))
            texts_to_translate.append(entry.get("real_world_scenario", ""))
            entry_map.append((i, "real_world_scenario"))
            texts_to_translate.append(entry.get("case_study_cloze", ""))
            entry_map.append((i, "case_study_cloze"))
        translated_texts = self._translate_to_swedish(texts_to_translate)
        for (entry_idx, field), translated in zip(entry_map, translated_texts):
            if translated and entry_idx < len(all_entries):
                if "sv" not in all_entries[entry_idx]:
                    all_entries[entry_idx]["sv"] = {}
                all_entries[entry_idx]["sv"][field] = translated
        return classified

    def _translate_to_swedish(self, texts):
        if not texts:
            return []
        cache_key = self._make_cache_key(texts)
        cache_path = os.path.join(self.cache_dir, cache_key + ".json")
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        try:
            from deep_translator import DeeplTranslator
            translator = DeeplTranslator(api_key=self.api_key, source="en", target="sv")
            translations = []
            batch_size = 50
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch = [t if t else "" for t in batch]
                results = translator.translate_batch(batch)
                translations.extend(results)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(translations, f)
            return translations
        except Exception as e:
            print(f"    Translation failed: {e}")
            return texts

    def _make_cache_key(self, texts):
        import hashlib
        key = "|".join(texts[:10])
        return hashlib.md5(key.encode()).hexdigest()[:16]

    def _fill_english(self, classified):
        for key in ["auto_accepted", "flag_yellow", "flag_red"]:
            for entry in classified.get(key, []):
                entry["sv"] = {
                    "concept": entry.get("concept", ""),
                    "definition": entry.get("definition", ""),
                    "real_world_scenario": entry.get("real_world_scenario", ""),
                    "case_study_cloze": entry.get("case_study_cloze", ""),
                }
        return classified
