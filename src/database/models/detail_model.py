from PyQt6.QtSql import QSqlTableModel, QSqlDatabase

from src.utilities.error_handler import ErrorHandler


class DetailModel(QSqlTableModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent, db_connection)
        self.setObjectName("detailModel")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.setTable("detail")

    def add_contact(self, data: list) -> None:
        record = self.record()
        for index, value in enumerate(data):
            record.setValue(index, value)
        self.insertRecord(-1, record)
        if not self.submitAll():
            ErrorHandler.database_error(self.lastError().text(), False)