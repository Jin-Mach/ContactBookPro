from src.contacts.contacts_ui.search_dialog.advanced_search_dialog import AdvancedSearchDialog


class AdvancedSearchControler:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        
    def advanced_search(self) -> None:
        dialog = AdvancedSearchDialog(self.parent)
        dialog.exec()