from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QSpinBox, QDialog,
    QPushButton, QLabel, QSpacerItem, QComboBox,
    QCheckBox
)

from helper import config_manager, get_string, settings_strings, theme_manager, show_message
from buffet import BuffetDefaultItemsList
from default_prices import DefaultPricesDialog


class SettingsDialog(QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.setWindowTitle(get_string("settings"))

        self.app = app

        self.init_ui()

    def init_ui(self):
        self.lbl_language = QLabel(f"{get_string('language')}:")

        self.combo_language = QComboBox()
        self.combo_language.addItems(
            [get_string('english'), get_string('farsi')])
        self.combo_language.setCurrentText(get_string(
            settings_strings['lang'][config_manager.get('LANGUAGE').capitalize()].lower()))

        self.lbl_theme = QLabel(f"{get_string('theme')}:")

        self.combo_theme = QComboBox()
        items = [get_string('light'),
                 get_string('dark'),
                 get_string('barcelona'),
                 get_string("tractor"),
                 get_string("cyberpunk"),
                 get_string("minecraft")]
        self.combo_theme.addItems(items)
        self.combo_theme.setCurrentText(get_string(settings_strings['theme'][
            config_manager.get('THEME').capitalize()].lower()))

        self.lbl_table_count = QLabel(f"{get_string('table_count')}:")

        self.spin_table_count = QSpinBox()
        self.spin_table_count.setRange(1, 50)
        self.spin_table_count.setValue(config_manager.get("TABLE_COUNT"))

        self.lbl_hide = QLabel(f"{get_string("setting_hide")}:")

        self.checkbox_hide = QCheckBox()
        self.checkbox_hide.setChecked(config_manager.get("HIDE_BTN"))

        self.lbl_price_default = QLabel(f"{get_string("default_hide")}:")

        self.checkbox_price_default = QCheckBox()
        self.checkbox_price_default.setChecked(config_manager.get("DEFAULT_PRICE_BTN"))

        self.btn_price_default = QPushButton(get_string('price_default'))
        self.btn_price_default.clicked.connect(self.open_default_prices)

        self.btn_buffet_default = QPushButton(get_string('buffet_default'))
        self.btn_buffet_default.clicked.connect(self.open_default_buffet)

        self.btn_apply = QPushButton(get_string('apply'))
        self.btn_apply.clicked.connect(self.apply_settings)

        self.btn_cancel = QPushButton(get_string('cancel'))
        self.btn_cancel.clicked.connect(lambda: self.close())

        settings_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        settings_layout.addWidget(self.lbl_language)
        settings_layout.addWidget(self.combo_language)
        settings_layout.addSpacerItem(QSpacerItem(0, 15))

        settings_layout.addWidget(self.lbl_theme)
        settings_layout.addWidget(self.combo_theme)
        settings_layout.addSpacerItem(QSpacerItem(0, 15))

        settings_layout.addWidget(self.lbl_table_count)
        settings_layout.addWidget(self.spin_table_count)
        settings_layout.addSpacerItem(QSpacerItem(0, 15))

        if config_manager.get("LANGUAGE") == "farsi":
            row1.addWidget(self.checkbox_hide, alignment=Qt.AlignLeft)
            row1.addWidget(self.lbl_hide, alignment=Qt.AlignRight)

            row2.addWidget(self.checkbox_price_default, alignment=Qt.AlignLeft)
            row2.addWidget(self.lbl_price_default, alignment=Qt.AlignRight)
        else:
            row1.addWidget(self.lbl_hide, alignment=Qt.AlignLeft)
            row1.addWidget(self.checkbox_hide, alignment=Qt.AlignRight)

            row2.addWidget(self.lbl_price_default, alignment=Qt.AlignRight)
            row2.addWidget(self.checkbox_price_default, alignment=Qt.AlignLeft)
        settings_layout.addSpacerItem(QSpacerItem(0, 15))

        row3.addWidget(self.btn_cancel)
        row3.addWidget(self.btn_apply)

        settings_layout.addLayout(row1)
        settings_layout.addLayout(row2)
        settings_layout.addWidget(self.btn_price_default)
        settings_layout.addWidget(self.btn_buffet_default)
        settings_layout.addLayout(row3)

        self.setLayout(settings_layout)

    def apply_settings(self):
        config_manager.set(
            "LANGUAGE", settings_strings['lang'][self.combo_language.currentText()])
        config_manager.set(
            "THEME", settings_strings['theme'][self.combo_theme.currentText()])
        config_manager.set("TABLE_COUNT", self.spin_table_count.value())
        config_manager.set("DEFAULT_PRICE_BTN", self.checkbox_price_default.isChecked())
        config_manager.set("HIDE_BTN", self.checkbox_hide.isChecked())

        theme_manager.load_theme(self.app, config_manager.get("THEME"))

        show_message(get_string('settings_applied'))
        self.close()

    def open_default_buffet(self):
        window = BuffetDefaultItemsList(self)
        window.exec_()

    def open_default_prices(self):
        window = DefaultPricesDialog(self)
        window.exec_()
