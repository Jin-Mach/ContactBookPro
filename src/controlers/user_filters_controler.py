from src.contacts.contacts_ui.search_dialog.user_filters_dialog import UserFiltersDialog
from src.utilities.error_handler import ErrorHandler


class UserFiltersControler:
    def __init__(self, parent=None) -> None:
        self.parent= parent

    def show_user_filters_dialog(self) -> None:
        try:
            user_filters_dialog = UserFiltersDialog(self.parent)
            user_filters_dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)