from PyQt5.QtWidgets import QMessageBox
from config_manager import ConfigManager
from language_manager import LanguageManager
from theme_manager import ThemeManager

config_manager = ConfigManager()
language_manager = LanguageManager(config_manager.get("LANGUAGE"))
get_string = language_manager.get_string
theme_manager = ThemeManager()

settings_strings = {
    "lang": {
        "English": "english",
        "انگلیسی": "english",
        "Farsi": "farsi",
        "فارسی": "farsi"
    },
    "theme": {
        "Light": "light",
        "روشن": "light",
        "Dark": "dark",
        "تاریک": "dark",
        "Barcelona": "barcelona",
        "بارسلونا": "barcelona"
    }
}


class BuffetItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}: {self.price}"

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
        }


def clean_price(price_text):
    if "," in price_text:
        return price_text.replace(",", "")
    return price_text


def format_price(price_text):
    return f"{price_text:,}"


def calc_price(time, price_per_hour, buffet_items):
    buffet_price = 0
    if buffet_items:
        for item in buffet_items:
            buffet_price += (int(clean_price(item.price)) * int(item.quantity))
    secs = time.second()
    mins = time.minute()
    hrs = time.hour()
    total_secs = secs + mins*60 + hrs*60*60
    cleaned_price_per_hour = int(clean_price(price_per_hour))
    price = (total_secs * cleaned_price_per_hour) / 3600
    rounded_price = int(price / 1000) * 1000
    return format_price(rounded_price + buffet_price)


def format_price_input(price_text):
    not_valid = ("+", "-", "0", "")
    if price_text in not_valid:
        return None
    else:
        formatted = format_price(int(clean_price(price_text)))
        return formatted


def show_message(text):
    message_window = QMessageBox()
    message_window.setText(text)
    message_window.exec_()
