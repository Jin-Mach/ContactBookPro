from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QLineEdit

from src.contacts.ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.database.models.completer_model import CompleterModel


class CompleterControler:
    def __init__(self, query_model: CompleterModel, table_view: ContactsTableviewWidget, search_input: QLineEdit) -> None:
        self.query_model = query_model
        self.table_view = table_view
        self.search_input = search_input
        self.completer_state = False
        self.search_input.textChanged.connect(lambda: self.change_state(False))

    def setup(self) -> None:
        self.completer = self.get_completer()
        self.search_input.setCompleter(self.completer)
        self.search_input.textChanged.connect(self.update_completer)

    def get_completer(self) -> QCompleter:
        completer = QCompleter(self.query_model)
        completer.setCompletionColumn(0)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.activated.connect(lambda: self.change_state(True))
        return completer

    def update_completer(self) -> None:
        self.state = False
        index = self.table_view.selectionModel().currentIndex()
        if index.isValid():
            self.query_model.get_data(index.column(), self.search_input)

    def change_state(self, state: bool) -> None:
        self.completer_state = state