from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QLineEdit

from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.database.models.completer_model import CompleterModel


class CompleterControler:
    def __init__(self, query_model: CompleterModel, table_view: ContactsTableviewWidget, search_input: QLineEdit) -> None:
        self.query_model = query_model
        self.table_view = table_view
        self.search_input = search_input

    def setup(self) -> None:
        completer = self.get_completer()
        self.search_input.setCompleter(completer)
        self.search_input.textChanged.connect(self.update_completer)

    def get_completer(self) -> QCompleter:
        completer = QCompleter(self.query_model)
        completer.setCompletionColumn(0)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        return completer

    def update_completer(self) -> None:
        column = self.table_view.selectionModel().currentIndex().column()
        self.query_model.get_data(column, self.search_input)