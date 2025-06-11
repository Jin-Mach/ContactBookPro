import pathlib
from datetime import datetime

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QTabWidget, QLayout, QVBoxLayout, QDialogButtonBox, QPushButton

from src.contacts.ui.contacts_dialog.dialog_widgets.mandatory_widget import MandatoryWidget
from src.contacts.ui.contacts_dialog.dialog_widgets.non_mandatory_widget import NonMandatoryWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences,PyTypeChecker
class ContactDialog(QDialog):
    def __init__(self, update_contact: bool, contact_data: dict | None, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactDialog")
        self.setFixedSize(600, 600)
        self.setWindowIcon(QIcon(str(pathlib.Path(__file__).parent.parent.parent.parent.joinpath("icons", "mainWindow", "window_icon.png"))))
        self.update_contact = update_contact
        self.setLayout(self.create_gui())
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            self.buttons = button_box.findChildren(QPushButton)
        self.set_ui_text()
        self.set_tooltips_text()
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
        button_box.accepted.connect(self.get_data)
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
        try:
            if "dialogTitle" in ui_text and "dialogTitleUpdate" in ui_text:
                if self.update_contact:
                    self.setWindowTitle(ui_text["dialogTitleUpdate"])
                else:
                    self.setWindowTitle(ui_text["dialogTitle"])
            for index, text in enumerate(tab_text):
                if text in ui_text:
                    self.dialog_tab_widget.setTabText(index, ui_text[text])
            for widget in self.buttons:
                if widget.objectName() in ui_text:
                    if widget.objectName() == "dialogAddContactButton" and self.update_contact:
                        widget.setText(ui_text[f"{widget.objectName()}Update"])
                    else:
                        widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
        try:
            for button in self.buttons:
                if button.objectName() in tooltips_text:
                    if button.objectName() == "dialogAddContactButton" and self.update_contact:
                        button.setToolTip(tooltips_text[f"{button.objectName()}Update"])
                        button.setToolTipDuration(5000)
                    else:
                        button.setToolTip(tooltips_text[button.objectName()])
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def colect_data(self) -> list | None:
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

    def get_data(self) -> None:
        if self.colect_data():
            self.colected_data = self.colect_data()
            self.accept()

    def set_contact_data(self, data: dict) -> None:
        self.mandatory_widget.set_contact_data(data)
        self.non_mandatory_widget.work_widget.set_contact_data(data)
        self.non_mandatory_widget.social_networks_widget.set_contact_data(data)
        self.non_mandatory_widget.personal_details_widget.set_contact_data(data)