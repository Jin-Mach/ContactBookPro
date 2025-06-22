import vobject
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QFileDialog

from src.database.utilities.row_data_provider import RowDataProvider
from src.utilities.encoding_provider import get_encoding
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def export_to_vcard(db_connection: QSqlDatabase, index: int, main_window: QMainWindow) -> None:
    try:
        menu_text = LanguageProvider.get_context_menu_text("vcardExportControler")
        contact_row_data = RowDataProvider.return_row_data(db_connection, index)
        if not contact_row_data:
            return
        file_name,_ = QFileDialog.getSaveFileName(parent=main_window, directory=QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),
                                                  filter=menu_text.get("vcardFilter", ""))
        if file_name:
            with open(file_name, "w", encoding=get_encoding()) as file:
                file.write(create_vcard_object(contact_row_data))
                main_window.tray_icon.show_notification("Export vCard", "exportSaved")
    except Exception as e:
        ErrorHandler.exception_handler(e, main_window)

def create_vcard_object(new_row_data: dict) -> str:
    row_data = new_row_data
    vcard = vobject.vCard()
    personal_name = vcard.add("n")
    personal_name.value = vobject.vcard.Name(
        given = row_data.get("first_name", ""),
        family = row_data.get("second_name", "")
    )
    personal_email = vcard.add("email")
    personal_email.value = row_data.get("personal_email", "")
    personal_email.params["TYPE"] = ["HOME"]
    personal_phone_number = vcard.add("tel")
    personal_phone_number.value = row_data.get("personal_phone_number", "")
    personal_phone_number.params["TYPE"] = ["MAIN"]
    contact_street = row_data.get("personal_house_number", "")
    if row_data.get("personal_street"):
        contact_street = f"{row_data.get('personal_street', '')} {row_data.get('personal_house_number', '')}"
    personal_address = vcard.add("adr")
    personal_address.value = vobject.vcard.Address(
        street = contact_street,
        city = row_data.get("personal_city", ""),
        code = row_data.get("personal_post_code", ""),
        country = row_data.get("personal_country", ""),
        box = "",
        extended = "",
        region = ""
    )
    personal_address.params["TYPE"] = ["HOME"]
    return vcard.serialize()