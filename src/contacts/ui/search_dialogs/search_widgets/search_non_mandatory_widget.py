from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget

from src.contacts.ui.search_dialogs.search_widgets.search_details_widget import SearchDeatilsWidget
from src.contacts.ui.search_dialogs.search_widgets.search_social_networks_widget import \
    SearchSocialNetworksWidget
from src.contacts.ui.search_dialogs.search_widgets.search_work_widget import SearchWorkWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class SearchNonMandatoryWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("searchNonMandatoryWidget")
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.non_mandatory_tab_widget = QTabWidget()
        self.search_work_widget = SearchWorkWidget(self)
        self.search_social_networks_widget = SearchSocialNetworksWidget(self)
        self.search_details_widget = SearchDeatilsWidget(self)
        self.non_mandatory_tab_widget.setObjectName("nonMandatoryTabWidget")
        self.non_mandatory_tab_widget.addTab(self.search_work_widget, "")
        self.non_mandatory_tab_widget.addTab(self.search_social_networks_widget, "")
        self.non_mandatory_tab_widget.addTab(self.search_details_widget, "")
        main_layout.addWidget(self.non_mandatory_tab_widget)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            tab_text = ["work", "social", "detail"]
            if ui_text:
                for index, text in enumerate(tab_text):
                    if text in ui_text:
                        self.non_mandatory_tab_widget.setTabText(index, ui_text.get(text, ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)