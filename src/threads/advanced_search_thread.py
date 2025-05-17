from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class AdvancedSearchThread(QThread):
    search_completed = pyqtSignal(list)
    error_message = pyqtSignal(str)
    def __init__(self, db_connection: QSqlDatabase, query_values: tuple) -> None:
        super().__init__()
        self.db_connection = db_connection
        self.query = query_values[0]
        self.values = query_values[1]

    def run(self) -> None:
        id_list = []
        query = QSqlQuery(self.db_connection)
        query.prepare(self.query)
        for value in self.values:
            query.addBindValue(value)
        if not query.exec():
            self.error_message.emit(query.lastError().text())
            return
        while query.next():
            id_list.append(query.value(0))
        self.search_completed.emit(id_list)