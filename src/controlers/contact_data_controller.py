from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.database.database_utilities.row_data_provider import RowDataProvider


class ContactDataController:
    def __init__(self, detail_widget: ContactsDetailWidget) -> None:
        self.contacts_detail_widget = detail_widget

    def get_models_data(self, index: int) -> None:
        data = RowDataProvider.return_row_data(index)
        if not data:
            print("contact data controler error")
            return
        self.contacts_detail_widget.personal_info_widget.set_data(data)
        self.contacts_detail_widget.tab_info_widget.set_data(data)
        self.contacts_detail_widget.notes_info_widget.set_data(data)