import pathlib

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.row_data_provider import RowDataProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class ExportContactPdfObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool, str)
    def __init__(self, db_path: str, index: int, row_data_provider: RowDataProvider,
                 main_window: QMainWindow):
        super().__init__()
        self.setObjectName("exportContactPdfObject")
        self.db_path = db_path
        self.index = index
        self.row_data_provider = row_data_provider
        self.main_window = main_window
        self.connection_name = f"exportContactPdfThread{id(self)}"
        _, self.index_map = LanguageProvider.get_export_settings("exportDataProvider")
        self.src_path = pathlib.Path(__file__).parent.parent.parent.parent

    def run_pdf_contact_export(self) -> None:
        db_connection = None
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(False, "")
                return
            contact_data = self.row_data_provider.return_row_data(db_connection, self.index)
            if not contact_data:
                self.finished.emit(False, "")
            file_path = self.src_path.parent.joinpath("output", "pdf_list.pdf")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            font_path = file_path.parent.parent.joinpath("fonts", "TimesNewRoman.ttf")
            self.create_pdf(contact_data)
            self.finished.emit(True, str(file_path))
        except Exception as e:
            print(e)
            self.error_message.emit(e)
            self.finished.emit(False, "")
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
                QSqlDatabase.removeDatabase(self.connection_name)

    def create_pdf(self, contact_data: dict[str, str]):
        print(self.index_map)