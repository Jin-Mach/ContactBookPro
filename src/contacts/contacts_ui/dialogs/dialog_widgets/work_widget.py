from typing import Optional

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit, QTabWidget

from src.contacts.contacts_utilities.contact_validator import ContactValidator
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class WorkWidget(QWidget):
    def __init__(self, main_tab: QTabWidget, non_mandatory_tab: QTabWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogWorkWidget")
        self.main_tab = main_tab
        self.non_mandatory_tab = non_mandatory_tab
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.set_validators()

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.dialog_work_email_text_label = QLabel()
        self.dialog_work_email_text_label.setObjectName("dialogWorkEmailTextLabel")
        self.dialog_work_email_edit = QLineEdit()
        self.dialog_work_email_edit.setObjectName("dialogWorkEmailEdit")
        self.dialog_work_phone_number_text_label = QLabel()
        self.dialog_work_phone_number_text_label.setObjectName("dialogWorkPhoneNumberTextLabel")
        self.dialog_work_phone_number_edit = QLineEdit()
        self.dialog_work_phone_number_edit.setObjectName("dialogPhoneNumberEdit")
        self.dialog_work_address_text_label = QLabel()
        self.dialog_work_address_text_label.setObjectName("dialogWorkAddressTextLabel")
        self.dialog_work_address_edit = QLineEdit()
        self.dialog_work_address_edit.setObjectName("dialogWorkAddressEdit")
        self.dialog_work_city_text_label = QLabel()
        self.dialog_work_city_text_label.setObjectName("dialogWorkCityTextLabel")
        self.dialog_work_city_edit = QLineEdit()
        self.dialog_work_city_edit.setObjectName("dialogWorkCityEdit")
        self.dialog_work_post_code_text_label = QLabel()
        self.dialog_work_post_code_text_label.setObjectName("dialogPostCodeTextLabel")
        self.dialog_work_post_code_edit = QLineEdit()
        self.dialog_work_post_code_edit.setObjectName("dialogPostCodeEdit")
        self.dialog_work_country_text_label = QLabel()
        self.dialog_work_country_text_label.setObjectName("dialogWorkCountryTextLabel")
        self.dialog_work_country_edit = QLineEdit()
        self.dialog_work_country_edit.setObjectName("dialogWorkCountryEdit")
        widgets = [
            (self.dialog_work_email_text_label, self.dialog_work_email_edit),
            (self.dialog_work_phone_number_text_label, self.dialog_work_phone_number_edit),
            (self.dialog_work_address_text_label, self.dialog_work_address_edit),
            (self.dialog_work_city_text_label, self.dialog_work_city_edit),
            (self.dialog_work_post_code_text_label, self.dialog_work_post_code_edit),
            (self.dialog_work_country_text_label, self.dialog_work_country_edit),
        ]
        for label, edit in widgets:
            main_layout.addRow(label, edit)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        widgets = self.findChildren((QLabel, QLineEdit))
        try:
            for widget in widgets:
                if isinstance(widget, QLabel):
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text[widget.objectName()])
                elif isinstance(widget, QLineEdit):
                    if widget.objectName() in ui_text:
                        widget.setPlaceholderText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_validators(self) -> None:
        phone_regex = QRegularExpression("^\\+[0-9]{1,14}$")
        phone_validator = QRegularExpressionValidator(phone_regex)
        self.dialog_work_phone_number_edit.setValidator(phone_validator)

    def return_work_data(self) -> Optional[list]:
        error_text = LanguageProvider.get_error_text(self.objectName())
        inputs = self.findChildren(QLineEdit)
        work_data = []
        try:
            for widget in inputs:
                text = widget.text().strip()
                if widget.objectName() == "dialogWorkEmailEdit" and text and not ContactValidator.validate_email(text):
                    DialogsProvider.show_error_dialog(error_text["emailValidatorError"], self)
                    self.set_tab_index()
                    widget.setFocus()
                    return None
                elif widget.objectName() == "dialogPhoneNumberEdit" and text and not ContactValidator.validate_phone_number(text):
                    DialogsProvider.show_error_dialog(error_text["phonenumberValidatorError"], self)
                    self.set_tab_index()
                    widget.setFocus()
                    return None
                work_data.append(text)
            return work_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tab_index(self) -> None:
        self.main_tab.setCurrentIndex(1)
        self.non_mandatory_tab.setCurrentIndex(0)