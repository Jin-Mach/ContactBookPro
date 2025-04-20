from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableView, QHeaderView

from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.controlers.contact_data_controller import ContactDataController
from src.database.models.mandatory_model import MandatoryModel
from src.utilities.error_handler import ErrorHandler


class ContactsTableviewWidget(QTableView):
    def __init__(self, mandatory_model: MandatoryModel, detail_widget: ContactsDetailWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsTableviewWidget")
        self.mandatory_model = mandatory_model
        self.contact_data_controler = ContactDataController(detail_widget)
        self.detail_widget = detail_widget
        self.setModel(self.mandatory_model)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSortingEnabled(True)
        self.hide_colums()
        self.selectionModel().currentRowChanged.connect(self.set_detail_data)

    def hide_colums(self) -> None:
        column_count = self.model().columnCount()
        columns = [3, 4, 5, 6]
        for index in range(column_count):
            if index in columns:
                self.setColumnHidden(index, False)
            else:
                self.setColumnHidden(index, True)

    def set_detail_data(self):
        try:
            current_index = self.selectionModel().currentIndex()
            if not current_index.isValid():
                print("chyba indexu")
                return
            current_row = self.mandatory_model.data(self.mandatory_model.index(current_index.row(), 0))
            self.contact_data_controler.get_models_data(current_row)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)