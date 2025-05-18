from src.contacts.contacts_ui.search_dialog.search_widgets.search_mandatory_widget import SearchMandatoryWidget
from src.contacts.contacts_ui.search_dialog.search_widgets.search_non_mandatory_widget import SearchNonMandatoryWidget
from src.utilities.error_handler import ErrorHandler


class FiltersControler:
    def __init__(self, search_mandatory_widget: SearchMandatoryWidget, search_non_mandatory_widget: SearchNonMandatoryWidget,
                 parent=None) -> None:
        self.search_mandatory_widget = search_mandatory_widget
        self.search_work_widget = search_non_mandatory_widget.search_work_widget
        self.search_social_networks_widget = search_non_mandatory_widget.search_social_networks_widget
        self.search_details_widget = search_non_mandatory_widget.search_details_widget
        self.parent = parent

    def show_active_filters(self) -> None:
        try:
            print(self.get_all_active_filters())
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
