from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit, QTabWidget

from src.contacts.ui.shared_widgets.validated_lineedit import ValidatedLineedit
from src.contacts.utilities.check_update_data import CheckUpdateProvider
from src.contacts.utilities.contact_validator import ContactValidator
from src.contacts.utilities.optimalize_data import normalize_texts
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
        ContactValidator.contact_input_validator(name_city_edits=[self.dialog_work_street_edit, self.dialog_work_city_edit,
                                                                  self.dialog_work_country_edit],
                                                 house_number_edit=self.dialog_work_house_number_edit,
                                                 post_code_edit=self.dialog_work_post_code_edit,
                                                 email_edit=self.dialog_work_email_edit,
                                                 phone_edit=self.dialog_work_phone_number_edit,
                                                 company_edit=self.dialog_work_company_edit)
        self.default_data = None

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.dialog_work_company_text_label = QLabel()
        self.dialog_work_company_text_label.setObjectName("dialogWorkCompanyTextLabel")
        self.dialog_work_company_edit = ValidatedLineedit(self)
        self.dialog_work_company_edit.setObjectName("dialogWorkCompanyEdit")
        self.dialog_work_email_text_label = QLabel()
        self.dialog_work_email_text_label.setObjectName("dialogWorkEmailTextLabel")
        self.dialog_work_email_edit = ValidatedLineedit(self)
        self.dialog_work_email_edit.setObjectName("dialogWorkEmailEdit")
        self.dialog_work_phone_number_text_label = QLabel()
        self.dialog_work_phone_number_text_label.setObjectName("dialogWorkPhoneNumberTextLabel")
        self.dialog_work_phone_number_edit = ValidatedLineedit(self)
        self.dialog_work_phone_number_edit.setObjectName("dialogPhoneNumberEdit")
        self.dialog_work_street_text_label = QLabel()
        self.dialog_work_street_text_label.setObjectName("dialogWorkStreetTextLabel")
        self.dialog_work_street_edit = ValidatedLineedit(self)
        self.dialog_work_street_edit.setObjectName("dialogWorkStreetEdit")
        self.dialog_work_house_number_text_label = QLabel()
        self.dialog_work_house_number_text_label.setObjectName("dialogWorkHouseNumberTextLabel")
        self.dialog_work_house_number_edit = ValidatedLineedit(self)
        self.dialog_work_house_number_edit.setObjectName("dialogWorkHouseNumberEdit")
        self.dialog_work_city_text_label = QLabel()
        self.dialog_work_city_text_label.setObjectName("dialogWorkCityTextLabel")
        self.dialog_work_city_edit = ValidatedLineedit(self)
        self.dialog_work_city_edit.setObjectName("dialogWorkCityEdit")
        self.dialog_work_post_code_text_label = QLabel()
        self.dialog_work_post_code_text_label.setObjectName("dialogPostCodeTextLabel")
        self.dialog_work_post_code_edit = ValidatedLineedit(self)
        self.dialog_work_post_code_edit.setObjectName("dialogPostCodeEdit")
        self.dialog_work_country_text_label = QLabel()
        self.dialog_work_country_text_label.setObjectName("dialogWorkCountryTextLabel")
        self.dialog_work_country_edit = ValidatedLineedit(self)
        self.dialog_work_country_edit.setObjectName("dialogWorkCountryEdit")
        widgets = [
            (self.dialog_work_company_text_label, self.dialog_work_company_edit),
            (self.dialog_work_email_text_label, self.dialog_work_email_edit),
            (self.dialog_work_phone_number_text_label, self.dialog_work_phone_number_edit),
            (self.dialog_work_street_text_label, self.dialog_work_street_edit),
            (self.dialog_work_house_number_text_label, self.dialog_work_house_number_edit),
            (self.dialog_work_city_text_label, self.dialog_work_city_edit),
            (self.dialog_work_post_code_text_label, self.dialog_work_post_code_edit),
            (self.dialog_work_country_text_label, self.dialog_work_country_edit),
        ]
        for label, edit in widgets:
            main_layout.addRow(label, edit)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_dialog_text(self.objectName())
            widgets = self.findChildren((QLabel, QLineEdit))
            if ui_text:
                for widget in widgets:
                    if isinstance(widget, QLabel):
                        if widget.objectName() in ui_text:
                            widget.setText(ui_text.get(widget.objectName(), ""))
                    elif isinstance(widget, QLineEdit):
                        if widget.objectName() in ui_text:
                            widget.setPlaceholderText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def return_work_data(self) -> list | None:
        try:
            error_text = LanguageProvider.get_error_text(self.objectName())
            inputs = self.findChildren(QLineEdit)
            work_data = []
            for widget in inputs:
                text = widget.text().strip()
                if widget.objectName() == "dialogWorkEmailEdit" and text and not ContactValidator.validate_email(text):
                    DialogsProvider.show_error_dialog(error_text.get("emailValidatorError"), self)
                    self.set_tab_index()
                    widget.setFocus()
                    return None
                elif widget.objectName() == "dialogPhoneNumberEdit" and text and not ContactValidator.validate_phone_number(text):
                    DialogsProvider.show_error_dialog(error_text.get("phoneNumberValidatorError", self))
                    self.set_tab_index()
                    widget.setFocus()
                    return None
                work_data.append(text)
            if not ContactValidator.validate_work_address(self.dialog_work_city_edit, self.dialog_work_house_number_edit,
                                                          self.dialog_work_post_code_edit, self.dialog_work_country_edit):
                DialogsProvider.show_error_dialog(error_text.get("workAddressValidatorError", self))
                self.set_tab_index()
                return None
            work_data += normalize_texts(
                [self.dialog_work_company_edit, self.dialog_work_street_edit, self.dialog_work_city_edit,
                 self.dialog_work_country_edit])
            if self.default_data:
                return [work_data, CheckUpdateProvider.check_update(self.objectName(), self.default_data, work_data)]
            return work_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def set_contact_data(self, data: dict) -> None:
        try:
            widget_data = [data.get("company_name", ""), data.get("work_email", ""),  data.get("work_phone_number", ""),
                           data.get("work_street", ""), data.get("work_house_number", ""), data.get("work_city", ""),
                           data.get("work_post_code", ""), data.get("work_country", "")]
            self.default_data = widget_data
            self.dialog_work_company_edit.setText(widget_data[0])
            self.dialog_work_email_edit.setText(widget_data[1])
            self.dialog_work_phone_number_edit.setText(widget_data[2])
            self.dialog_work_street_edit.setText(widget_data[3])
            self.dialog_work_house_number_edit.setText(widget_data[4])
            self.dialog_work_city_edit.setText(widget_data[5])
            self.dialog_work_post_code_edit.setText(widget_data[6])
            self.dialog_work_country_edit.setText(widget_data[7])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tab_index(self) -> None:
        self.main_tab.setCurrentIndex(1)
        self.non_mandatory_tab.setCurrentIndex(0)