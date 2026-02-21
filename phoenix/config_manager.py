import json
import os


class ConfigManager:
    def __init__(self):
        self.path = "config.json"
        self.config_data = self.load_config()

    def load_config(self):
        default_config = {
            "TABLE_COUNT": 3,
            "LANGUAGE": "english",
            "THEME": "dark",
            "HIDE_BTN": True,
            "DEFAULT_PRICE_BTN": False,
            "DEFAULT_PRICES": {
                "ONE_PLAYER": "0",
                "TWO_PLAYERS": "0",
                "FOUR_PLAYERS": "0"
            },
            "BUFFET_DEFAULT_ITEMS": []
        }

        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as config_file:
                    return json.load(config_file)
            except:
                return default_config
        else:
            return default_config

    def save_config(self):
        with open(self.path, "w", encoding="utf-8") as config_file:
            json.dump(self.config_data, config_file,
                      indent=4, ensure_ascii=False)

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self.save_config()
