from PyQt6.QtWidgets import QTableView


class ContactsTableviewWidget(QTableView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsTableviewWidget")