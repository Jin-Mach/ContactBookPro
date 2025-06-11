from PyQt6.QtCore import QByteArray, QBuffer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from src.utilities.error_handler import ErrorHandler


class BlobHandler:

    @staticmethod
    def pixmap_to_blob(label: QLabel, parent=None) -> bytes | None:
        try:
            pixmap = label.pixmap()
            if pixmap and not pixmap.isNull():
                byte_array = QByteArray()
                buffer = QBuffer(byte_array)
                buffer.open(QBuffer.OpenModeFlag.WriteOnly)
                if not pixmap.save(buffer, "PNG"):
                    return None
                return bytes(byte_array.data())
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)
            return None

    @staticmethod
    def blob_to_pixmap(blob: QByteArray, parent=None) -> QPixmap | None:
        try:
            if blob:
                pixmap = QPixmap()
                if pixmap.loadFromData(blob, "PNG"):
                    return pixmap
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)
            return None