from typing import Callable

from PyQt6.QtCore import QAbstractTableModel, QSize
from PyQt6.QtWidgets import QTableView, QAbstractItemView, QHeaderView, QPushButton

from src.database.models.advanced_filter_model import AdvancedFilterModel
from src.database.utilities.model_header_provider import ModelHeaderProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class FiltersTableviewWidget(QTableView):
    def __init__(self, advanced_filter_model: AdvancedFilterModel, remove_filter: Callable[[int, QAbstractTableModel], None], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("filtersTableviewWidget")
        self.advanced_filter_model = advanced_filter_model
        self.remove_filter = remove_filter
        self.setModel(self.advanced_filter_model)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.set_headers()
        self.add_reset_button()

    def set_headers(self) -> None:
        ModelHeaderProvider.set_advanced_filter_model_headers(self.advanced_filter_model, self)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().resizeSection(4, 50)
        self.hideColumn(3)

    def create_reset_button(self, row: int) -> QPushButton | None:
        try:
            button = QPushButton()
            button.setObjectName("deleteFilterButton")
            button.setProperty("row", row)
            IconProvider.set_buttons_icon(self.objectName(), [button], QSize(20, 20), self)
            tooltip_text = LanguageProvider.get_tooltips_text(self.objectName())
            if tooltip_text:
                button.setToolTip(tooltip_text.get(button.objectName(), ""))
                button.setToolTipDuration(5000)
            button.clicked.connect(self.get_current_row)
            return button
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def add_reset_button(self) -> None:
        for row in range(self.advanced_filter_model.rowCount()):
            index = self.advanced_filter_model.index(row, 4)
            self.setIndexWidget(index, None)
            delete_filter_button = self.create_reset_button(row)
            if delete_filter_button:
                self.setIndexWidget(index, delete_filter_button)

    def get_current_row(self) -> None:
        try:
            button = self.sender()
            if not button:
                return
            row = button.property("row")
            self.remove_filter(row, self.advanced_filter_model)
            if self.advanced_filter_model.rowCount() > 0:
                self.add_reset_button()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent())