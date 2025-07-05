from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.export_data_provider import ExportDataProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class ExportContactsListPdfObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool, str)

    def __init__(self, db_path: str, id_list: list | None, export_data_provider: ExportDataProvider,
                 main_window: QMainWindow) -> None:
        super().__init__()
        self.setObjectName("exportContactsListPdfObject")
        self.db_path = db_path
        self.id_list = id_list
        self.export_data_provider = export_data_provider
        self.main_window = main_window
        _, self.index_map = LanguageProvider.get_export_settings("exportDataProvider")
        self.connection_name = f"exportListPdfThread{id(self)}"

    def run_pdf_list_preview(self) -> None:
        db_connection = None
        try:
            print(self.connection_name)
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(False, "")
                return
            pdf_data = self.export_data_provider.get_pdf_list_data(db_connection, self.id_list, self.main_window)
            if not pdf_data:
                self.finished.emit(False, "")
                return
            print(pdf_data)
            self.finished.emit(True, "ok")
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit(False, "")
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
                QSqlDatabase.removeDatabase(self.connection_name)
