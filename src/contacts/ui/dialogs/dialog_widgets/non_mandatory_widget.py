from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QLayout

from src.contacts.ui.dialogs.dialog_widgets.personal_details_widget import PersonalDetailsWidget
from src.contacts.ui.dialogs.dialog_widgets.social_networks_widget import SocialNetworkWidget
from src.contacts.ui.dialogs.dialog_widgets.work_widget import WorkWidget
from src.utilities.language_provider import LanguageProvider


class NonMandatoryWidget(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogNonMandatoryWidget")
        self.work_widget = WorkWidget(self)
        self.social_networks_widget = SocialNetworkWidget(self)
        self.personal_details_widget = PersonalDetailsWidget(self)
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        self.dialog_tab_widget = QTabWidget(self)
        self.dialog_tab_widget.setObjectName("dialogTabWidget")
        self.dialog_tab_widget.addTab(self.work_widget, "")
        self.dialog_tab_widget.addTab(self.social_networks_widget, "")
        self.dialog_tab_widget.addTab(self.personal_details_widget, "")
        main_layout.addWidget(self.dialog_tab_widget)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        tab_text = ["work", "socialNetworks", "personalDetail"]
        for index, text in enumerate(tab_text):
            if text in ui_text:
                self.dialog_tab_widget.setTabText(index, ui_text[text])
            else:
                print("error")