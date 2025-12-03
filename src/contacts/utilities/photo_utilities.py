import pathlib

from PyQt6.QtCore import QStandardPaths, Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QLabel

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def set_contact_photo(photo_label: QLabel, photo_label_size: QSize, parent=None) -> None:
    default_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
    file_filter = ";;".join(set_dialog_filters(parent))
    try:
        photo_path, _ = QFileDialog.getOpenFileName(parent=parent, directory=default_path, filter=file_filter)
        if photo_path:
            pixmap = QPixmap(photo_path)
            if pixmap.isNull():
                return
            pixmap = pixmap.scaled(photo_label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            photo_label.setPixmap(pixmap)
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)

def reset_contact_photo(photo_label: QLabel, photo_label_size: QSize, parent=None) -> None:
    try:
        icon_path = pathlib.Path(__file__).parents[2].joinpath("icons", "dialogPersonalDetailWidget",
                                                                         "no_user_photo.png")

        if not icon_path.exists():
            photo_label.clear()
            return
        pixmap = QPixmap(str(icon_path))
        if pixmap.isNull():
            photo_label.clear()
            return
        pixmap = pixmap.scaled(photo_label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        photo_label.setPixmap(pixmap)
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)

def set_dialog_filters(parent=None) -> list:
    try:
        ui_text = LanguageProvider.get_json_text("dialog_text.json", "photoUtilities")
        filters = ["basicFilesFilter", "advancedFilesFilter", "allFilesFilter"]
        final_filter = []
        if ui_text:
            for filter_type in filters:
                if filter_type in ui_text:
                    final_filter.append(ui_text.get(filter_type, ""))
        return final_filter
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)
        return ["*.*"]