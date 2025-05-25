from PyQt6.QtWidgets import QListWidget


class UserFiltersListwidgetWidget(QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)