from typing import Any

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from src.contacts.utilities.phone_utilities import format_phone_number
from src.utilities.error_handler import ErrorHandler


class StyledItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> Any:
        try:
            if not index.isValid():
                return
            value = index.data()
            if index.column() == 5:
                formated_number = format_phone_number(value)
                painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, formated_number)
                return
            super().paint(painter, option, index)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)