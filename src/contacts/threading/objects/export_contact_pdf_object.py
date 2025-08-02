import pathlib

from io import BytesIO
from PIL import Image as PILImage
from typing import Any, TYPE_CHECKING
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.utilities.date_handler import format_date
from src.contacts.utilities.generate_qr_code import create_qr_code
from src.contacts.utilities.generate_vcard import create_vcard
from src.database.utilities.contacts_utilities.row_data_provider import RowDataProvider
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.database.utilities.contacts_utilities.export_data_provider import ExportDataProvider


# noinspection PyUnresolvedReferences
class ExportContactPdfObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool)
    def __init__(self, db_path: str, pdf_path: Path, index: int, export_data_provider: "ExportDataProvider",
                 main_window: QMainWindow):
        super().__init__()
        self.setObjectName("exportContactPdfObject")
        self.db_path = db_path
        self.pdf_path = pdf_path
        self.index = index
        self.export_data_provider = export_data_provider
        self.main_window = main_window
        self.connection_name = f"exportContactPdfThread{id(self)}"
        self.src_path = Path(__file__).parents[3]

    def run_pdf_contact_export(self) -> None:
        db_connection = None
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(False)
                return
            self.contact_data = self.export_data_provider.get_pdf_contact_data(db_connection, self.index, self.main_window)
            self.row_data = RowDataProvider.return_row_data(db_connection, self.index)
            if not self.contact_data:
                self.finished.emit(False)
                return
            font_path = self.src_path.parent.joinpath("fonts", "TimesNewRoman.ttf")
            pdfmetrics.registerFont(TTFont("TimesNewRoman", str(font_path)))
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            document = SimpleDocTemplate(str(self.pdf_path), leftMargin=10, rightMargin=10, topMargin=10, bottomMargin=10,
                                         pageSize=A4)
            story, error = ExportContactPdfObject.create_pdf(self.contact_data, ui_text)
            if error:
                self.error_message.emit(error)
                self.finished.emit(False)
                return
            document.build(story, onFirstPage=self.build_canvas, onLaterPages=self.build_canvas)
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
            basic_info = ExportContactPdfObject.create_basic_info(contact_data, ui_text)
            address_info = ExportContactPdfObject.create_address_info(contact_data, ui_text)
            work_info = ExportContactPdfObject.create_work_info(contact_data, ui_text)
            notes_info = ExportContactPdfObject.create_notes_info(contact_data, ui_text)
            story = []
            story.extend(basic_info)
            story.extend(address_info)
            story.extend(work_info)
            story.extend(notes_info)
            return story, None
        except Exception as e:
            return None, e

    @staticmethod
    def create_basic_info(contact_data: dict[str, Any], ui_text: dict[str, str]) -> list:
        try:
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="MyNameHeading", parent=styles["Heading2"],
                                      fontName="TimesNewRoman", fontSize=25, spaceBefore=0, spaceAfter=4, leading=25))
            styles.add(ParagraphStyle(name="ContactHeading", parent=styles["Heading2"],
                                      fontName="TimesNewRoman", fontSize=15, spaceAfter=10))
            styles.add(ParagraphStyle(name="ContactNormal", parent=styles["Normal"],
                                      fontName="TimesNewRoman", fontSize=12, spaceAfter=6, leading=15))
            styles.add(ParagraphStyle(name="TitleStyle", parent=styles["Normal"],
                                      fontName="TimesNewRoman", fontSize=12, spaceBefore=0, spaceAfter=2))
            styles.add(ParagraphStyle(name="BirthdayStyle", parent=styles["Normal"],
                                      fontName="TimesNewRoman", fontSize=12, spaceBefore=2, spaceAfter=0))
            photo = ExportContactPdfObject.get_image_from_blob(contact_data.get('photo', None))
            if not photo:
                photo = Spacer(4 * cm, 4 * cm)
            title = contact_data.get('title', '')
            birthday = contact_data.get('birthday', '')
            data = []
            if title:
                title_paragraph = Paragraph(title, styles["TitleStyle"])
                data.append(title_paragraph)
            first_name = Paragraph(f"{contact_data.get('first_name', '')}", styles["MyNameHeading"])
            second_name = Paragraph(f"{contact_data.get('second_name', '')}", styles["MyNameHeading"])
            data.append(first_name)
            data.append(second_name)
            if birthday:
                birthday = format_date(birthday)
                birthday_paragraph = Paragraph(birthday, styles["BirthdayStyle"])
                data.append(birthday_paragraph)
            final_data = [[photo, data]]
            table = Table(final_data)
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER')
            ]))
            contact_title = Paragraph(f"{ui_text.get('contactTitle', '')}", styles["ContactHeading"])
            email_paragraph = Paragraph(f"{ui_text.get('personalEmail', '')} {contact_data.get('personal_email', '')}",
                                        styles["ContactNormal"])
            phone_paragraph = Paragraph(f"{ui_text.get('personalPhoneNumber', '')} {contact_data.get('personal_phone_number', '')}",
                                        styles["ContactNormal"])
            story = [table, Spacer(1, 10), contact_title, email_paragraph, phone_paragraph, Spacer(1, 10),
                     HRFlowable(width="100%", thickness=1, color=colors.black)]
            return story
        except Exception as e:
            ExportContactPdfObject.error_message.emit(e)
            return []

    @staticmethod
    def create_address_info(contact_data: dict[str, Any], ui_text: dict[str, str]) -> list:
        try:
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="AddressHeading", parent=styles["Heading2"],
                                      fontName="TimesNewRoman", fontSize=15, spaceAfter=10))
            styles.add(ParagraphStyle(name="AddressNormal", parent=styles["Normal"],
                                      fontName="TimesNewRoman", fontSize=12, spaceAfter=6, leading=15))
            address_title = Paragraph(f"{ui_text.get('addressTitle', '')}", styles["AddressHeading"])
            street = contact_data.get('personal_street', '')
            if not street:
                address = f"{contact_data.get('personal_city', '')} {contact_data.get('personal_house_number', '')}"
            else:
                address = f"{street} {contact_data.get('personal_house_number', '')}"
            full_address_paragraph = Paragraph(f"{ui_text.get('personalAddress', '')} {address}, "
                                               f"{contact_data.get('personal_city', '')}, {contact_data.get('personal_post_code', '')}",
                                               styles["AddressNormal"])
            country_paragraph = Paragraph(f"{ui_text.get('personalCountry', '')} {contact_data.get('personal_country', '')}",
                                          styles["AddressNormal"])
            story = [address_title, full_address_paragraph, country_paragraph, Spacer(1, 10),
                     HRFlowable(width="100%", thickness=1, color=colors.black)]
            return story
        except Exception as e:
            ExportContactPdfObject.error_message.emit(e)
            return []

    @staticmethod
    def create_work_info(contact_data: dict[str, Any], ui_text: dict[str, str]) -> list:
        try:
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="WorkHeading", parent=styles["Heading2"], fontName="TimesNewRoman", fontSize=15,
                                      spaceAfter=10))
            styles.add(ParagraphStyle(name="WorkNormal", parent=styles["Normal"], fontName="TimesNewRoman", fontSize=12,
                                      spaceAfter=6))
            company = contact_data.get('company_name', '')
            email = contact_data.get('work_email', '')
            phone = contact_data.get('work_phone_number', '')
            country = contact_data.get('work_country', '')
            work_title = Paragraph(f"{ui_text.get('workTitle', '')}", styles["WorkHeading"])
            story = []
            if company:
                company_paragraph = Paragraph(f"{ui_text.get('workCompany', '')} {company}", styles["WorkNormal"])
                story.append(company_paragraph)
            if email:
                email_paragraph = Paragraph(f"{ui_text.get('workEmail', '')} {email}", styles["WorkNormal"])
                story.append(email_paragraph)
            if phone:
                phone_paragraph = Paragraph(f"{ui_text.get('workPhone', '')} {phone}", styles["WorkNormal"])
                story.append(phone_paragraph)
            if country:
                street = ui_text.get('work_street', '')
                if not street:
                    address = f"{contact_data.get('work_city', '')} {contact_data.get('work_house_number', '')}"
                else:
                    address = f"{street} {contact_data.get('work_house_number', '')}"
                full_address_paragraph = Paragraph(f"{ui_text.get('workAddress', '')} {address}, "
                                                   f"{contact_data.get('work_city', '')}, {contact_data.get('work_post_code', '')}",
                                                   styles["WorkNormal"])
                country_paragraph = Paragraph(f"{ui_text.get('workCountry', '')} {country}", styles["WorkNormal"])
                story.append(full_address_paragraph)
                story.append(country_paragraph)
            if story:
                story = [work_title] + story
                story += [Spacer(1, 10)]
                story += [HRFlowable(width="100%", thickness=1, color=colors.black)]
            return story
        except Exception as e:
            ExportContactPdfObject.error_message.emit(e)
            return []

    @staticmethod
    def create_notes_info(contact_data: dict[str, Any], ui_text: dict[str, str]) -> list:
        try:
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="NotesHeading", parent=styles["Heading2"], fontName="TimesNewRoman", fontSize=15,
                                      spaceAfter=10))
            styles.add(ParagraphStyle(name="NotesNormal", parent=styles["Normal"], fontName="TimesNewRoman", fontSize=12,
                                      leading=15, spaceAfter=6))
            notes_title = Paragraph(f"{ui_text.get('notesTitle', '')}", styles["NotesHeading"])
            notes_raw = contact_data.get('notes', '')
            story = []
            if notes_raw:
                lines = notes_raw.splitlines()
                story = [notes_title]
                for line in lines:
                    story.extend([Paragraph(f"{line}", styles["NotesNormal"])])
            return story
        except Exception as e:
            ExportContactPdfObject.error_message.emit(e)
            return []

    def build_canvas(self, canvas: Canvas, document: SimpleDocTemplate) -> None:
        try:
            row_data = self.row_data
            width, height = A4
            top_row_height = 150
            bottom_row_height = 70
            qr_size = 2*cm
            custom_color = Color(0.267, 0.541, 1.0)
            gender = row_data.get('gender', '')
            if gender:
                if int(gender) == 2:
                    custom_color = Color(0.91, 0.67, 0.72)
            canvas.setFillColor(custom_color)
            canvas.rect(0, height - top_row_height, width, top_row_height, stroke=0, fill=1)
            canvas.rect(0, 0, width, bottom_row_height, stroke=0, fill=1)
            qr_code = ExportContactPdfObject.create_pdf_qr_code(self.contact_data)
            if qr_code:
                image_reader = ImageReader(qr_code)
                canvas.drawImage(image_reader, width - qr_size - 10, 10, width=qr_size, height=qr_size)
        except Exception as e:
            ExportContactPdfObject.error_message.emit(e)


    @staticmethod
    def get_image_from_blob(photo_blob: bytes | None) -> Image | None:
        try:
            if photo_blob is None:
                icon_path = pathlib.Path(__file__).parents[4].joinpath("icons", "exportContactPdfObject", "noContactImage.png")
                if icon_path.exists():
                    return Image(str(icon_path), width=4*cm, height=4*cm)
                return None
            blob_image = BytesIO(photo_blob)
            pil_image = PILImage.open(blob_image)
            pil_image.verify()
            blob_image.seek(0)
            return Image(blob_image, width=4*cm, height=4*cm)
        except IOError:
            return None

    @staticmethod
    def create_pdf_qr_code(contact_data: dict[str, Any]) -> BytesIO| None:
        try:
            vcard = create_vcard(contact_data)
            qr_code = create_qr_code(vcard)
            if qr_code is None:
                return None
            image_to_bytearray = BytesIO()
            qr_code.save(image_to_bytearray, "PNG")
            image_to_bytearray.seek(0)
            return image_to_bytearray
        except IOError:
            return None