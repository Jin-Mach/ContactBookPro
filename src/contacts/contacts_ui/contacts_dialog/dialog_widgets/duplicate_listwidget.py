from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QListWidget, QAbstractItemView, QWidget, QHBoxLayout, QLabel, QListWidgetItem

from src.utilities.error_handler import ErrorHandler


class DuplicateListwidget(QListWidget):
    def __init__(self, duplicate_data: list, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("duplicateListwidget")
        self.duplicate_data = duplicate_data
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.set_data(self.duplicate_data)

    def set_data(self, duplicate_data: list) -> None:
        try:
            for contact in duplicate_data:
                contact_id = contact["id"]
                first_name = contact["first_name"]
                second_name = contact["second_name"]
                widget = self.create_list_widget(contact_id, first_name, second_name)
                if widget:
                    list_widget_item = QListWidgetItem()
                    list_widget_item.setSizeHint(QSize(0, 50))
                    self.addItem(list_widget_item)
                    self.setItemWidget(list_widget_item, widget)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def create_list_widget(self, contact_id: int, first_name: str, second_name: str) -> QWidget | None:
        try:
            widget = QWidget()
            widget.setProperty("id", contact_id)
            main_layout = QHBoxLayout()
            main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_text_label = QLabel()
            name_text_label.setText(f"{first_name} {second_name}")
            main_layout.addWidget(name_text_label)
            widget.setLayout(main_layout)
            return widget
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def return_selected_contact_id(self) -> int | None:
        try:
            item = self.currentItem()
            if item is not None:
                widget = self.itemWidget(item)
                return widget.property("id")
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None