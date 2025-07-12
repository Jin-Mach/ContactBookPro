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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image, TableStyle
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
            document = SimpleDocTemplate(str(self.pdf_path), leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
                                         pageSize=A4)
            story, error = ExportContactPdfObject.create_pdf(contact_data, ui_text)
            if error:
                self.error_message.emit(error)
                self.finished.emit(False)
                return
            document.build(story, onFirstPage=ExportContactPdfObject.create_color_column)
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
            story = []
            mandatory_column = ExportContactPdfObject.build_mandatory_column(contact_data, ui_text)
            non_mandatory_column = ""
            table_data = [[mandatory_column, non_mandatory_column]]
            table = Table(table_data, colWidths=[200, 350])
            table.setStyle(TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.5, colors.red),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.blue),
            ]
            ))
            story.append(table)
            return story, None
        except Exception as e:
            return None, e

    @staticmethod
    def build_mandatory_column(contact_data: dict[str, Any], ui_text: dict[str, str]) -> Table:
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="MyHeading2", parent=styles["Heading2"], fontName="TimesNewRoman", fontSize=20,
                                  alignment=0))
        styles.add(ParagraphStyle(name="MyNormal", parent=styles["Normal"], fontName="TimesNewRoman", fontSize=15,
                                  alignment=0))
        spacer_normal = Spacer(1, 5)
        spacer_between = Spacer(1, 15)
        photo = contact_data.get('photo', None)
        if isinstance(photo, QByteArray):
            photo = bytes(photo)
        contact_image = ExportContactPdfObject.get_image_from_blob(photo)
        if not contact_image:
            contact_image = Spacer(1, 5 * cm)
        street = ui_text.get('personal_street', '')
        if not street:
            address = f"{contact_data.get('personal_city', '')} {contact_data.get('personal_house_number', '')}"
        else:
            address = f"{street} {contact_data.get('personal_house_number', '')}"
        qr_image = ExportContactPdfObject.create_pdf_qr_code(contact_data)
        if qr_image is None:
            qr_image = Spacer(1, 3 * cm)
        rows = [
            ("image", contact_image),
            ("spacer", Spacer(1, 30)),
            ("title", ui_text.get('mandatoryColumnContactTitle', '')),
            ("normal", contact_data.get('personal_email', '')),
            ("spacer", spacer_normal),
            ("normal", contact_data.get('personal_phone_number', '')),
            ("spacer", spacer_between),
            ("title", ui_text.get('mandatoryColumnAddressTitle', '')),
            ("normal", address),
            ("spacer", spacer_normal),
            ("normal", contact_data.get('personal_city', '')),
            ("spacer", spacer_normal),
            ("normal", contact_data.get('personal_post_code', '')),
            ("spacer", spacer_normal),
            ("normal", contact_data.get('personal_country', '')),
            ("spacer", spacer_between),
        ]
        birthday = contact_data.get('birthday', '')
        if birthday:
            rows.extend([
                ("title", ui_text.get('mandatoryColumnBirthdayTitle', "")),
                ("normal", birthday),
            ])
        rows.append(("spacer", Spacer(1, 7 * cm)))
        rows.append(("image", qr_image))
        data = []
        for kind, value in rows:
            if kind == "title":
                data.append([Paragraph(value, styles["MyHeading2"])])
            elif kind == "normal":
                data.append([Paragraph(value, styles["MyNormal"])])
            elif kind == "spacer":
                data.append([value])
            elif kind == "image":
                data.append([value])
        table = Table(data)
        table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (0, 0), "CENTER"),
            ("ALIGN", (0, len(data) - 1), (0, len(data) - 1), "CENTER"),
        ]))
        return table

    @staticmethod
    def create_color_column(canvas: Canvas, document: SimpleDocTemplate) -> None:
        x = 0
        y = 0
        width, height = A4
        custom_blue = Color(0.267, 0.541, 1.0)
        canvas.setFillColor(custom_blue)
        canvas.rect(x, y, 222, height, stroke=0, fill=1)

    @staticmethod
    def get_image_from_blob(photo_blob: bytes | None) -> Image | None:
        if photo_blob is None:
            return None
        try:
            blob_image = BytesIO(photo_blob)
            pil_image = PILImage.open(blob_image)
            pil_image.verify()
            blob_image.seek(0)
            return Image(blob_image, width=5*cm, height=5*cm)
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