from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel, QSqlDatabase

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class DatabaseModel(QSqlTableModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent, db_connection)
        self.setObjectName("databaseModel")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.setTable("contacts")
        self.set_headers_text()

    def set_headers_text(self) -> None:
        headers_text = LanguageProvider.get_headers_text(self.objectName())
        headers_keys = headers_text.keys()
        try:
            for index, key in enumerate(headers_keys):
                    self.setHeaderData(index, Qt.Orientation.Horizontal, headers_text[key])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
