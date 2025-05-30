from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QMainWindow

from src.contacts.contacts_ui.search_dialog.active_filters_dialog import ActiveFiltersDialog
from src.contacts.contacts_ui.search_dialog.filter_name_dialog import FilterNameDialog
from src.contacts.contacts_ui.search_dialog.search_widgets.search_mandatory_widget import SearchMandatoryWidget
from src.contacts.contacts_ui.search_dialog.search_widgets.search_non_mandatory_widget import SearchNonMandatoryWidget
from src.contacts.contacts_ui.search_dialog.user_filters_dialog import UserFiltersDialog
from src.contacts.contacts_utilities.filters_provider import FiltersProvider
from src.contacts.contacts_utilities.get_main_window import get_main_window_instance
from src.database.models.advanced_filter_model import AdvancedFilterModel
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class FiltersControler:
    def __init__(self, search_mandatory_widget: SearchMandatoryWidget, search_non_mandatory_widget: SearchNonMandatoryWidget,
                 parent=None) -> None:
        self.class_name = "filtersControler"
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
                DialogsProvider.show_error_dialog(error_text["noActiveFilter"], self.parent)
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
                        DialogsProvider.show_error_dialog(error_text["existingFilterName"], self.parent)
                        return
                    main_window = get_main_window_instance()
                    if main_window:
                        main_window.tray_icon.show_notification(filter_name, "filterAdded")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_saved_filter(self, filter_name: str) -> None:
        try:
            FiltersProvider.remove_filter(filter_name)
            self.user_filters_dialog.user_filters_listwidget.set_filters_data(FiltersProvider.get_filters_data())
            main_window = get_main_window_instance()
            if main_window:
                main_window.tray_icon.show_notification(filter_name, "filterDeleted")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def show_user_filters(self) -> None:
        try:
            self.user_filters_dialog.user_filters_listwidget.set_filters_data(FiltersProvider.get_filters_data())
            self.user_filters_dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

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

    def remove_active_filter(self, row: int, model: QAbstractTableModel) -> None:
        try:
            self.active_filters_dialog.reset_active_filters_widgets(row, model)
            model.remove_row(row)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)