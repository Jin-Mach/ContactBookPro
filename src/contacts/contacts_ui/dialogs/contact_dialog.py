from typing import Optional
from datetime import datetime

from PyQt6.QtWidgets import QDialog, QTabWidget, QLayout, QVBoxLayout, QDialogButtonBox

from src.contacts.contacts_ui.dialogs.dialog_widgets.mandatory_widget import MandatoryWidget
from src.contacts.contacts_ui.dialogs.dialog_widgets.non_mandatory_widget import NonMandatoryWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences,PyTypeChecker
class ContactDialog(QDialog):
    def __init__(self, update_contact: bool, contact_data: Optional[dict], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactDialog")
        self.setFixedSize(600, 600)
        self.update_contact = update_contact
        self.setLayout(self.create_gui())
        self.set_ui_text()
        if self.update_contact:
            self.set_contact_data(contact_data)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.dialog_tab_widget = QTabWidget()
        self.dialog_tab_widget.setObjectName("dialogTabWidget")
        self.mandatory_widget = MandatoryWidget(self.dialog_tab_widget, self)
        self.non_mandatory_widget = NonMandatoryWidget(self.dialog_tab_widget, self)
        self.dialog_tab_widget.addTab(self.mandatory_widget, "")
        self.dialog_tab_widget.addTab(self.non_mandatory_widget, "")
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.new_data)
        button_box.rejected.connect(self.reject)
        self.add_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.add_button.setObjectName("dialogAddContactButton")
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_button.setObjectName("dialogCancelButton")
        main_layout.addWidget(self.dialog_tab_widget)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_dialog_text(self.objectName())
        tab_text = ["mandatory", "nonMandatory"]
        widgets = [self.add_button, self.cancel_button]
        try:
            if "dialogTitle" in ui_text:
                self.setWindowTitle(ui_text["dialogTitle"])
            for index, text in enumerate(tab_text):
                if text in ui_text:
                    self.dialog_tab_widget.setTabText(index, ui_text[text])
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if widget.objectName() == "dialogAddContactButton" and self.update_contact:
                        widget.setText(ui_text[f"{widget.objectName()}Update"])
                    else:
                        widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def new_data(self) -> Optional[list]:
        try:
            mandatory_data = self.mandatory_widget.return_mandatory_data()
            work_data = self.non_mandatory_widget.work_widget.return_work_data()
            social_network_data = self.non_mandatory_widget.social_networks_widget.return_social_network_data()
            detail_data = self.non_mandatory_widget.personal_details_widget.return_personal_data()
            now = datetime.now().strftime("%d.%m.%Y")
            info_data = [now, now, None, None]
            if not all([mandatory_data, work_data, social_network_data, detail_data, info_data]):
                return None
            data = [mandatory_data, work_data, social_network_data, detail_data, info_data]
            super().accept()
            return data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def set_contact_data(self, data: dict) -> None:
        self.mandatory_widget.set_contact_data(data)
        self.non_mandatory_widget.work_widget.set_contact_data(data)
        self.non_mandatory_widget.social_networks_widget.set_contact_data(data)
        self.non_mandatory_widget.personal_details_widget.set_contact_data(data)