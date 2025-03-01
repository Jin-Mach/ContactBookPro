from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class SocialNetworkWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogSocialNetworkWidget")
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.dialog_facebook_url_text_label = QLabel()
        self.dialog_facebook_url_text_label.setObjectName("dialogFacebookUrlTextLabel")
        self.dialog_facebook_url_edit = QLineEdit()
        self.dialog_facebook_url_edit.setObjectName("dialogFacebookUrlEdit")
        self.dialog_x_url_text_label = QLabel()
        self.dialog_x_url_text_label.setObjectName("dialogXUrlTextLabel")
        self.dialog_x_url_edit = QLineEdit()
        self.dialog_x_url_edit.setObjectName("dialogXUrlEdit")
        self.dialog_instagram_url_text_label = QLabel()
        self.dialog_instagram_url_text_label.setObjectName("dialogInstagramUrlTextLabel")
        self.dialog_instagram_url_edit = QLineEdit()
        self.dialog_instagram_url_edit.setObjectName("dialogInstagramUrlEdit")
        self.dialog_linkedin_url_text_label = QLabel()
        self.dialog_linkedin_url_text_label.setObjectName("dialogLinkedinUrlTextLabel")
        self.dialog_linkedin_url_edit = QLineEdit()
        self.dialog_linkedin_url_edit.setObjectName("dialogLinkedinUrlEdit")
        self.dialog_github_url_text_label = QLabel()
        self.dialog_github_url_text_label.setObjectName("dialogGithubUrlTextLabel")
        self.dialog_github_url_edit = QLineEdit()
        self.dialog_github_url_edit.setObjectName("dialogGithubUrlEdit")
        self.dialog_website_text_label = QLabel()
        self.dialog_website_text_label.setObjectName("dialogWebsiteTextLabel")
        self.dialog_website_edit = QLineEdit()
        self.dialog_website_edit.setObjectName("dialogWebsiteEdit")
        widgets = [
            (self.dialog_facebook_url_text_label, self.dialog_facebook_url_edit),
            (self.dialog_x_url_text_label, self.dialog_x_url_edit),
            (self.dialog_instagram_url_text_label, self.dialog_instagram_url_edit),
            (self.dialog_linkedin_url_text_label, self.dialog_linkedin_url_edit),
            (self.dialog_github_url_text_label, self.dialog_github_url_edit),
            (self.dialog_website_text_label, self.dialog_website_edit),
        ]
        for label, edit in widgets:
            main_layout.addRow(label, edit)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        widgets = [self.dialog_facebook_url_text_label, self.dialog_x_url_text_label, self.dialog_instagram_url_text_label,
                   self.dialog_linkedin_url_text_label, self.dialog_github_url_text_label, self.dialog_website_text_label]
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)