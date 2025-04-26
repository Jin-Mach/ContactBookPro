from PyQt6.QtSql import QSqlTableModel, QSqlDatabase

from src.database.database_utilities.row_data_provider import RowDataProvider
from src.utilities.error_handler import ErrorHandler


class InfoModel(QSqlTableModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent, db_connection)
        self.setObjectName("infoModel")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.setTable("info")
        self.select()

    def add_contact(self, data: list) -> None:
        record = self.record()
        for index, value in enumerate(data):
            record.setValue(index, value)
        self.insertRecord(-1, record)
        if not self.submitAll():
            ErrorHandler.database_error(self.lastError().text(), False)

    def update_contact(self, contact_id: int, current_date: str) -> None:
        row_index = RowDataProvider.get_row_by_id(self, contact_id)
        if row_index == -1:
            return
        index = self.index(row_index, 2)
        self.setData(index, current_date)
        if not self.submitAll():
            ErrorHandler.database_error(self.lastError().text(), False)