import sys

from typing import TYPE_CHECKING
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.utilities.phone_utilities import format_phone_number
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.database.utilities.contacts_utilities.export_data_provider import ExportDataProvider


# noinspection PyUnresolvedReferences
class ExportContactsListPdfObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool)

    def __init__(self, db_path: str, pdf_path: Path, id_list: list | None, export_data_provider: "ExportDataProvider",
                 main_window: QMainWindow) -> None:
        super().__init__()
        self.setObjectName("exportContactsListPdfObject")
        self.db_path = db_path
        self.pdf_path = pdf_path
        self.id_list = id_list
        self.export_data_provider = export_data_provider
        self.main_window = main_window
        self.connection_name = f"exportListPdfThread{id(self)}"
        self.project_path = Path(__file__).parents[4]

    def run_pdf_list_export(self) -> None:
        db_connection = None
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(False)
                return
            pdf_data = self.export_data_provider.get_pdf_list_data(db_connection, self.id_list, self.main_window)
            if not pdf_data:
                self.finished.emit(False)
                return
            font_path = self.project_path.joinpath("fonts", "TimesNewRoman.ttf")
            pdfmetrics.registerFont(TTFont("TimesNewRoman", str(font_path)))
            document = SimpleDocTemplate(str(self.pdf_path), leftMargin=50, rightMargin=50, topMargin=70, bottomMargin=50,
                                         pagesize=A4)
            story, error = ExportContactsListPdfObject.create_flowable_list(document, pdf_data)
            if error:
                self.error_message.emit(error)
                self.finished.emit(False)
                return
            document.build(story, onFirstPage=self.draw_header_footer, onLaterPages=self.draw_header_footer)
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
    def create_flowable_list(document: SimpleDocTemplate, contact_data: list[dict[str, str]]) -> tuple[list | None, Exception | None]:
        try:
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="MyHeading2", parent=styles["Heading2"], fontName="TimesNewRoman"))
            styles.add(ParagraphStyle(name="MyNormal", parent=styles["Normal"], fontName="TimesNewRoman"))
            styles.add(ParagraphStyle(name="HeaderStyle", parent=styles["MyHeading2"], textColor=colors.red))
            line_width = document.pagesize[0] - document.leftMargin - document.rightMargin
            story = []
            for contact in contact_data:
                header_paragraph = Paragraph(f"{contact.get('first_name', '')} {contact.get('second_name', '')} ",
                    styles["HeaderStyle"])
                gender_relationship_paragraph = Paragraph(f"({contact.get('gender', '')}, {contact.get('relationship', '')})",
                                                          styles["MyNormal"])
                email_paragraph = Paragraph(contact.get("personal_email", ""), styles["MyNormal"])
                formated_phone_number = format_phone_number(contact.get("personal_phone_number", ""))
                phone_paragraph = Paragraph(str(formated_phone_number), styles["MyNormal"])
                street = contact.get("personal_street", "")
                if not street:
                    address = f"{contact.get('personal_city', '')} {contact.get('personal_house_number', '')}"
                else:
                    address = f"{contact.get('personal_street', '')} {contact.get('personal_house_number', '')}"
                address_paragraph = Paragraph(
                    f"{address}, {contact.get('personal_city', '')}, "
                    f"{contact.get('personal_post_code', '')}, {contact.get('personal_country', '')}",
                    styles["MyNormal"]
                )
                contact_block = [
                    header_paragraph,
                    gender_relationship_paragraph,
                    email_paragraph,
                    phone_paragraph,
                    address_paragraph
                ]
                story.append(KeepTogether(contact_block))
                story.append(Spacer(1, 5))
                story.append(
                    HRFlowable(width=line_width, thickness=1, lineCap="round", color=colors.black, hAlign="CENTER",
                               spaceBefore=0, spaceAfter=0))
                story.append(Spacer(1, 5))
            return story, None
        except Exception as e:
            return None, e

    def draw_header_footer(self, canvas: Canvas, document: SimpleDocTemplate) -> None:
        self.draw_header(canvas, document)
        self.draw_footer(canvas, document)

    def draw_header(self, canvas: Canvas, document: SimpleDocTemplate) -> None:
        try:
            icon_path = self.project_path.joinpath("icons", "mainWindow", "mainWindowLogo.png")
            image = ImageReader(str(icon_path))
            image_width = 50
            image_height = 50
            x_pos = document.leftMargin
            y_pos = document.pagesize[1] - image_height - 20
            canvas.drawImage(image, x=x_pos, y=y_pos, width=image_width, height=image_height, preserveAspectRatio=True,
                             mask="auto")
            canvas.setStrokeColor(colors.black)
            canvas.setLineWidth(1)
            line_y = y_pos - 5
            canvas.line(document.leftMargin, line_y, document.pagesize[0] - document.rightMargin, line_y)
        except Exception as e:
            self.error_message.emit(e)

    def draw_footer(self, canvas: Canvas, document: SimpleDocTemplate) -> None:
        try:
            canvas.setStrokeColor(colors.black)
            canvas.setLineWidth(1)
            canvas.line(document.leftMargin, 20, document.pagesize[0] - document.rightMargin, 20)
            font = "TimesNewRoman"
            font_size = 10
            y_pos = 5
            left_x = document.leftMargin + 10
            current_time = datetime.now().strftime("%#d.%#m.%Y %H:%M")
            if sys.platform == "darwin":
                current_time = datetime.now().strftime("%-d.%-m.%Y %H:%M")
            canvas.setFont(font, font_size)
            canvas.drawString(left_x, y_pos, current_time)
            page = str(canvas.getPageNumber())
            page_width = canvas.stringWidth(page, font, font_size)
            pos_x = document.pagesize[0] / 2 - page_width
            canvas.drawString(pos_x, y_pos, page)
            right_x = document.pagesize[0] - document.rightMargin - 10
            application_name = LanguageProvider.get_json_text("ui_text.json", "mainWindow").get("mainWindowTitle", "")
            text_width = canvas.stringWidth(application_name, font, font_size)
            start_x = right_x - text_width
            canvas.drawString(start_x, y_pos, application_name)
        except Exception as e:
            self.error_message.emit(e)