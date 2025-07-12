from typing import Any
from pathlib import Path

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.export_data_provider import ExportDataProvider


# noinspection PyUnresolvedReferences
class ExportContactPdfObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool)
    def __init__(self, db_path: str, pdf_path: Path, index: int, export_data_provider: ExportDataProvider,
                 main_window: QMainWindow):
        super().__init__()
        self.setObjectName("exportContactPdfObject")
        self.db_path = db_path
        self.pdf_path = pdf_path
        self.index = index
        self.export_data_provider = export_data_provider
        self.main_window = main_window
        self.connection_name = f"exportContactPdfThread{id(self)}"
        self.src_path = Path(__file__).parent.parent.parent.parent

    def run_pdf_contact_export(self) -> None:
        db_connection = None
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(False)
                return
            contact_data = self.export_data_provider.get_pdf_contact_data(db_connection, self.index, self.main_window)
            if not contact_data:
                self.finished.emit(False)
                return
            font_path = self.src_path.parent.joinpath("fonts", "TimesNewRoman.ttf")
            pdfmetrics.registerFont(TTFont("TimesNewRoman", str(font_path)))
            self.create_pdf(str(self.pdf_path), contact_data)
            self.finished.emit(True)
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit(False)
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
                QSqlDatabase.removeDatabase(self.connection_name)

    def create_pdf(self, pdf_path: str, contact_data: dict[str, Any]) -> None:
        try:
            print(contact_data)
            canvas = Canvas(pdf_path, pagesize=A4)
            canvas.setFont("TimesNewRoman", 15)
            canvas.save()
        except Exception as e:
            self.error_message.emit(e)