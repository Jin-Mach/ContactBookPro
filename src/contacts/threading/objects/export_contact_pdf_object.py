from io import BytesIO
from PIL import Image as PILImage
from typing import Any
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image, TableStyle, HRFlowable
from reportlab.platypus import Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PyQt6.QtCore import QObject, pyqtSignal, QByteArray
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.utilities.generate_qr_code import create_qr_code
from src.contacts.utilities.generate_vcard import create_vcard
from src.database.utilities.export_data_provider import ExportDataProvider
from src.utilities.language_provider import LanguageProvider


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
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            document = SimpleDocTemplate(str(self.pdf_path), leftMargin=10, rightMargin=10, topMargin=10, bottomMargin=10,
                                         pageSize=A4)
            story, error = ExportContactPdfObject.create_pdf(contact_data, ui_text)
            if error:
                self.error_message.emit(error)
                self.finished.emit(False)
                return
            document.build(story, onFirstPage=ExportContactPdfObject.create_color_row, onLaterPages=ExportContactPdfObject.create_color_row)
            self.finished.emit(True)
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit(False)
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
                QSqlDatabase.removeDatabase(self.connection_name)

    @staticmethod
    def create_pdf(contact_data: dict[str, Any], ui_text: dict[str, str]) -> tuple[list | None, Exception | None]:
        try:
            print(contact_data)
            mandatory_build = ExportContactPdfObject.create_mandatory_row(contact_data, ui_text)
            story = mandatory_build
            return story, None
        except Exception as e:
            print(e)
            return None, e

    @staticmethod
    def create_mandatory_row(contact_data: dict[str, Any], ui_text: dict[str, str]) -> list:
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="MyNameHeading", parent=styles["Heading2"],
                                  fontName="TimesNewRoman", fontSize=30, spaceAfter=10))
        styles.add(ParagraphStyle(name="MyContactHeading", parent=styles["Heading2"],
                                  fontName="TimesNewRoman", fontSize=15, spaceAfter=10))
        photo = ExportContactPdfObject.get_image_from_blob(contact_data.get('photo', None))
        if not photo:
            photo = Spacer(4 * cm, 4 * cm)
        first_name = Paragraph(f"{contact_data.get('first_name', '')}",styles["MyNameHeading"])
        second_name = Paragraph(f"{contact_data.get('second_name', '')}", styles["MyNameHeading"])
        data = [[photo, [first_name, second_name]]]
        table = Table(data)
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER')
        ]))
        email_paragraph = Paragraph(f"{ui_text.get('personalEmail', '')} {contact_data.get('personal_email', '')}",
                                    styles["MyContactHeading"])
        phone_paragraph = Paragraph(f"{ui_text.get('personalPhoneNumber', '')} {contact_data.get('personal_phone_number', '')}",
                                    styles["MyContactHeading"])
        story = [table, Spacer(1, 10), email_paragraph, phone_paragraph]
        return story

    @staticmethod
    def create_color_row(canvas: Canvas, document: SimpleDocTemplate) -> None:
        width, height = A4
        row_height = 150
        custom_blue = Color(0.267, 0.541, 1.0)
        canvas.setFillColor(custom_blue)
        canvas.rect(0, height - row_height, width, row_height, stroke=0, fill=1)

    @staticmethod
    def get_image_from_blob(photo_blob: bytes | None) -> Image | None:
        if photo_blob is None:
            return None
        try:
            blob_image = BytesIO(photo_blob)
            pil_image = PILImage.open(blob_image)
            pil_image.verify()
            blob_image.seek(0)
            return Image(blob_image, width=4*cm, height=4*cm)
        except IOError:
            return None

    @staticmethod
    def create_pdf_qr_code(contact_data: dict[str, Any]) ->Image | None:
        try:
            vcard = create_vcard(contact_data)
            qr_code = create_qr_code(vcard)
            if qr_code is None:
                return None
            image_to_bytearray = BytesIO()
            qr_code.save(image_to_bytearray, "PNG")
            image_to_bytearray.seek(0)
            qr_code_image = RLImage(image_to_bytearray, width=3*cm, height=3*cm)
            return qr_code_image
        except IOError:
            return None