from functools import partial

from PyQt6.QtCore import QSize, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QComboBox, QPushButton, QLabel, QFormLayout, QHBoxLayout, QLineEdit

from src.contacts.contacts_utilities.contact_validator import ContactValidator
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class SearchMandatoryWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("searchMandatoryWidget")
        self.operator_width = 150
        self.setLayout(self.create_gui())
        self.set_ui_text()
        ContactValidator.search_input_validator(email_edit=self.search_email_edit, phone_edit=self.search_phone_number_edit)

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
        self.search_first_name_edit = QLineEdit()
        self.search_first_name_edit.setObjectName("searchFirstNameEdit")
        self.search_first_name_operator = QComboBox()
        self.search_first_name_operator.setObjectName("searchFirstNameOperator")
        self.search_first_name_operator.setFixedWidth(self.operator_width)
        self.search_second_name_text_label = QLabel()
        self.search_second_name_text_label.setObjectName("searchSecondNameTextLabel")
        self.search_second_name_edit = QLineEdit()
        self.search_second_name_edit.setObjectName("searchSecondNameEdit")
        self.search_second_name_operator = QComboBox()
        self.search_second_name_operator.setObjectName("searchSecondNameOperator")
        self.search_second_name_operator.setFixedWidth(self.operator_width)
        self.search_email_text_label = QLabel()
        self.search_email_text_label.setObjectName("searchEmailTextLabel")
        self.search_email_edit = QLineEdit()
        self.search_email_edit.setObjectName("searchEmailEdit")
        self.search_email_operator = QComboBox()
        self.search_email_operator.setObjectName("searchEmailOperator")
        self.search_email_operator.setFixedWidth(self.operator_width)
        self.search_phone_number_text_label = QLabel()
        self.search_phone_number_text_label.setObjectName("searchPhoneNumberTextLabel")
        self.search_phone_number_edit = QLineEdit()
        self.search_phone_number_edit.setObjectName("searchPhoneNumberEdit")
        self.search_phone_number_operator = QComboBox()
        self.search_phone_number_operator.setObjectName("searchPhoneNumberOperator")
        self.search_phone_number_operator.setFixedWidth(self.operator_width)
        self.search_city_text_label = QLabel()
        self.search_city_text_label.setObjectName("searchCityTextLabel")
        self.search_city_edit = QLineEdit()
        self.search_city_edit.setObjectName("searchCityEdit")
        self.search_city_operator = QComboBox()
        self.search_city_operator.setObjectName("searchCityOperator")
        self.search_city_operator.setFixedWidth(self.operator_width)
        self.search_street_text_label = QLabel()
        self.search_street_text_label.setObjectName("searchStreetTextLabel")
        self.search_street_edit = QLineEdit()
        self.search_street_edit.setObjectName("searchStreetEdit")
        self.search_street_operator = QComboBox()
        self.search_street_operator.setObjectName("searchStreetOperator")
        self.search_street_operator.setFixedWidth(self.operator_width)
        self.search_house_number_text_label = QLabel()
        self.search_house_number_text_label.setObjectName("searchHouseNumberTextLabel")
        self.search_house_number_edit = QLineEdit()
        self.search_house_number_edit.setObjectName("searchHouseNumberEdit")
        self.search_house_number_operator = QComboBox()
        self.search_house_number_operator.setObjectName("searchHouseNumberOperator")
        self.search_house_number_operator.setFixedWidth(self.operator_width)
        self.search_post_code_text_label = QLabel()
        self.search_post_code_text_label.setObjectName("searchPostCodeTextLabel")
        self.search_post_code_edit = QLineEdit()
        self.search_post_code_edit.setObjectName("searchPostCodeEdit")
        self.search_post_code_operator = QComboBox()
        self.search_post_code_operator.setObjectName("searchPostCodeOperator")
        self.search_post_code_operator.setFixedWidth(self.operator_width)
        self.search_country_text_label = QLabel()
        self.search_country_text_label.setObjectName("searchCountryTextLabel")
        self.search_country_edit = QLineEdit()
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
            (self.search_city_text_label, self.search_city_edit, self.search_city_operator),
            (self.search_street_text_label, self.search_street_edit, self.search_street_operator),
            (self.search_house_number_text_label, self.search_house_number_edit, self.search_house_number_operator),
            (self.search_post_code_text_label, self.search_post_code_edit, self.search_post_code_operator),
            (self.search_country_text_label, self.search_country_edit, self.search_country_operator)
        ]
        tooltip_text = LanguageProvider.get_tooltips_text("advancedSearchDialog")
        for label, edit, operator in fields:
            layout = QHBoxLayout()
            clear_filter_pushbutton = QPushButton()
            clear_filter_pushbutton.setObjectName("clearFilterPushbutton")
            IconProvider.set_buttons_icon("advancedSearchDialog", [clear_filter_pushbutton], QSize(25, 25))
            if clear_filter_pushbutton.objectName() in tooltip_text:
                clear_filter_pushbutton.setToolTip(tooltip_text[clear_filter_pushbutton.objectName()])
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
            for widget in widgets:
                if isinstance(widget, QLabel):
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text[widget.objectName()])
                elif isinstance(widget, QComboBox):
                    if widget.objectName().endswith("Combobox") and widget.objectName() in ui_text:
                        widget.addItems(ui_text[widget.objectName()])
                    elif "operators" in ui_text:
                        widget.addItems(ui_text["operators"])
                elif isinstance(widget, QLineEdit):
                    if widget.objectName() in ui_text:
                        widget.setPlaceholderText(ui_text[widget.objectName()])
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