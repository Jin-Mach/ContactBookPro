from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.database.database_utilities.row_data_provider import RowDataProvider
from src.utilities.error_handler import ErrorHandler


class ContactDataController:
    def __init__(self, detail_widget: ContactsDetailWidget) -> None:
        self.contacts_detail_widget = detail_widget

    def get_models_data(self, index: int, parent=None) -> None:
        try:
            data = RowDataProvider.return_row_data(index)
            self.contacts_detail_widget.personal_info_widget.set_data(data)
            self.contacts_detail_widget.tab_info_widget.set_data(data)
            self.contacts_detail_widget.notes_info_widget.set_data(data)
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)