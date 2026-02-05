import json
import os

class LanguageManager:
    def __init__(self, lang_code="english"):
        self.lang_code = lang_code
        self.strings = {}
        self.load_language(lang_code) 

    def load_language(self, lang_code):
        path = os.path.join("languages", f"{lang_code}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.strings = json.load(f)
            except:
                self.strings = {}
        else:
            self.strings = {}

    def get_string(self, key):
        return self.strings.get(key, key)