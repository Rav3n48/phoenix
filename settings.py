from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QSpinBox, QDialog,
    QPushButton, QLabel, QSpacerItem, QComboBox
)

from helper import config_manager, get_string, settings_strings, show_message
from buffet import BuffetDefaultItemsList


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        settings_layout = QVBoxLayout()

        row = QHBoxLayout()

        self.lbl_language = QLabel(f"{get_string('language')}:")

        self.lbl_theme = QLabel(f"{get_string('theme')}:")

        self.lbl_table_count = QLabel(f"{get_string('table_count')}:")

        self.combo_language = QComboBox()
        self.combo_language.addItems(
            [get_string('english'), get_string('farsi')])
        self.combo_language.setCurrentText(get_string(
            settings_strings['lang'][config_manager.get('LANGUAGE').capitalize()].lower()))

        self.combo_theme = QComboBox()
        self.combo_theme.addItems(
            [get_string('light'), get_string('dark'), get_string('barcelona')])
        self.combo_theme.setCurrentText(get_string(settings_strings['theme'][
            config_manager.get('THEME').capitalize()].lower()))

        self.spin_table_count = QSpinBox()
        self.spin_table_count.setRange(1, 50)
        self.spin_table_count.setValue(config_manager.get("TABLE_COUNT"))

        self.btn_buffet_default = QPushButton(get_string('buffet_default'))
        self.btn_buffet_default.clicked.connect(self.open_default_buffet)

        self.btn_apply = QPushButton(get_string('apply'))
        self.btn_apply.clicked.connect(self.apply_settings)

        self.btn_cancel = QPushButton(get_string('cancel'))
        self.btn_cancel.clicked.connect(lambda: self.close())

        row.addWidget(self.btn_cancel)
        row.addWidget(self.btn_apply)

        settings_layout.addWidget(self.lbl_language)
        settings_layout.addWidget(self.combo_language)
        settings_layout.addSpacerItem(QSpacerItem(0, 15))

        settings_layout.addWidget(self.lbl_theme)
        settings_layout.addWidget(self.combo_theme)
        settings_layout.addSpacerItem(QSpacerItem(0, 15))

        settings_layout.addWidget(self.lbl_table_count)
        settings_layout.addWidget(self.spin_table_count)
        settings_layout.addSpacerItem(QSpacerItem(0, 15))

        settings_layout.addWidget(self.btn_buffet_default)

        settings_layout.addLayout(row)

        self.setLayout(settings_layout)

    def apply_settings(self):
        config_manager.set(
            "LANGUAGE", settings_strings['lang'][self.combo_language.currentText()])
        config_manager.set(
            "THEME", settings_strings['theme'][self.combo_theme.currentText()])
        config_manager.set("TABLE_COUNT", self.spin_table_count.value())

        show_message(get_string('settings_applied'))
        self.close()

    def open_default_buffet(self):
        window = BuffetDefaultItemsList(self)
        window.exec_()
