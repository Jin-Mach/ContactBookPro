from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

from src.database.utilities.model_header_provider import ModelHeaderProvider


class AdvancedFilterModel(QAbstractTableModel):
    def __init__(self, filter_data: list, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("advancedFilterModel")
        self.filter_data = filter_data
        self.headers = {}

    def columnCount(self, parent=QModelIndex) -> int:
        return 5

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.filter_data)

    def setHeaderData(self, section: int, orientation: Qt.Orientation, value: Any, role=Qt.ItemDataRole.DisplayRole) -> bool:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            self.headers[section] = value
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section in self.headers:
                return self.headers[section]
            return ""
        return None

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            filter_item = self.filter_data[index.row()]
            label_text = filter_item["label_text"].rstrip(":")
            operator_text = filter_item["combobox_text"].lower()
            edit_text = filter_item["edit_text"]
            combobox = filter_item["combobox"]
            edit = filter_item["edit"]
            if index.column() == 0:
                return label_text
            elif index.column() == 1:
                return operator_text
            if edit:
                if index.column() == 2:
                    if edit_text:
                        return edit_text
                    return None
                elif index.column() == 3:
                    return f"{combobox.objectName()}, {edit.objectName()}"
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        return None

    def remove_row(self, row: int) -> None:
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.filter_data[row]
        self.endRemoveRows()