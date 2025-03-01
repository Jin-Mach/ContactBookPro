from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtWidgets import QTableView, QHeaderView


class ContactsTableviewWidget(QTableView):
    def __init__(self, model: QSqlTableModel, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsTableviewWidget")
        self.setModel(model)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.hide_colums()

    def hide_colums(self) -> None:
        column_count = self.model().columnCount()
        columns = [1, 2, 3, 4, 5, 6, 7, 8]
        for index in range(column_count):
            if index in columns:
                self.setColumnHidden(index, False)
            else:
                self.setColumnHidden(index, True)