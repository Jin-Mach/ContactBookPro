from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def set_manadatory_model_headers(model: QSqlTableModel) -> None:
    headers_text = LanguageProvider.get_headers_text(model.objectName())
    headers_keys = headers_text.keys()
    try:
        for index, key in enumerate(headers_keys):
            model.setHeaderData(index, Qt.Orientation.Horizontal, headers_text[key])
    except Exception as e:
        ErrorHandler.exception_handler(e)