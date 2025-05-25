from typing import Optional

from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QTableView, QHeaderView, QWidget, QAbstractItemView

from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.controlers.contact_data_controller import ContactDataController
from src.database.models.mandatory_model import MandatoryModel
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


# noinspection PyTypeChecker
class ContactsTableviewWidget(QTableView):
    def __init__(self, mandatory_model: MandatoryModel, detail_widget: ContactsDetailWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsTableviewWidget")
        self.mandatory_model = mandatory_model
        self.contact_data_controler = ContactDataController(detail_widget)
        self.detail_widget = detail_widget
        self.setModel(self.mandatory_model)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSortingEnabled(True)
        self.set_headers()
        self.selectionModel().currentRowChanged.connect(lambda: self.set_detail_data(None))
        self.selectionModel().currentChanged.connect(self.set_search_text_label)
        self.ui_text = LanguageProvider.get_ui_text(self.objectName())
        self.gender_items = self.ui_text["gender_items"]
        self.relationship_items = self.ui_text["relationship_items"]

    def set_headers(self) -> None:
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        column_count = self.model().columnCount()
        columns = [1, 2, 3, 4, 5, 6]
        for index in range(column_count):
            if index in columns:
                self.setColumnHidden(index, False)
            else:
                self.setColumnHidden(index, True)

    def set_detail_data(self, last_index: Optional[QModelIndex]) -> None:
        try:
            current_index = last_index
            if not current_index:
                current_index = self.selectionModel().currentIndex()
                if not current_index.isValid():
                    get_logger().error("indexError", exc_info=True)
                    return
            current_row = self.mandatory_model.data(self.mandatory_model.index(current_index.row(), 0))
            self.contact_data_controler.get_models_data(current_row, self)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_search_text_label(self) -> None:
        try:
            tool_bar = self.parent().findChild(QWidget, "contactsToolbarWidget")
            current_column = self.currentIndex().column()
            if tool_bar:
                if current_column == 1 or current_column == 2:
                    tool_bar.search_line_edit.clear()
                    tool_bar.search_combobox.clear()
                    if current_column == 1:
                        tool_bar.search_combobox.addItems(self.gender_items)
                    else:
                        tool_bar.search_combobox.addItems(self.relationship_items)
                    tool_bar.search_combobox.setDisabled(False)
                    tool_bar.search_line_edit.setDisabled(True)
                else:
                    tool_bar.search_combobox.clear()
                    tool_bar.search_combobox.setDisabled(True)
                    tool_bar.search_line_edit.setDisabled(False)
            search_filter = self.ui_text["searchFilter"]
            current_filter = search_filter[str(current_column)]
            if tool_bar:
                tool_bar.search_text_label.setText(f"{self.ui_text["searchText"]} {current_filter}")
        except Exception as e:
            ErrorHandler.exception_handler(e, self)