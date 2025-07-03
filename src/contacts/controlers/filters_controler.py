from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QDialog

from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.ui.search_dialogs.active_filters_dialog import ActiveFiltersDialog
from src.contacts.ui.search_dialogs.filter_name_dialog import FilterNameDialog
from src.contacts.ui.search_dialogs.search_widgets.search_mandatory_widget import SearchMandatoryWidget
from src.contacts.ui.search_dialogs.search_widgets.search_non_mandatory_widget import SearchNonMandatoryWidget
from src.contacts.ui.search_dialogs.user_filters_dialog import UserFiltersDialog
from src.contacts.utilities.filters_provider import FiltersProvider
from src.contacts.utilities.instance_provider import InstanceProvider
from src.database.models.advanced_filter_model import AdvancedFilterModel
from src.database.models.mandatory_model import MandatoryModel
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class FiltersController:
    def __init__(self, search_mandatory_widget: SearchMandatoryWidget, search_non_mandatory_widget: SearchNonMandatoryWidget,
                 parent=None) -> None:
        self.class_name = "filtersController"
        self.search_mandatory_widget = search_mandatory_widget
        self.search_non_mandatory_widget = search_non_mandatory_widget
        self.search_work_widget = self.search_non_mandatory_widget.search_work_widget
        self.search_social_networks_widget = self.search_non_mandatory_widget.search_social_networks_widget
        self.search_details_widget = self.search_non_mandatory_widget.search_details_widget
        self.parent = parent
        self.user_filters_dialog = UserFiltersDialog(delete_filter=self.delete_saved_filter, parent=self.parent)
        self.user_filters_dialog.user_filters_listwidget.set_filters_data(FiltersProvider.get_filters_data())

    def show_active_filters(self) -> None:
        try:
            if not self.get_all_active_filters():
                error_text = LanguageProvider.get_error_text(self.class_name)
                DialogsProvider.show_error_dialog(error_text.get("noActiveFilter", ""), self.parent)
                return
            advanced_filter_model = AdvancedFilterModel(self.get_all_active_filters(), self.parent)
            self.active_filters_dialog = ActiveFiltersDialog(advanced_filter_model, self.remove_active_filter,
                                                             self.search_mandatory_widget, self.search_non_mandatory_widget,
                                                             self.parent)
            self.active_filters_dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def save_filter(self) -> None:
        try:
            filter_dialog = FilterNameDialog(self.parent)
            if filter_dialog.exec() == QDialog.DialogCode.Accepted:
                filter_name = filter_dialog.get_filter_name()
                advanced_dialog = self.parent.parent()
                if advanced_dialog and advanced_dialog.objectName() == "advancedSearchDialog":
                    status, result = FiltersProvider.add_new_filter(filter_name, advanced_dialog.get_finall_filter())
                    if not status and result == "exists":
                        error_text = LanguageProvider.get_error_text(self.class_name)
                        DialogsProvider.show_error_dialog(error_text.get("existingFilterName", ""), self.parent)
                        return
                    main_window = InstanceProvider.get_main_window_instance()
                    if main_window:
                        main_window.tray_icon.show_notification(filter_name, "filterAdded")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_saved_filter(self, filter_name: str) -> None:
        try:
            FiltersProvider.remove_filter(filter_name)
            self.user_filters_dialog.user_filters_listwidget.set_filters_data(FiltersProvider.get_filters_data())
            main_window = InstanceProvider.get_main_window_instance()
            if main_window:
                main_window.tray_icon.show_notification(filter_name, "filterDeleted")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def show_user_filters(self, db_connection: QSqlDatabase, mandatory_model: MandatoryModel, status_bar: ContactsStatusbarWidget) -> None:
        try:
            filters = FiltersProvider.get_filters_data()
            if not filters:
                error_text = LanguageProvider.get_error_text(self.class_name)
                DialogsProvider.show_error_dialog(error_text.get("noUserFilters", ""), self.parent)
                return
            from src.contacts.controlers.advanced_search_controler import AdvancedSearchController
            advanced_search_controller = AdvancedSearchController(db_connection, mandatory_model, status_bar)
            self.user_filters_dialog.user_filters_listwidget.set_filters_data(filters)
            if self.user_filters_dialog.exec() == QDialog.DialogCode.Accepted:
                selected_filter = self.user_filters_dialog.check_selected_filter()
                new_filter = FiltersProvider.return_selected_filter(selected_filter)
                advanced_search_controller.apply_saved_filter(new_filter)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def get_all_active_filters(self) -> list:
        try:
            active_filters = []
            active_filters.extend(self.search_mandatory_widget.return_mandatory_current_filter())
            active_filters.extend(self.search_work_widget.return_work_current_filter())
            active_filters.extend(self.search_social_networks_widget.return_social_networks_current_filter())
            active_filters.extend(self.search_details_widget.return_details_current_filter())
            return active_filters
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return []

    def remove_active_filter(self, row: int, model: AdvancedFilterModel) -> None:
        try:
            self.active_filters_dialog.reset_active_filters_widgets(row, model)
            model.remove_row(row)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)