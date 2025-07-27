from functools import partial

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLayout, QComboBox, QPushButton, QLabel, QFormLayout, QHBoxLayout, QLineEdit

from src.contacts.ui.shared_widgets.validated_lineedit import ValidatedLineedit
from src.contacts.utilities.contact_validator import ContactValidator
from src.contacts.utilities.optimalize_data import normalize_input
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class SearchMandatoryWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("searchMandatoryWidget")
        self.operator_width = 150
        self.setLayout(self.create_gui())
        self.set_ui_text()
        ContactValidator.search_input_validator(name_city_edits=[self.search_first_name_edit, self.search_second_name_edit,
                                                                 self.search_street_edit, self.search_city_edit, self.search_country_edit],
                                                house_number_edit=self.search_house_number_edit,
                                                post_code_edit=self.search_post_code_edit,
                                                email_edit=self.search_email_edit,
                                                phone_edit=self.search_phone_number_edit)

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.search_gender_text_label = QLabel()
        self.search_gender_text_label.setObjectName("searchGenderTextLabel")
        self.search_gender_combobox = QComboBox()
        self.search_gender_combobox.setObjectName("searchGenderCombobox")
        self.search_gender_combobox.setFixedWidth(200)
        self.search_relationship_text_label = QLabel()
        self.search_relationship_text_label.setObjectName("searchRelationshipTextLabel")
        self.search_relationship_combobox = QComboBox()
        self.search_relationship_combobox.setObjectName("searchRelationshipCombobox")
        self.search_relationship_combobox.setFixedWidth(200)
        self.search_first_name_text_label = QLabel()
        self.search_first_name_text_label.setObjectName("searchFirstNameTextLabel")
        self.search_first_name_edit = ValidatedLineedit(self)
        self.search_first_name_edit.setObjectName("searchFirstNameEdit")
        self.search_first_name_operator = QComboBox()
        self.search_first_name_operator.setObjectName("searchFirstNameOperator")
        self.search_first_name_operator.setFixedWidth(self.operator_width)
        self.search_second_name_text_label = QLabel()
        self.search_second_name_text_label.setObjectName("searchSecondNameTextLabel")
        self.search_second_name_edit = ValidatedLineedit(self)
        self.search_second_name_edit.setObjectName("searchSecondNameEdit")
        self.search_second_name_operator = QComboBox()
        self.search_second_name_operator.setObjectName("searchSecondNameOperator")
        self.search_second_name_operator.setFixedWidth(self.operator_width)
        self.search_email_text_label = QLabel()
        self.search_email_text_label.setObjectName("searchEmailTextLabel")
        self.search_email_edit = ValidatedLineedit(self)
        self.search_email_edit.setObjectName("searchEmailEdit")
        self.search_email_operator = QComboBox()
        self.search_email_operator.setObjectName("searchEmailOperator")
        self.search_email_operator.setFixedWidth(self.operator_width)
        self.search_phone_number_text_label = QLabel()
        self.search_phone_number_text_label.setObjectName("searchPhoneNumberTextLabel")
        self.search_phone_number_edit = ValidatedLineedit(self)
        self.search_phone_number_edit.setObjectName("searchPhoneNumberEdit")
        self.search_phone_number_operator = QComboBox()
        self.search_phone_number_operator.setObjectName("searchPhoneNumberOperator")
        self.search_phone_number_operator.setFixedWidth(self.operator_width)
        self.search_street_text_label = QLabel()
        self.search_street_text_label.setObjectName("searchStreetTextLabel")
        self.search_street_edit = ValidatedLineedit(self)
        self.search_street_edit.setObjectName("searchStreetEdit")
        self.search_street_operator = QComboBox()
        self.search_street_operator.setObjectName("searchStreetOperator")
        self.search_street_operator.setFixedWidth(self.operator_width)
        self.search_house_number_text_label = QLabel()
        self.search_house_number_text_label.setObjectName("searchHouseNumberTextLabel")
        self.search_house_number_edit = ValidatedLineedit(self)
        self.search_house_number_edit.setObjectName("searchHouseNumberEdit")
        self.search_house_number_operator = QComboBox()
        self.search_house_number_operator.setObjectName("searchHouseNumberOperator")
        self.search_house_number_operator.setFixedWidth(self.operator_width)
        self.search_city_text_label = QLabel()
        self.search_city_text_label.setObjectName("searchCityTextLabel")
        self.search_city_edit = ValidatedLineedit(self)
        self.search_city_edit.setObjectName("searchCityEdit")
        self.search_city_operator = QComboBox()
        self.search_city_operator.setObjectName("searchCityOperator")
        self.search_city_operator.setFixedWidth(self.operator_width)
        self.search_post_code_text_label = QLabel()
        self.search_post_code_text_label.setObjectName("searchPostCodeTextLabel")
        self.search_post_code_edit = ValidatedLineedit(self)
        self.search_post_code_edit.setObjectName("searchPostCodeEdit")
        self.search_post_code_operator = QComboBox()
        self.search_post_code_operator.setObjectName("searchPostCodeOperator")
        self.search_post_code_operator.setFixedWidth(self.operator_width)
        self.search_country_text_label = QLabel()
        self.search_country_text_label.setObjectName("searchCountryTextLabel")
        self.search_country_edit = ValidatedLineedit(self)
        self.search_country_edit.setObjectName("searchCountryEdit")
        self.search_country_operator = QComboBox()
        self.search_country_operator.setObjectName("searchCountryOperator")
        self.search_country_operator.setFixedWidth(self.operator_width)
        fields = [
            (self.search_gender_text_label, self.search_gender_combobox, None),
            (self.search_relationship_text_label, self.search_relationship_combobox, None),
            (self.search_first_name_text_label, self.search_first_name_edit, self.search_first_name_operator),
            (self.search_second_name_text_label, self.search_second_name_edit, self.search_second_name_operator),
            (self.search_email_text_label, self.search_email_edit, self.search_email_operator),
            (self.search_phone_number_text_label, self.search_phone_number_edit, self.search_phone_number_operator),
            (self.search_street_text_label, self.search_street_edit, self.search_street_operator),
            (self.search_house_number_text_label, self.search_house_number_edit, self.search_house_number_operator),
            (self.search_city_text_label, self.search_city_edit, self.search_city_operator),
            (self.search_post_code_text_label, self.search_post_code_edit, self.search_post_code_operator),
            (self.search_country_text_label, self.search_country_edit, self.search_country_operator)
        ]
        tooltip_text = LanguageProvider.get_tooltips_text("advancedSearchDialog")
        for label, edit, operator in fields:
            layout = QHBoxLayout()
            clear_filter_pushbutton = QPushButton()
            clear_filter_pushbutton.setObjectName("clearFilterPushbutton")
            IconProvider.set_buttons_icon("advancedSearchDialog", [clear_filter_pushbutton], QSize(25, 25))
            if tooltip_text and clear_filter_pushbutton.objectName() in tooltip_text:
                clear_filter_pushbutton.setToolTip(tooltip_text.get(clear_filter_pushbutton.objectName(), ""))
                clear_filter_pushbutton.setToolTipDuration(5000)
            clear_filter_pushbutton.clicked.connect(partial(SearchMandatoryWidget.reset_row_filter, edit, operator))
            layout.addWidget(edit)
            if isinstance(edit, QComboBox):
                layout.addStretch()
            elif isinstance(edit, QLineEdit):
                layout.addWidget(operator)
            layout.addWidget(clear_filter_pushbutton)
            main_layout.addRow(label, layout)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            widgets = self.findChildren((QLabel, QComboBox, QLineEdit))
            if ui_text:
                for widget in widgets:
                    if isinstance(widget, QLabel):
                        if widget.objectName() in ui_text:
                            widget.setText(ui_text.get(widget.objectName(), ""))
                    elif isinstance(widget, QComboBox):
                        if widget.objectName().endswith("Combobox") and widget.objectName() in ui_text:
                            widget.addItems(ui_text.get(widget.objectName(), ""))
                        elif "operators" in ui_text:
                            widget.addItems(ui_text.get("operators", []))
                    elif isinstance(widget, QLineEdit):
                        if widget.objectName() in ui_text:
                            widget.setPlaceholderText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def reset_row_filter(widget: QWidget, operator: QComboBox) -> None:
        if isinstance(widget, QComboBox):
            widget.setCurrentIndex(0)
        else:
            widget.clear()
            operator.setCurrentIndex(0)

    def reset_all_filters(self) -> None:
        widgets = self.findChildren((QComboBox, QLineEdit))
        for widget in widgets:
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            else:
                widget.clear()

    def return_mandatory_filter(self) -> tuple[str, list]:
        try:
            fields = [
                (self.search_gender_combobox, "=", "gender"),
                (self.search_relationship_combobox, "=", "relationship"),
                (self.search_first_name_edit, self.search_first_name_operator, "first_name_normalized"),
                (self.search_second_name_edit, self.search_second_name_operator, "second_name_normalized"),
                (self.search_email_edit, self.search_email_operator, "personal_email"),
                (self.search_phone_number_edit, self.search_phone_number_operator, "personal_phone_number"),
                (self.search_street_edit, self.search_street_operator, "personal_street_normalized"),
                (self.search_house_number_edit, self.search_house_number_operator, "personal_house_number"),
                (self.search_city_edit, self.search_city_operator, "personal_city_normalized"),
                (self.search_post_code_edit, self.search_post_code_operator, "personal_post_code"),
                (self.search_country_edit, self.search_country_operator, "personal_country_normalized")
            ]
            filters = []
            values = []
            normalized_columns = {"first_name_normalized", "second_name_normalized", "personal_city_normalized",
                                "personal_street_normalized", "personal_country_normalized"}
            for edit, operator, column in fields:
                if isinstance(edit, QLineEdit):
                    value = edit.text().strip()
                    if column in normalized_columns:
                        value = normalize_input(edit)
                    operation = operator.currentIndex()
                    if value:
                        if operation == 0:
                            filters.append(f"{column} = ?")
                            values.append(value)
                        elif operation == 1:
                            filters.append(f"{column} LIKE ?")
                            values.append(f"%{value}%")
                        elif operation == 2:
                            filters.append(f"{column} LIKE ?")
                            values.append(f"{value}%")
                        elif operation == 3:
                            filters.append(f"{column} LIKE ?")
                            values.append(f"%{value}")
                elif isinstance(edit, QComboBox):
                    index = edit.currentIndex()
                    if index > 0:
                        filters.append(f"{column} {operator} ?")
                        values.append(index)
            if filters:
                return " AND ".join(filters), values
            return "", []
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return "", []

    def return_mandatory_current_filter(self) -> list:
        try:
            fields = [
                (self.search_gender_text_label, self.search_gender_combobox, None),
                (self.search_relationship_text_label, self.search_relationship_combobox, None),
                (self.search_first_name_text_label, self.search_first_name_operator, self.search_first_name_edit),
                (self.search_second_name_text_label, self.search_second_name_operator, self.search_second_name_edit),
                (self.search_email_text_label, self.search_email_operator, self.search_email_edit),
                (self.search_phone_number_text_label, self.search_phone_number_operator, self.search_phone_number_edit),
                (self.search_street_text_label, self.search_street_operator, self.search_street_edit),
                (self.search_house_number_text_label, self.search_house_number_operator, self.search_house_number_edit),
                (self.search_city_text_label, self.search_city_operator, self.search_city_edit),
                (self.search_post_code_text_label, self.search_post_code_operator, self.search_post_code_edit),
                (self.search_country_text_label, self.search_country_operator, self.search_country_edit)
            ]
            active_filters = []
            for label, combobox, edit in fields:
                if not edit and combobox.currentIndex() > 0:
                    active_filters.append({
                        "label_text": label.text(),
                        "combobox": combobox,
                        "combobox_text": combobox.currentText(),
                        "edit": None,
                        "edit_text": None
                    })
                else:
                    if edit:
                        text = edit.text().strip()
                        if text:
                            edit_text = text
                            if edit in (self.search_first_name_edit, self.search_second_name_edit, self.search_city_edit,
                                        self.search_street_edit, self.search_country_edit):
                                edit_text = normalize_input(edit)
                            active_filters.append({
                                "label_text": label.text(),
                                "combobox": combobox,
                                "combobox_text": combobox.currentText(),
                                "edit": edit,
                                "edit_text": edit_text
                            })
            return active_filters
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return []