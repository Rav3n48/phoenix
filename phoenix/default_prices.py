from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpacerItem, QLineEdit, QDialog
)

from helper import (
    get_string, config_manager,
    format_price_input, show_message
)


class DefaultPricesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(get_string("price_default"))

        self.prices = config_manager.get("DEFAULT_PRICES")

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        self.lbl_one = QLabel(f"{get_string('one_player')}:")

        self.input_one = QLineEdit()
        self.input_one.setPlaceholderText(get_string('one_player'))
        self.input_one.setValidator(QIntValidator())
        self.input_one.textEdited.connect(lambda: self.input_one.setText(
            format_price_input(self.input_one.text())))
        self.input_one.setText(self.prices.get("ONE_PLAYER", "0"))

        self.lbl_two = QLabel(f"{get_string('two_players')}:")
        self.input_two = QLineEdit()
        self.input_two.setPlaceholderText(get_string('two_players'))
        self.input_two.setValidator(QIntValidator())
        self.input_two.textEdited.connect(lambda: self.input_two.setText(
            format_price_input(self.input_two.text())))
        self.input_two.setText(self.prices.get("TWO_PLAYERS", "0"))

        self.lbl_four = QLabel(f"{get_string('four_players')}:")
        self.input_four = QLineEdit()
        self.input_four.setPlaceholderText(get_string('four_players'))
        self.input_four.setValidator(QIntValidator())
        self.input_four.textEdited.connect(lambda: self.input_four.setText(
            format_price_input(self.input_four.text())))
        self.input_four.setText(self.prices.get("FOUR_PLAYERS", "0"))

        self.btn_confirm = QPushButton(get_string('confirm'))
        self.btn_confirm.clicked.connect(self.confirm)

        self.btn_cancel = QPushButton(get_string('cancel'))
        self.btn_cancel.clicked.connect(lambda: self.close())

        if config_manager.get("LANGUAGE") == "farsi":
            row1.addWidget(self.input_one, alignment=Qt.AlignLeft)
            row1.addWidget(self.lbl_one, alignment=Qt.AlignRight)

            row2.addWidget(self.input_two, alignment=Qt.AlignLeft)
            row2.addWidget(self.lbl_two, alignment=Qt.AlignRight)

            row3.addWidget(self.input_four, alignment=Qt.AlignLeft)
            row3.addWidget(self.lbl_four, alignment=Qt.AlignRight)

        else:
            row1.addWidget(self.lbl_one, alignment=Qt.AlignLeft)
            row1.addWidget(self.input_one, alignment=Qt.AlignRight)

            row2.addWidget(self.lbl_two, alignment=Qt.AlignLeft)
            row2.addWidget(self.input_two, alignment=Qt.AlignRight)

            row3.addWidget(self.lbl_four, alignment=Qt.AlignLeft)
            row3.addWidget(self.input_four, alignment=Qt.AlignRight)

        row4.addWidget(self.btn_cancel)
        row4.addWidget(self.btn_confirm)

        layout.addLayout(row1)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row2)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row3)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row4)

        self.setLayout(layout)

    def confirm(self):
        one = self.input_one.text()
        two = self.input_two.text()
        four = self.input_four.text()
        if one.strip() == "" or two == "" or four == "":
            show_message(get_string('default_price_error'))
        else:
            prices = config_manager.get("DEFAULT_PRICES", {
                "ONE_PLAYER": 0,
                "TWO_PLAYERS": 0,
                "FOUR_PLAYERS": 0
            })
            prices["ONE_PLAYER"] = one
            prices["TWO_PLAYERS"] = two
            prices["FOUR_PLAYERS"] = four
            config_manager.set("DEFAULT_PRICES", prices)
            show_message(get_string('done'))
            self.close()
