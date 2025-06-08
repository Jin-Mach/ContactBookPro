from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtSql import QSqlTableModel

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ModelHeaderProvider:
    @staticmethod
    def set_mandatory_model_headers(model: QSqlTableModel, parent=None) -> None:
        try:
            headers = LanguageProvider.get_headers_text(model.objectName())
            for index, key in enumerate(headers.keys()):
                model.setHeaderData(index, Qt.Orientation.Horizontal, headers[key])
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)

    @staticmethod
    def set_advanced_filter_model_headers(model: QAbstractTableModel, parent=None) -> None:
        try:
            headers = LanguageProvider.get_headers_text(model.objectName())
            for index, key in enumerate(headers.keys()):
                model.setHeaderData(index, Qt.Orientation.Horizontal, headers[key])
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)