from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QIcon, QIntValidator, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QShortcut,
    QLineEdit, QMenuBar, QAction
)
import os
from helper import (
    get_string, theme_manager, config_manager,
    format_price_input, show_message, calc_price,
    clean_price, format_price
)
from settings import SettingsDialog
from buffet import BuffetDialog


class TabbedPanelWidget(QWidget):
    def __init__(self, app):
        super().__init__()

        self.app = app

        self.init_ui()

    def init_ui(self):
        self.menu_bar = QMenuBar()

        self.action_settings = QAction(get_string('settings'), self)
        self.action_settings.triggered.connect(self.open_settings)

        self.menu_bar.addAction(self.action_settings)

        tabs = QTabWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.menu_bar)
        layout.addWidget(tabs)

        for i in range(config_manager.get("TABLE_COUNT")):
            self.table_name = f"{get_string('table')} {i+1}"
            tab = QWidget()
            content = MainWidget()
            content_layout = QVBoxLayout(tab)
            content_layout.addWidget(content)
            tabs.addTab(tab, self.table_name)

    def open_settings(self):
        window = SettingsDialog(self.app, self)
        window.exec_()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.buffet_items = list()

        self.time = QTime(0, 0, 0)

        self.init_ui()

    def init_ui(self):
        self.lbl_timer = QLabel(self.time.toString("hh:mm:ss"))
        self.lbl_timer.setStyleSheet(
            "font-size: 80px; padding: 20px; margin: 25px")

        self.input_price_per_hour = QLineEdit()
        self.input_price_per_hour.setPlaceholderText(
            get_string('price_per_hour'))
        self.input_price_per_hour.setValidator(QIntValidator())
        self.input_price_per_hour.textEdited.connect(
            lambda: self.input_price_per_hour.setText(
                format_price_input(
                    self.input_price_per_hour.text())))
        self.input_price_per_hour.setAlignment(Qt.AlignCenter)
        self.input_price_per_hour.setStyleSheet(
            "margin: 10px 160px; padding: 10px; font-size: 16pt")
        
        self.btn_hide_price_input = QPushButton(get_string("hide"))
        self.btn_hide_price_input.clicked.connect(self.hide_price)
        self.btn_hide_price_input.setFlat(True)
        shortcut_hide = QShortcut(QKeySequence(Qt.Key_H), self)
        shortcut_hide.activated.connect(self.btn_hide_price_input.click)
        self.btn_hide_price_input.setStyleSheet("margin: 30px 5px; padding: 5px; border: none; background: transparent; font-size: 10pt")

        self.btn_start_stop = QPushButton(get_string('start'))
        shortcut_start_stop = QShortcut(QKeySequence(Qt.Key_Space), self)
        shortcut_start_stop.activated.connect(self.btn_start_stop.click)
        self.btn_start_stop.clicked.connect(self.start_stop)

        self.btn_price = QPushButton(get_string('price'))
        shortcut_price = QShortcut(QKeySequence(Qt.Key_Tab), self)
        shortcut_price.activated.connect(self.btn_price.click)
        self.btn_price.clicked.connect(self.price_display)

        self.btn_reset = QPushButton(get_string('reset'))
        shortcut_reset = QShortcut(QKeySequence(Qt.Key_R), self)
        shortcut_reset.activated.connect(self.btn_reset.click)
        self.btn_reset.clicked.connect(self.reset)

        self.btn_buffet = QPushButton(get_string('buffet'))
        shortcut_buffet = QShortcut(QKeySequence(Qt.Key_B), self)
        shortcut_buffet.activated.connect(self.btn_buffet.click)
        self.btn_buffet.clicked.connect(self.buffet)

        row1 = QHBoxLayout()
        row1.addWidget(self.input_price_per_hour)
        if config_manager.get("HIDE_BTN"):
            row1.addWidget(self.btn_hide_price_input, alignment=Qt.AlignRight)

        row2 = QHBoxLayout()
        row2.addWidget(self.btn_reset)
        row2.addWidget(self.btn_buffet)
        row2.addWidget(self.btn_price)
        row2.addWidget(self.btn_start_stop)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.lbl_timer, alignment=Qt.AlignCenter)
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

    def start_stop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.update_btn_text()
        else:
            self.timer.start()
            self.update_btn_text()

    def update_btn_text(self):
        if self.timer.isActive():
            self.btn_start_stop.setText(get_string('stop'))
        else:
            self.btn_start_stop.setText(get_string('start'))

    def reset(self):
        self.timer.stop()
        self.time = QTime(0, 0, 0)
        self.input_price_per_hour.clear()
        self.buffet_items = list()
        self.update_timer()
        self.update_btn_text()

    def update_timer(self):
        if self.timer.isActive():
            self.time = self.time.addSecs(1)
        txt = self.time.toString("hh:mm:ss")
        self.lbl_timer.setText(txt)

    def hide_price(self):
        if self.input_price_per_hour.isVisible():
            self.btn_hide_price_input.setText(get_string("show"))
            self.input_price_per_hour.setVisible(False)
        else:
            self.btn_hide_price_input.setText(get_string("hide"))
            self.input_price_per_hour.setVisible(True)

    def price_display(self):
        price_text = self.input_price_per_hour.text()
        if price_text == "" or self.time.toString() == "00:00:00":
            show_message(get_string('show_price_error'))
        else:
            total_price = calc_price(self.time, price_text, self.buffet_items)
            buffet_text = "\n"
            game_price = str()
            if self.buffet_items:
                game_price = int(clean_price(total_price))
                buffet_text = str()
                for item in self.buffet_items:
                    buffet_text += f"{item.name}: {item.quantity} {get_string('in_price')} {item.price} {get_string('currency')} \n"
                    game_price -= (int(clean_price(item.price))
                                   * int(item.quantity))

                show_message(
                    f"{get_string('total_price')}: {total_price} {get_string('currency')} \n{"-"*60}\n {get_string('game_price')}: {format_price(game_price)} {get_string('currency')} \n {buffet_text}")
            else:
                show_message(
                    f"{get_string('price')}: {total_price} {get_string('currency')} \n")

    def buffet(self):
        window = BuffetDialog(self, self.buffet_items)
        window.exec_()


def run():
    app = QApplication([])
    app.setWindowIcon(QIcon(os.path.join("assets", "phoenix.ico")))
    app.setApplicationName(get_string("phoenix"))
    app.setApplicationDisplayName(get_string("phoenix"))
    window = TabbedPanelWidget(app)
    theme_manager.load_theme(app, config_manager.get("THEME"))
    window.show()
    app.exec_()

if __name__ == "__main__":
    run()