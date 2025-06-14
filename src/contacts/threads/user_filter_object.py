from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class UserFilterObject(QObject):
    search_completed = pyqtSignal(list)
    error_message = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, db_path: str, query_values: tuple) -> None:
        super().__init__()
        self.db_path = db_path
        self.query = query_values[0]
        self.values = query_values[1]
        self.connection_name = f"userFilterThread{id(self)}"

    def run_user_filter(self) -> None:
        id_list = []
        db = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
        db.setDatabaseName(self.db_path)
        if not db.open():
            self.error_message.emit(db.lastError().text())
            self.finished.emit()
            return
        query = QSqlQuery(db)
        query.prepare(self.query)
        for value in self.values:
            query.addBindValue(value)
        if not query.exec():
            self.error_message.emit(query.lastError().text())
            self.finished.emit()
            return
        while query.next():
            id_list.append(query.value(0))
        self.search_completed.emit(id_list)
        self.finished.emit()