from PyQt6.QtCore import QByteArray
from PyQt6.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery

from src.utilities.error_handler import ErrorHandler


class DetailModel(QSqlTableModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent, db_connection)
        self.setObjectName("detailModel")
        self.db_connection = db_connection
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.setTable("detail")
        self.select()

    def add_contact(self, data: list) -> None:
        query = QSqlQuery(self.db_connection)
        query.prepare("""INSERT INTO detail (id, title, birthday, notes, photo)
                        VALUES (?, ?, ?, ?, ?)
        """)
        for value in data:
            if isinstance(value, bytes):
                value = QByteArray(value)
            query.addBindValue(value)
        if not query.exec():
            ErrorHandler.database_error(query.lastError().text(), False, custom_message="queryError")

    def update_contact(self, contact_id: int, data: list) -> None:
        query = QSqlQuery(self.db_connection)
        query.prepare("UPDATE detail SET title=?, birthday=?, notes=?, photo=? WHERE id=?")
        for value in data:
            if isinstance(value, bytes):
                query.addBindValue(QByteArray(value))
            else:
                query.addBindValue(value)
        query.addBindValue(contact_id)
        if not query.exec():
            ErrorHandler.database_error(query.lastError().text(), False, custom_message="queryError")