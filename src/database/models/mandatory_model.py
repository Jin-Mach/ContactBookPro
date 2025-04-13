from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel, QSqlDatabase

from src.database.database_utilities.set_manadatory_headers import set_manadatory_model_headers
from src.utilities.error_handler import ErrorHandler


class MandatoryModel(QSqlTableModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent, db_connection)
        self.setObjectName("mandatoryModel")
        self.setTable("mandatory")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.setSort(0, Qt.SortOrder.AscendingOrder)
        set_manadatory_model_headers(self)
        self.select()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 3:
                first_name = super().data(self.index(index.row(), 3), role)
                second_name = super().data(self.index(index.row(), 4), role)
                return f"{first_name} {second_name}"
            elif index.column() == 6:
                adress = super().data(self.index(index.row(), 7), role)
                city = super().data(self.index(index.row(), 8), role)
                post_code = super().data(self.index(index.row(), 9), role)
                country = super().data(self.index(index.row(), 10), role)
                return f"{adress}, {city}, {post_code}, {country}"
            elif index.column() == 4:
                return super().data(self.index(index.row(), 5), role)
            elif index.column() == 5:
                return super().data(self.index(index.row(), 6), role)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        return super().data(index, role)

    def add_contact(self, data: list) -> None:
        record = self.record()
        for index, value in enumerate(data):
            record.setValue(index + 1, value)
        self.insertRecord(self.rowCount(), record)
        if not self.submitAll():
            ErrorHandler.database_error(self.lastError().text(), False)
        self.select()

    def delete_contact(self, row_index: int) -> None:
        if row_index > -1:
            if not self.removeRow(row_index):
                ErrorHandler.database_error(self.lastError().text(), False)
                return
            if not self.submitAll():
                ErrorHandler.database_error(self.lastError().text(), False)
        self.select()

    def clear_database(self) -> None:
        row_count = self.rowCount()
        if row_count > 0:
            self.removeRows(0, row_count)
            if not self.submitAll():
                ErrorHandler.database_error(self.lastError().text(), False)
        self.select()