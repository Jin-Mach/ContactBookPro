from functools import partial
from typing import Callable

from PyQt6.QtCore import QSize, QItemSelectionModel
from PyQt6.QtWidgets import QListWidget, QAbstractItemView, QWidget, QHBoxLayout, QListWidgetItem, QLabel, QPushButton, \
    QVBoxLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class UserFiltersListwidget(QListWidget):
    def __init__(self, delete_filter: Callable[[str], None], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("userFiltersListwidget")
        self.delete_filter = delete_filter
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())

    def set_filters_data(self, filters: dict[str, dict]) -> None:
        try:
            self.clear()
            filters_names = list(filters.keys())
            filters_names.sort()
            for filter_name in filters_names:
                widget = self.create_list_widget(str(filter_name))
                if widget:
                    list_widget_item = QListWidgetItem()
                    list_widget_item.setSizeHint(QSize(0, 50))
                    self.addItem(list_widget_item)
                    self.setItemWidget(list_widget_item, widget)
            self.selectionModel().setCurrentIndex(self.model().index(0, 0), QItemSelectionModel.SelectionFlag.SelectCurrent)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def create_list_widget(self, filter_name: str) -> QWidget | None:
        try:
            widget = QWidget()
            widget.filter_name = filter_name
            layout = QHBoxLayout()
            layout.setContentsMargins(5, 0, 5, 0)
            text_label = QLabel(filter_name)
            button_layout = QVBoxLayout()
            delete_filter_button = QPushButton()
            delete_filter_button.setFixedSize(30, 30)
            delete_filter_button.setObjectName("deleteFilterPushbutton")
            IconProvider.set_buttons_icon(self.objectName(), [delete_filter_button], QSize(30, 30), self)
            if delete_filter_button.objectName() in self.tooltips_text:
                delete_filter_button.setToolTip(self.tooltips_text[delete_filter_button.objectName()])
                delete_filter_button.setToolTipDuration(5000)
            delete_filter_button.clicked.connect(partial(self.delete_selected_filter, filter_name))
            button_layout.addStretch()
            button_layout.addWidget(delete_filter_button)
            button_layout.addStretch()
            layout.addWidget(text_label)
            layout.addLayout(button_layout)
            widget.setLayout(layout)
            return widget
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def delete_selected_filter(self, filter_name: str) -> None:
        try:
            self.delete_filter(filter_name)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def return_selected_filter(self) -> str | None:
        try:
            item = self.currentItem()
            if item is None:
                return None
            selected_widget = self.itemWidget(item)
            return selected_widget.filter_name
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None