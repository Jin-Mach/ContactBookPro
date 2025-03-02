from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QLayout

from src.contacts.contacts_ui.dialogs.dialog_widgets.personal_details_widget import PersonalDetailsWidget
from src.contacts.contacts_ui.dialogs.dialog_widgets.social_networks_widget import SocialNetworkWidget
from src.contacts.contacts_ui.dialogs.dialog_widgets.work_widget import WorkWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class NonMandatoryWidget(QTabWidget):
    def __init__(self, tab_widget: QTabWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogNonMandatoryWidget")
        self.tab_widget = tab_widget
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        self.dialog_tab_widget = QTabWidget(self)
        self.dialog_tab_widget.setObjectName("nonMandatoryTabWidget")
        self.work_widget = WorkWidget(self.tab_widget, self.dialog_tab_widget, self)
        self.social_networks_widget = SocialNetworkWidget(self.tab_widget, self.dialog_tab_widget, self)
        self.personal_details_widget = PersonalDetailsWidget(self)
        self.dialog_tab_widget.addTab(self.work_widget, "")
        self.dialog_tab_widget.addTab(self.social_networks_widget, "")
        self.dialog_tab_widget.addTab(self.personal_details_widget, "")
        main_layout.addWidget(self.dialog_tab_widget)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        tab_text = ["work", "socialNetworks", "personalDetail"]
        try:
            for index, text in enumerate(tab_text):
                if text in ui_text:
                    self.dialog_tab_widget.setTabText(index, ui_text[text])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)