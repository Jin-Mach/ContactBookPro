from PyQt6.QtWidgets import QWidget, QLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QTabWidget

from src.contacts.ui.shared_widgets.validated_lineedit import ValidatedLineedit
from src.contacts.utilities.check_update_data import CheckUpdateProvider
from src.contacts.utilities.contact_validator import ContactValidator
from src.contacts.utilities.optimalize_data import normalize_texts
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
        ContactValidator.contact_input_validator(name_city_edits=[self.dialog_first_name_edit, self.dialog_second_name_edit,
                                                                  self.dialog_street_edit, self.dialog_city_edit,
                                                                  self.dialog_country_edit],
                                                 house_number_edit=self.dialog_house_number_edit,
                                                 post_code_edit=self.dialog_post_code_edit,
                                                 email_edit=self.dialog_email_edit,
                                                 phone_edit=self.dialog_phone_number_edit)
        self.default_data = None

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
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
        self.dialog_first_name_edit = ValidatedLineedit(self)
        self.dialog_first_name_edit.setObjectName("dialogFirstNameEdit")
        self.dialog_second_name_text_label = QLabel()
        self.dialog_second_name_text_label.setObjectName("dialogSecondNameTextLabel")
        self.dialog_second_name_edit = ValidatedLineedit(self)
        self.dialog_second_name_edit.setObjectName("dialogSecondNameEdit")
        self.dialog_email_text_label = QLabel()
        self.dialog_email_text_label.setObjectName("dialogEmailTextLabel")
        self.dialog_email_edit = ValidatedLineedit(self)
        self.dialog_email_edit.setObjectName("dialogEmailEdit")
        self.dialog_phone_number_text_label = QLabel()
        self.dialog_phone_number_text_label.setObjectName("dialogPhoneNumberTextLabel")
        self.dialog_phone_number_edit = ValidatedLineedit(self)
        self.dialog_phone_number_edit.setObjectName("dialogPhoneNumberEdit")
        self.dialog_street_text_label = QLabel()
        self.dialog_street_text_label.setObjectName("dialogStreetTextLabel")
        self.dialog_street_edit = ValidatedLineedit(self)
        self.dialog_street_edit.setObjectName("dialogStreetEdit")
        self.dialog_house_number_text_label = QLabel()
        self.dialog_house_number_text_label.setObjectName("dialogHouseNumberTextLabel")
        self.dialog_house_number_edit = ValidatedLineedit(self)
        self.dialog_house_number_edit.setObjectName("dialogHouseNumberEdit")
        self.dialog_city_text_label = QLabel()
        self.dialog_city_text_label.setObjectName("dialogCityTextLabel")
        self.dialog_city_edit = ValidatedLineedit(self)
        self.dialog_city_edit.setObjectName("dialogCityEdit")
        self.dialog_post_code_text_label = QLabel()
        self.dialog_post_code_text_label.setObjectName("dialogPostCodeTextLabel")
        self.dialog_post_code_edit = ValidatedLineedit(self)
        self.dialog_post_code_edit.setObjectName("dialogPostCodeEdit")
        self.dialog_country_text_label = QLabel()
        self.dialog_country_text_label.setObjectName("dialogCountryTextLabel")
        self.dialog_country_edit = ValidatedLineedit(self)
        self.dialog_country_edit.setObjectName("dialogCountryEdit")
        fields = [
            (self.dialog_gender_text_label, self.dialog_gender_combobox),
            (self.dialog_relationship_text_label, self.dialog_relationship_combobox),
            (self.dialog_first_name_text_label, self.dialog_first_name_edit),
            (self.dialog_second_name_text_label, self.dialog_second_name_edit),
            (self.dialog_email_text_label, self.dialog_email_edit),
            (self.dialog_phone_number_text_label, self.dialog_phone_number_edit),
            (self.dialog_street_text_label, self.dialog_street_edit),
            (self.dialog_house_number_text_label, self.dialog_house_number_edit),
            (self.dialog_city_text_label, self.dialog_city_edit),
            (self.dialog_post_code_text_label, self.dialog_post_code_edit),
            (self.dialog_country_text_label, self.dialog_country_edit),
        ]
        for label, edit in fields:
            main_layout.addRow(label, edit)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_dialog_text(self.objectName())
            widgets = self.findChildren((QLabel, QComboBox, QLineEdit))
            if ui_text:
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            widget.setText(ui_text.get(widget.objectName(), ""))
                        elif isinstance(widget, QComboBox):
                            widget.addItems(ui_text.get(widget.objectName(), ""))
                        elif isinstance(widget, QLineEdit):
                            widget.setPlaceholderText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def return_mandatory_data(self) -> list | None:
        try:
            error_text = LanguageProvider.get_error_text("dialogMandatoryWidget")
            inputs = self.findChildren((QLineEdit, QComboBox))
            labels = self.findChildren(QLabel)
            gender_relationship_data = []
            mandatory_data = []
            for widget in inputs:
                if isinstance(widget, QComboBox):
                    if widget.currentIndex() == 0:
                        object_name_text = widget.objectName().removeprefix("dialog").removesuffix("Combobox")
                        if error_text:
                            DialogsProvider.show_error_dialog(error_text.get(f"{object_name_text.lower()}Error", "Chyba"), self)
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    gender_relationship_data.append(widget.currentIndex())
                if isinstance(widget, QLineEdit):
                    text = widget.text().strip()
                    if not text and widget.objectName() != "dialogStreetEdit":
                        label_text = self.return_label_text(labels, widget)
                        if error_text:
                            DialogsProvider.show_error_dialog(f"{error_text.get("emptyTextError", "")}{label_text}", self)
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    elif widget.objectName() == "dialogEmailEdit" and not ContactValidator.validate_email(text):
                        if error_text:
                            DialogsProvider.show_error_dialog(error_text.get("emailValidatorError", ""), self)
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    elif widget.objectName() == "dialogPhoneNumberEdit" and not ContactValidator.validate_phone_number(text):
                        if error_text:
                            DialogsProvider.show_error_dialog(error_text.get("phoneNumberValidatorError", ""), self)
                        self.main_tab_widget.setCurrentIndex(0)
                        widget.setFocus()
                        return None
                    mandatory_data.append(text)
            mandatory_data = gender_relationship_data + mandatory_data + normalize_texts([self.dialog_first_name_edit, self.dialog_second_name_edit,
                                               self.dialog_street_edit, self.dialog_city_edit, self.dialog_country_edit])
            if self.default_data:
                return [mandatory_data, CheckUpdateProvider.check_update(self.objectName(), self.default_data, mandatory_data)]
            return mandatory_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def set_contact_data(self, data: dict) -> None:
        try:
            widget_data = [
                int(data.get("gender", 0)),
                int(data.get("relationship", 0)),
                data.get("first_name", ""),
                data.get("second_name", ""),
                data.get("personal_email", ""),
                data.get("personal_phone_number", ""),
                data.get("personal_street", ""),
                data.get("personal_house_number", ""),
                data.get("personal_city", ""),
                data.get("personal_post_code", ""),
                data.get("personal_country", ""),
            ]
            self.default_data = widget_data
            self.dialog_gender_combobox.setCurrentIndex(widget_data[0])
            self.dialog_relationship_combobox.setCurrentIndex(widget_data[1])
            self.dialog_first_name_edit.setText(widget_data[2])
            self.dialog_second_name_edit.setText(widget_data[3])
            self.dialog_email_edit.setText(widget_data[4])
            self.dialog_phone_number_edit.setText(widget_data[5])
            self.dialog_street_edit.setText(widget_data[6])
            self.dialog_house_number_edit.setText(widget_data[7])
            self.dialog_city_edit.setText(widget_data[8])
            self.dialog_post_code_edit.setText(widget_data[9])
            self.dialog_country_edit.setText(widget_data[10])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def return_label_text(label_list: list, widget: QWidget) -> str:
        widget_name = widget.objectName()
        for label in label_list:
            label_name = label.objectName().removesuffix("TextLabel")
            if widget_name.startswith(label_name):
                return label.text().removesuffix(":")
        return ""