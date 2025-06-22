from functools import partial

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QLayout, QFormLayout, QLineEdit, QComboBox, QHBoxLayout, QPushButton

from src.contacts.ui.shared_widgets.validated_lineedit import ValidatedLineedit
from src.contacts.utilities.contact_validator import ContactValidator
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class SearchSocialNetworksWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("searchSocialNetworksDialog")
        self.operator_width = 150
        self.setLayout(self.create_gui())
        self.set_ui_text()
        ContactValidator.search_input_validator(url_edit=self.findChildren(QLineEdit))

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.search_facebook_url_text_label = QLabel()
        self.search_facebook_url_text_label.setObjectName("searchFacebookUrlTextLabel")
        self.search_facebook_url_edit = ValidatedLineedit(self)
        self.search_facebook_url_edit.setObjectName("searchFacebookUrlEdit")
        self.search_facebook_url_operator = QComboBox()
        self.search_facebook_url_operator.setObjectName("searchFacebookUrlOperator")
        self.search_facebook_url_operator.setFixedWidth(self.operator_width)
        self.search_x_url_text_label = QLabel()
        self.search_x_url_text_label.setObjectName("searchXUrlTextLabel")
        self.search_x_url_edit = ValidatedLineedit(self)
        self.search_x_url_edit.setObjectName("searchXUrlEdit")
        self.search_x_url_operator = QComboBox()
        self.search_x_url_operator.setObjectName("searchXUrlOperator")
        self.search_x_url_operator.setFixedWidth(self.operator_width)
        self.search_instagram_url_text_label = QLabel()
        self.search_instagram_url_text_label.setObjectName("searchInstagramUrlTextLabel")
        self.search_instagram_url_edit = ValidatedLineedit(self)
        self.search_instagram_url_edit.setObjectName("searchInstagramUrlEdit")
        self.search_instagram_url_operator = QComboBox()
        self.search_instagram_url_operator.setObjectName("searchInstagramUrlOperator")
        self.search_instagram_url_operator.setFixedWidth(self.operator_width)
        self.search_linkedin_url_text_label = QLabel()
        self.search_linkedin_url_text_label.setObjectName("searchLinkedinUrlTextLabel")
        self.search_linkedin_url_edit = ValidatedLineedit(self)
        self.search_linkedin_url_edit.setObjectName("searchLinkedinUrlEdit")
        self.search_linkedin_url_operator = QComboBox()
        self.search_linkedin_url_operator.setObjectName("searchLinkedinUrlOperator")
        self.search_linkedin_url_operator.setFixedWidth(self.operator_width)
        self.search_github_url_text_label = QLabel()
        self.search_github_url_text_label.setObjectName("searchGithubUrlTextLabel")
        self.search_github_url_edit = ValidatedLineedit(self)
        self.search_github_url_edit.setObjectName("searchGithubUrlEdit")
        self.search_github_url_operator = QComboBox()
        self.search_github_url_operator.setObjectName("searchGithubUrlOperator")
        self.search_github_url_operator.setFixedWidth(self.operator_width)
        self.search_website_url_text_label = QLabel()
        self.search_website_url_text_label.setObjectName("searchWebsiteUrlTextLabel")
        self.search_website_url_edit = ValidatedLineedit(self)
        self.search_website_url_edit.setObjectName("searchWebsiteUrlEdit")
        self.search_website_url_operator = QComboBox()
        self.search_website_url_operator.setObjectName("searchWebsiteUrlOperator")
        self.search_website_url_operator.setFixedWidth(self.operator_width)
        fields = [(self.search_facebook_url_text_label, self.search_facebook_url_edit, self.search_facebook_url_operator),
                  (self.search_x_url_text_label, self.search_x_url_edit, self.search_x_url_operator),
                  (self.search_instagram_url_text_label, self.search_instagram_url_edit, self.search_instagram_url_operator),
                  (self.search_linkedin_url_text_label, self.search_linkedin_url_edit, self.search_linkedin_url_operator),
                  (self.search_github_url_text_label, self.search_github_url_edit, self.search_github_url_operator),
                  (self.search_website_url_text_label, self.search_website_url_edit, self.search_website_url_operator)]
        tooltip_text = LanguageProvider.get_tooltips_text("advancedSearchDialog")
        for label, edit, operator in fields:
            layout = QHBoxLayout()
            clear_filter_pushbutton = QPushButton()
            clear_filter_pushbutton.setObjectName("clearFilterPushbutton")
            IconProvider.set_buttons_icon("advancedSearchDialog", [clear_filter_pushbutton], QSize(25, 25))
            if tooltip_text and clear_filter_pushbutton.objectName() in tooltip_text:
                clear_filter_pushbutton.setToolTip(tooltip_text.get(clear_filter_pushbutton.objectName(), ""))
                clear_filter_pushbutton.setToolTipDuration(5000)
            clear_filter_pushbutton.clicked.connect(partial(SearchSocialNetworksWidget.reset_row_filter, edit, operator))
            layout.addWidget(edit)
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
                        if "operators" in ui_text:
                            widget.addItems(ui_text.get("operators", []))
                    elif isinstance(widget, QLineEdit):
                        if widget.objectName() in ui_text:
                            widget.setPlaceholderText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def reset_row_filter(edit: QLineEdit, operator: QComboBox) -> None:
        edit.clear()
        operator.setCurrentIndex(0)

    def reset_all_filters(self) -> None:
        widgets = self.findChildren((QComboBox, QLineEdit))
        for widget in widgets:
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            else:
                widget.clear()

    def return_social_filter(self) -> tuple[str, list]:
        try:
            fields = [
                (self.search_facebook_url_edit, self.search_facebook_url_operator, "facebook_url"),
                (self.search_x_url_edit, self.search_x_url_operator, "x_url"),
                (self.search_instagram_url_edit, self.search_instagram_url_operator, "instagram_url"),
                (self.search_linkedin_url_edit, self.search_linkedin_url_operator, "linkedin_url"),
                (self.search_github_url_edit, self.search_github_url_operator, "github_url"),
                (self.search_website_url_edit, self.search_website_url_operator, "website_url")
            ]
            filters = []
            values = []
            for edit, operator, column in fields:
                if isinstance(edit, QLineEdit):
                    value = edit.text().strip()
                    operation = operator.currentIndex()
                    if value and operation > 0:
                        if operation == 1:
                            filters.append(f"{column} = ?")
                            values.append(value)
                        elif operation == 2:
                            filters.append(f"{column} LIKE ?")
                            values.append(f"%{value}%")
                        elif operation == 3:
                            filters.append(f"{column} LIKE ?")
                            values.append(f"{value}%")
                        elif operation == 4:
                            filters.append(f"{column} LIKE ?")
                            values.append(f"%{value}")
            if filters:
                return " AND ".join(filters), values
            return "", []
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return "", []

    def return_social_networks_current_filter(self) -> list:
        try:
            fields = [
                (self.search_facebook_url_text_label, self.search_facebook_url_operator, self.search_facebook_url_edit),
                (self.search_x_url_text_label, self.search_x_url_operator, self.search_x_url_edit),
                (self.search_instagram_url_text_label, self.search_instagram_url_operator, self.search_instagram_url_edit),
                (self.search_linkedin_url_text_label, self.search_linkedin_url_operator, self.search_linkedin_url_edit),
                (self.search_github_url_text_label, self.search_github_url_operator, self.search_github_url_edit),
                (self.search_website_url_text_label, self.search_website_url_operator, self.search_website_url_edit)
            ]
            active_filters = []
            for label, combobox, edit in fields:
                if edit.text().strip():
                    active_filters.append({
                        "label_text": label.text(),
                        "combobox": combobox,
                        "combobox_text": combobox.currentText(),
                        "edit": edit,
                        "edit_text": edit.text().strip()
                    })
            return active_filters
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return []