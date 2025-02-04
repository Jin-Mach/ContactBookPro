from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QLayout

from src.contacts.ui.dialogs.dialog_widgets.personal_details_widget import PersonalDetailsWidget
from src.contacts.ui.dialogs.dialog_widgets.social_networks_widget import SocialNetworkWidget
from src.contacts.ui.dialogs.dialog_widgets.work_widget import WorkWidget


class NonMandatoryWidget(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogNonMandatoryWidget")
        self.work_widget = WorkWidget(self)
        self.social_networks_widget = SocialNetworkWidget(self)
        self.personal_details_widget = PersonalDetailsWidget(self)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        dialog_tab_widget = QTabWidget(self)
        dialog_tab_widget.setObjectName("dialogTabWidget")
        self.work_tab_text = "work"
        self.social_networks_text = "social networks"
        self.personal_details_text = "personal details"
        dialog_tab_widget.addTab(self.work_widget, self.work_tab_text)
        dialog_tab_widget.addTab(self.social_networks_widget, self.social_networks_text)
        dialog_tab_widget.addTab(self.personal_details_widget, self.personal_details_text)
        main_layout.addWidget(dialog_tab_widget)
        return main_layout