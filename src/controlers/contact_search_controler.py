from PyQt6.QtWidgets import QLineEdit

from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.database.database_utilities.search_provider import SearchProvider
from src.database.models.mandatory_model import MandatoryModel
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ContactSearchControler:
    def __init__(self, mandatory_model: MandatoryModel, table_view: ContactsTableviewWidget, status_bar: ContactsStatusbarWidget,
                 parent=None) -> None:
        self.class_name = "contactSearchControler"
        self.mandatory_model = mandatory_model
        self.table_view = table_view
        self.status_bar = status_bar
        self.parent = parent
        self.error_text = LanguageProvider.get_error_text(self.class_name)

    def basic_search(self, search_input: QLineEdit) -> None:
        search_text = search_input.text().strip()
        filters = {
            "3": "first_name LIKE '%VALUE%' OR second_name LIKE '%VALUE%'",
            "4": "personal_email LIKE '%VALUE%'",
            "5": "personal_phone_number LIKE '%VALUE%'",
            "6": (
                "personal_city LIKE '%VALUE%' OR personal_street LIKE '%VALUE%' OR personal_house_number LIKE '%VALUE%' OR "
                "personal_post_code LIKE '%VALUE%' OR personal_country LIKE '%VALUE%'"
            )
        }
        try:
            if search_text:
                if self.table_view.selectionModel().hasSelection():
                    column_index = self.table_view.currentIndex().column()
                    new_filter = filters[str(column_index)].replace("VALUE", search_text)
                    SearchProvider.basic_search(self.mandatory_model, new_filter)
                    if self.mandatory_model.rowCount() < 1:
                        DialogsProvider.show_error_dialog(self.error_text["noFilteredData"])
                        SearchProvider.reset_filter(self.mandatory_model)
                        search_input.setFocus()
                    self.status_bar.set_count_text(self.mandatory_model.rowCount(), self.status_bar.contacts_total_count)
                else:
                    DialogsProvider.show_error_dialog(self.error_text["noTableviewSelection"], self.parent)
            else:
                DialogsProvider.show_error_dialog(self.error_text["emptySearchText"], self.parent)
                if self.parent:
                    self.parent.search_line_edit.setFocus()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def reset_filter(self, search_input: QLineEdit) -> None:
        ui_text = LanguageProvider.get_ui_text(self.parent.objectName())
        try:
            search_input.clear()
            search_input.setFocus()
            SearchProvider.reset_filter(self.mandatory_model)
            self.status_bar.set_count_text(self.mandatory_model.rowCount(), self.mandatory_model.rowCount())
            self.status_bar.contacts_total_count = self.mandatory_model.rowCount()
            if ui_text:
                self.parent.search_text_label.setText(ui_text[self.parent.search_text_label.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)