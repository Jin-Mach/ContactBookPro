from PyQt6.QtWidgets import QLineEdit, QComboBox

from src.contacts.controlers.completer_controller import CompleterController
from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.contacts.utilities.optimalize_data import normalize_input
from src.database.models.mandatory_model import MandatoryModel
from src.database.utilities.search_provider import SearchProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ContactSearchController:
    def __init__(self, controller: CompleterController, mandatory_model: MandatoryModel, table_view: ContactsTableviewWidget,
                 contacts_statusbar: ContactsStatusbarWidget, search_combobox: QComboBox, parent=None) -> None:
        self.class_name = "contactSearchController"
        self.controller = controller
        self.mandatory_model = mandatory_model
        self.table_view = table_view
        self.contacts_statusbar = contacts_statusbar
        self.search_combobox = search_combobox
        self.parent = parent
        self.error_text = LanguageProvider.get_error_text(self.class_name)
        self.index_error_text = LanguageProvider.get_error_text("widgetErrors")
        self.new_filter = None

    def basic_search(self, search_input: QLineEdit) -> None:
        search_text = normalize_input(search_input)
        self.new_filter = None
        filters = {
            "1": "gender VALUE",
            "2": "relationship VALUE",
            "3": "first_name_normalized LIKE '%VALUE%' OR second_name_normalized LIKE '%VALUE%'",
            "4": "personal_email LIKE '%VALUE%'",
            "5": "personal_phone_number LIKE '%VALUE%'",
            "6": (
                "personal_city_normalized LIKE '%VALUE%' OR personal_street_normalized LIKE '%VALUE%' OR personal_house_number LIKE '%VALUE%' OR "
                "personal_post_code LIKE '%VALUE%' OR personal_country_normalized LIKE '%VALUE%'"
            )
        }
        try:
            if self.table_view.selectionModel().hasSelection():
                column_index = self.table_view.currentIndex().column()
                combobox_index = self.search_combobox.currentIndex()
                if column_index in (1, 2):
                    if combobox_index == 0:
                        self.new_filter = filters.get(str(column_index), "").replace("VALUE", "LIKE '%'")
                    else:
                        self.new_filter = filters.get(str(column_index), "").replace("VALUE", f"= {str(combobox_index)}")
                else:
                    if search_text:
                        if column_index == 3:
                            self.new_filter = self.return_multicolumn_filter(search_text, ["first_name_normalized",
                                                                                           "second_name_normalized"])
                        elif column_index == 6:
                            self.new_filter = self.return_multicolumn_filter(search_text, ["personal_city_normalized",
                                                                                           "personal_street_normalized",
                                                                                           "personal_house_number", "personal_post_code",
                                                                                           "personal_country_normalized"])
                        else:
                            self.new_filter = filters.get(str(column_index), "").replace("VALUE", search_text)
                    else:
                        DialogsProvider.show_error_dialog(self.error_text.get("emptySearchText", ""), self.parent)
                        if self.parent:
                            self.parent.search_line_edit.setFocus()
                if self.new_filter:
                    if column_index in (1, 2) or search_text:
                        SearchProvider.basic_search(self.mandatory_model, self.new_filter)
                        if self.mandatory_model.rowCount() < 1:
                            DialogsProvider.show_error_dialog(self.error_text.get("noFilteredData", ""))
                            SearchProvider.reset_filter(self.mandatory_model)
                            search_input.setFocus()
                        self.contacts_statusbar.set_count_text(self.mandatory_model.rowCount(), 0)
                    else:
                        DialogsProvider.show_error_dialog(self.error_text.get("emptySearchText", ""), self.parent)
                        if self.parent:
                            self.parent.search_line_edit.setFocus()
            else:
                DialogsProvider.show_error_dialog(self.error_text.get("noTableviewSelection", ""), self.parent)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def reset_filter(self, search_input: QLineEdit) -> None:
        ui_text = LanguageProvider.get_ui_text(self.parent.objectName())
        try:
            self.search_combobox.setDisabled(True)
            search_input.clear()
            search_input.setDisabled(True)
            SearchProvider.reset_filter(self.mandatory_model)
            self.contacts_statusbar.set_count_text(self.mandatory_model.rowCount(), 0)
            self.contacts_statusbar.contacts_total_count = self.mandatory_model.rowCount()
            if ui_text:
                self.parent.search_text_label.setText(ui_text.get(self.parent.search_text_label.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def return_multicolumn_filter(self, search_text: str, columns: list[str]) -> str:
        prepared_text = search_text.split()
        filter_operator = " OR "
        filter_list = []
        column_index = self.table_view.currentIndex().column()
        if column_index > -1:
            if not self.controller.completer_state:
                for word in prepared_text:
                    for column_name in columns:
                        save_word = word.replace("'", "''")
                        filter_list.append(f"{column_name} LIKE '%{save_word}%'")
                return filter_operator.join(filter_list)
            if column_index == 3:
                return self.set_name_filter(prepared_text)
            elif column_index == 6:
                return self.set_address_filter(search_text)
            return ""
        else:
            DialogsProvider.show_error_dialog(self.index_error_text.get("indexError", ""), self.parent)
            return ""

    @staticmethod
    def set_name_filter(splitted_text: list) -> str:
        return f"first_name_normalized = '{splitted_text[0]}' AND second_name_normalized = '{splitted_text[1]}'"

    @staticmethod
    def set_address_filter(search_text: str) -> str:
        split_text = search_text.split(",")
        prepared_text = [part.strip() for part in split_text]
        return (f"personal_city_normalized = '{prepared_text[0]}' AND "
                f"personal_house_number = '{prepared_text[-3]}' AND "
                f"personal_post_code = '{prepared_text[-2]}' AND "
                f"personal_country_normalized = '{prepared_text[-1]}'")