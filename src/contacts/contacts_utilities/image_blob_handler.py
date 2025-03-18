from typing import Optional

from PyQt6.QtCore import QByteArray, QBuffer
from PyQt6.QtWidgets import QLabel

from src.utilities.error_handler import ErrorHandler


def image_to_blob(label: QLabel, parent=None) -> Optional[bytes]:
    try:
        pixmap = label.pixmap()
        if pixmap and not pixmap.isNull():
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.OpenModeFlag.WriteOnly)
            if not pixmap.save(buffer, "PNG"):
                return None
            return bytes(byte_array.data())
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)
