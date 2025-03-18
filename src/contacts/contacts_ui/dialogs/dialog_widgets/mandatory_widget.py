from typing import Optional

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QTabWidget

from src.contacts.contacts_utilities.contact_validator import ContactValidator
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class MandatoryWidget(QWidget):
    def __init__(self, main_tab_widget: QTabWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogMandatoryWidget")
        self.main_tab_widget = main_tab_widget
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.set_validators()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.dialog_gender_text_label = QLabel()
        self.dialog_gender_text_label.setObjectName("dialogGenderTextLabel")
        self.dialog_gender_combobox = QComboBox()
        self.dialog_gender_combobox.setObjectName("dialogGenderCombobox")
        self.dialog_gender_combobox.setFixedWidth(200)
        self.dialog_relationship_text_label = QLabel()
        self.dialog_relationship_text_label.setObjectName("dialogRelationshipTextLabel")
        self.dialog_relationship_combobox = QComboBox()
        self.dialog_relationship_combobox.setObjectName("dialogRelationshipCombobox")
        self.dialog_relationship_combobox.setFixedWidth(200)
        self.dialog_first_name_text_label = QLabel()
        self.dialog_first_name_text_label.setObjectName("dialogFirstNameTextLabel")
        self.dialog_first_name_edit = QLineEdit()
        self.dialog_first_name_edit.setObjectName("dialogFirstNameEdit")
        self.dialog_second_name_text_label = QLabel()
        self.dialog_second_name_text_label.setObjectName("dialogSecondNameTextLabel")
        self.dialog_second_name_edit = QLineEdit()
        self.dialog_second_name_edit.setObjectName("dialogSecondNameEdit")
        self.dialog_email_text_label = QLabel()
        self.dialog_email_text_label.setObjectName("dialogEmailTextLabel")
        self.dialog_email_edit = QLineEdit()
        self.dialog_email_edit.setObjectName("dialogEmailEdit")
        self.dialog_phone_number_text_label = QLabel()
        self.dialog_phone_number_text_label.setObjectName("dialogPhoneNumberTextLabel")
        self.dialog_phone_number_edit = QLineEdit()
        self.dialog_phone_number_edit.setObjectName("dialogPhoneNumberEdit")
        self.dialog_address_text_label = QLabel()
        self.dialog_address_text_label.setObjectName("dialogAddressTextLabel")
        self.dialog_address_edit = QLineEdit()
        self.dialog_address_edit.setObjectName("dialogAddressEdit")
        self.dialog_city_text_label = QLabel()
        self.dialog_city_text_label.setObjectName("dialogCityTextLabel")
        self.dialog_city_edit = QLineEdit()
        self.dialog_city_edit.setObjectName("dialogCityEdit")
        self.dialog_post_code_text_label = QLabel()
        self.dialog_post_code_text_label.setObjectName("dialogPostCodeTextLabel")
        self.dialog_post_code_edit = QLineEdit()
        self.dialog_post_code_edit.setObjectName("dialogPostCodeEdit")
        self.dialog_country_text_label = QLabel()
        self.dialog_country_text_label.setObjectName("dialogCountryTextLabel")
        self.dialog_country_edit = QLineEdit()
        self.dialog_country_edit.setObjectName("dialogCountryEdit")
        fields = [
            (self.dialog_gender_text_label, self.dialog_gender_combobox),
            (self.dialog_relationship_text_label, self.dialog_relationship_combobox),
            (self.dialog_first_name_text_label, self.dialog_first_name_edit),
            (self.dialog_second_name_text_label, self.dialog_second_name_edit),
            (self.dialog_email_text_label, self.dialog_email_edit),
            (self.dialog_phone_number_text_label, self.dialog_phone_number_edit),
            (self.dialog_address_text_label, self.dialog_address_edit),
            (self.dialog_city_text_label, self.dialog_city_edit),
            (self.dialog_post_code_text_label, self.dialog_post_code_edit),
            (self.dialog_country_text_label, self.dialog_country_edit),
        ]
        for label, edit in fields:
            form_layout.addRow(label, edit)
        main_layout.addLayout(form_layout)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_dialog_text(self.objectName())
        widgets = self.findChildren((QLabel, QComboBox, QLineEdit))
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QLabel):
                        widget.setText(ui_text[widget.objectName()])
                    elif isinstance(widget, QComboBox):
                        widget.addItems(ui_text[widget.objectName()])
                    elif isinstance(widget, QLineEdit):
                        widget.setPlaceholderText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_validators(self) -> None:
        phone_regex = QRegularExpression("^\\+[0-9]{1,14}$")
        phone_validator = QRegularExpressionValidator(phone_regex)
        self.dialog_phone_number_edit.setValidator(phone_validator)

    def return_manadatory_data(self) -> Optional[list]:
        error_text = LanguageProvider.get_error_text("dialogMandatoryWidget")
        inputs = self.findChildren((QLineEdit, QComboBox))
        labels = self.findChildren(QLabel)
        mandatory_data = []
        try:
            for widget in inputs:
                if isinstance(widget, QComboBox):
                    if widget.currentIndex() == 0:
                        object_name_text = widget.objectName().removeprefix("dialog").removesuffix("Combobox")
                        DialogsProvider.show_error_dialog(error_text[f"{object_name_text.lower()}Error"])
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    mandatory_data.append(widget.currentIndex())
                if isinstance(widget, QLineEdit):
                    text = widget.text().strip()
                    if not text:
                        label_text = self.return_label_text(labels, widget)
                        DialogsProvider.show_error_dialog(f"{error_text["emptyTextError"]}{label_text}")
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    elif widget.objectName() == "dialogEmailEdit" and not ContactValidator.validate_email(text):
                        DialogsProvider.show_error_dialog(error_text["emailValidatorError"])
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    elif widget.objectName() == "dialogPhoneNumberEdit" and not ContactValidator.validate_phone_number(text):
                        DialogsProvider.show_error_dialog(error_text["phonenumberValidatorError"])
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    mandatory_data.append(text)
            return mandatory_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def return_label_text(label_list: [QLabel], widget: QWidget) -> str:
        widget_name = widget.objectName()
        for label in label_list:
            label_name = label.objectName().removesuffix("TextLabel")
            if widget_name.startswith(label_name):
                return label.text().removesuffix(":")
        return ""