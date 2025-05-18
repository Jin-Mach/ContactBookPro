from PyQt6.QtWidgets import QListView


class FiltersListviewWidget(QListView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)