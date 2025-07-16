from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.ui.preview_widgets.qr_code_preview import QrCodePreviewDialog
from src.contacts.utilities.generate_qr_code import create_qr_code
from src.contacts.utilities.generate_vcard import create_vcard
from src.database.utilities.row_data_provider import RowDataProvider
from src.utilities.error_handler import ErrorHandler


def qr_code_preview(db_connection: QSqlDatabase, index: int, main_window: QMainWindow) -> None:
    try:
        row_data = RowDataProvider.return_row_data(db_connection, index)
        if not row_data:
            return
        vcard = create_vcard(row_data, main_window=main_window)
        if not vcard:
            return
        qr_code = create_qr_code(vcard, main_window=main_window)
        if not qr_code:
            return
        qr_preview_dialog = QrCodePreviewDialog(main_window)
        qr_preview_dialog.set_labels_texts(f"{row_data.get('first_name', '')}\n{row_data.get('second_name', '')}", qr_code)
        qr_preview_dialog.exec()
    except Exception as e:
        ErrorHandler.exception_handler(e, main_window)