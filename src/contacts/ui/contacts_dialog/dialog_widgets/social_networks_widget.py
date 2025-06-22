from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit, QTabWidget

from src.contacts.ui.shared_widgets.validated_lineedit import ValidatedLineedit
from src.contacts.utilities.check_update_data import CheckUpdateProvider
from src.contacts.utilities.contact_validator import ContactValidator
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class SocialNetworkWidget(QWidget):
    def __init__(self, main_tab: QTabWidget, non_mandatory_tab: QTabWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogSocialNetworkWidget")
        self.main_tab = main_tab
        self.non_mandatory_tab = non_mandatory_tab
        self.setLayout(self.create_gui())
        self.set_ui_text()
        ContactValidator.contact_input_validator(url_edit=self.findChildren(QLineEdit))
        self.default_data = None

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.dialog_facebook_url_text_label = QLabel()
        self.dialog_facebook_url_text_label.setObjectName("dialogFacebookUrlTextLabel")
        self.dialog_facebook_url_edit = ValidatedLineedit(self)
        self.dialog_facebook_url_edit.setObjectName("dialogFacebookUrlEdit")
        self.dialog_x_url_text_label = QLabel()
        self.dialog_x_url_text_label.setObjectName("dialogXUrlTextLabel")
        self.dialog_x_url_edit = ValidatedLineedit(self)
        self.dialog_x_url_edit.setObjectName("dialogXUrlEdit")
        self.dialog_instagram_url_text_label = QLabel()
        self.dialog_instagram_url_text_label.setObjectName("dialogInstagramUrlTextLabel")
        self.dialog_instagram_url_edit = ValidatedLineedit(self)
        self.dialog_instagram_url_edit.setObjectName("dialogInstagramUrlEdit")
        self.dialog_linkedin_url_text_label = QLabel()
        self.dialog_linkedin_url_text_label.setObjectName("dialogLinkedinUrlTextLabel")
        self.dialog_linkedin_url_edit = ValidatedLineedit(self)
        self.dialog_linkedin_url_edit.setObjectName("dialogLinkedinUrlEdit")
        self.dialog_github_url_text_label = QLabel()
        self.dialog_github_url_text_label.setObjectName("dialogGithubUrlTextLabel")
        self.dialog_github_url_edit = ValidatedLineedit(self)
        self.dialog_github_url_edit.setObjectName("dialogGithubUrlEdit")
        self.dialog_website_url_text_label = QLabel()
        self.dialog_website_url_text_label.setObjectName("dialogWebsiteUrlTextLabel")
        self.dialog_website_url_edit = ValidatedLineedit(self)
        self.dialog_website_url_edit.setObjectName("dialogWebsiteUrlEdit")
        widgets = [
            (self.dialog_facebook_url_text_label, self.dialog_facebook_url_edit),
            (self.dialog_x_url_text_label, self.dialog_x_url_edit),
            (self.dialog_instagram_url_text_label, self.dialog_instagram_url_edit),
            (self.dialog_linkedin_url_text_label, self.dialog_linkedin_url_edit),
            (self.dialog_github_url_text_label, self.dialog_github_url_edit),
            (self.dialog_website_url_text_label, self.dialog_website_url_edit),
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

    def return_social_network_data(self) -> list | None:
        try:
            error_text = LanguageProvider.get_error_text(self.objectName())
            inputs = self.findChildren(QLineEdit)
            social_network_data = []
            if error_text:
                for widget in inputs:
                    text = widget.text().strip()
                    site = widget.objectName().replace("dialog", "").replace("UrlEdit", "")
                    if text:
                        is_valid = ContactValidator.validate_url(text, site)
                        if site.lower() == "website" and not is_valid:
                            DialogsProvider.show_error_dialog(error_text.get("websiteValidatorError"), "")
                            self.set_tab_index()
                            widget.setFocus()
                            return None
                        if not is_valid:
                            message = error_text.get("urlValidatorError", "").replace("{site}", site)
                            DialogsProvider.show_error_dialog(message)
                            self.set_tab_index()
                            widget.setFocus()
                            return None
                    social_network_data.append(text)
                if self.default_data:
                    return [social_network_data, CheckUpdateProvider.check_update(self.objectName(), self.default_data, social_network_data)]
                return social_network_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def set_contact_data(self, data: dict) -> None:
        try:
            widget_data = [data.get("facebook_url", ""), data.get("x_url", ""), data.get("instagram_url", ""),
                           data.get("linkedin_url", ""), data.get("github_url", ""), data.get("website_url", "")]
            self.default_data = widget_data
            self.dialog_facebook_url_edit.setText(widget_data[0])
            self.dialog_x_url_edit.setText(widget_data[1])
            self.dialog_instagram_url_edit.setText(widget_data[2])
            self.dialog_linkedin_url_edit.setText(widget_data[3])
            self.dialog_github_url_edit.setText(widget_data[4])
            self.dialog_website_url_edit.setText(widget_data[5])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tab_index(self) -> None:
        self.main_tab.setCurrentIndex(1)
        self.non_mandatory_tab.setCurrentIndex(1)