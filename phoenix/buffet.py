from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSpinBox,
    QPushButton, QLabel, QSpacerItem, QListWidgetItem,
    QLineEdit, QComboBox, QDialog, QListWidget
)

from helper import (
    BuffetItem, get_string, config_manager,
    format_price_input, show_message
)


class BuffetDialog(QDialog):
    def __init__(self, main_window, buffet_items):
        super().__init__(main_window)

        self.buffet_items = buffet_items

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()

        self.lbl_name = QLabel(f"{get_string('item_name')}:")

        self.lbl_price = QLabel(f"{get_string('item_price')}:")

        self.lbl_quantity = QLabel(f"{get_string('item_quantity')}:")

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText(get_string('item_name'))

        self.input_price = QLineEdit()
        self.input_price.setPlaceholderText(get_string('item_price'))
        self.input_price.setValidator(QIntValidator())
        self.input_price.textEdited.connect(lambda: self.input_price.setText(
            format_price_input(self.input_price.text())))

        self.spin_quantity = QSpinBox()
        self.spin_quantity.setRange(1, 100)

        self.combo_default = QComboBox()
        buffet_items = config_manager.get("BUFFET_DEFAULT_ITEMS")
        if buffet_items:
            self.combo_default.addItems(
                [get_string('default_item')] + [f"{item['name']}: {item['price']}" for item in buffet_items])
        else:
            self.combo_default.addItems(
                [get_string('default_item')])
        self.combo_default.setCurrentText(get_string('default_item'))
        self.combo_default.currentTextChanged.connect(self.set_default_item)

        self.btn_add_item = QPushButton(get_string('add'))
        self.btn_add_item.clicked.connect(self.add_buffet_item)

        self.btn_cancel = QPushButton(get_string('cancel'))
        self.btn_cancel.clicked.connect(lambda: self.close())

        if config_manager.get("LANGUAGE") == "farsi":
            row1.addWidget(self.input_name, alignment=Qt.AlignLeft)
            row1.addWidget(self.lbl_name, alignment=Qt.AlignRight)

            row2.addWidget(self.input_price, alignment=Qt.AlignLeft)
            row2.addWidget(self.lbl_price, alignment=Qt.AlignRight)

            row3.addWidget(self.spin_quantity, alignment=Qt.AlignLeft)
            row3.addWidget(self.lbl_quantity, alignment=Qt.AlignRight)

        else:
            row1.addWidget(self.lbl_name, alignment=Qt.AlignLeft)
            row1.addWidget(self.input_name, alignment=Qt.AlignRight)

            row2.addWidget(self.lbl_price, alignment=Qt.AlignLeft)
            row2.addWidget(self.input_price, alignment=Qt.AlignRight)

            row3.addWidget(self.lbl_quantity, alignment=Qt.AlignLeft)
            row3.addWidget(self.spin_quantity, alignment=Qt.AlignRight)
        

        row4.addWidget(self.combo_default)

        row5.addWidget(self.btn_cancel)
        row5.addWidget(self.btn_add_item)

        layout.addLayout(row1)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row2)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row3)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row4)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row5)

        self.setLayout(layout)

    def add_buffet_item(self):
        name = self.input_name.text()
        price = self.input_price.text()
        quantity = self.spin_quantity.value()
        if name.strip() == "" or price == "":
            show_message(get_string('add_buffet_item_error'))
        else:
            item = BuffetItem(name, price, quantity)
            self.buffet_items.append(item)
            show_message(get_string('added'))
            self.close()

    def set_default_item(self):
        if self.combo_default.currentText() != get_string('default_item'):
            item_data = self.combo_default.currentText().strip().split(":")
            self.input_name.setText(item_data[0])
            self.input_price.setText(item_data[1])
        else:
            self.input_name.setText(None)
            self.input_price.setText(None)


class BuffetDefaultDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        self.lbl_name = QLabel(f"{get_string('item_name')}:")

        self.lbl_price = QLabel(f"{get_string('item_price')}:")

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText(get_string('item_name'))

        self.input_price = QLineEdit()
        self.input_price.setPlaceholderText(get_string('item_price'))
        self.input_price.setValidator(QIntValidator())
        self.input_price.textEdited.connect(lambda: self.input_price.setText(
            format_price_input(self.input_price.text())))

        self.btn_add_item = QPushButton(get_string('add'))
        self.btn_add_item.clicked.connect(self.add_buffet_item)

        self.btn_cancel = QPushButton(get_string('cancel'))
        self.btn_cancel.clicked.connect(lambda: self.close())

        if config_manager.get("LANGUAGE") == "farsi":
            row1.addWidget(self.input_name, alignment=Qt.AlignLeft)
            row1.addWidget(self.lbl_name, alignment=Qt.AlignRight)

            row2.addWidget(self.input_price, alignment=Qt.AlignLeft)
            row2.addWidget(self.lbl_price, alignment=Qt.AlignRight)

        else:
            row1.addWidget(self.lbl_name, alignment=Qt.AlignLeft)
            row1.addWidget(self.input_name, alignment=Qt.AlignRight)

            row2.addWidget(self.lbl_price, alignment=Qt.AlignLeft)
            row2.addWidget(self.input_price, alignment=Qt.AlignRight)

        row3.addWidget(self.btn_cancel)
        row3.addWidget(self.btn_add_item)

        layout.addLayout(row1)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row2)
        layout.addSpacerItem(QSpacerItem(0, 15))

        layout.addLayout(row3)

        self.setLayout(layout)

    def add_buffet_item(self):
        name = self.input_name.text()
        price = self.input_price.text()
        if name.strip() == "" or price == "":
            show_message(get_string('add_buffet_item_error'))
        else:
            item = BuffetItem(name, price, 1)
            items = config_manager.get("BUFFET_DEFAULT_ITEMS", [])
            items.append(item.to_dict())
            config_manager.set("BUFFET_DEFAULT_ITEMS", items)
            show_message(get_string('added'))
            self.close()


class BuffetDefaultItemsList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout(self)
        row = QHBoxLayout()

        self.list_widget = QListWidget()

        self.btn_add_new = QPushButton(get_string('add_new_item'))
        self.btn_add_new.clicked.connect(self.add_new_item)

        self.btn_cancel = QPushButton(get_string('cancel'))
        self.btn_cancel.clicked.connect(lambda: self.close())

        row.addWidget(self.btn_cancel)
        row.addWidget(self.btn_add_new)

        layout.addWidget(self.list_widget)
        layout.addLayout(row)

        self.display_list()

    def display_list(self):
        self.list_widget.clear()
        buffet_items = config_manager.get("BUFFET_DEFAULT_ITEMS")
        if buffet_items:
            for index, item_text in enumerate(buffet_items):
                item_widget = QWidget()
                layout = QHBoxLayout(item_widget)
                layout.setContentsMargins(5, 2, 5, 2)

                label = QLabel(
                    f"{item_text['name']}: {item_text['price']} {get_string('currency')}")

                delete_btn = QPushButton(get_string('remove'))
                delete_btn.setStyleSheet(
                    "background-color: #e34747; border-radius: 15px; font-weight: bold; font-size: 12pt; padding: 6px")

                delete_btn.clicked.connect(
                    lambda clicked, idx=index: self.delete_item(idx))

                layout.addWidget(label)
                layout.addStretch()
                layout.addWidget(delete_btn)

                list_item = QListWidgetItem()
                list_item.setSizeHint(item_widget.sizeHint())
                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, item_widget)

    def delete_item(self, index):
        items = config_manager.get("BUFFET_DEFAULT_ITEMS")
        if 0 <= index < len(items):
            items.pop(index)
            config_manager.set("BUFFET_DEFAULT_ITEMS", items)
            self.display_list()

    def add_new_item(self):
        window = BuffetDefaultDialog(self)
        window.exec_()
        self.display_list()
