from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QAbstractItemView


class UserFiltersListwidget(QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("userFiltersListwidget")
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.sortItems(Qt.SortOrder.AscendingOrder)
        self.setSortingEnabled(True)