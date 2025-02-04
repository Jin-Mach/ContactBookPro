from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit


class SocialNetworkWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogSocialNetworkWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.dialog_facebook_url_text_label = QLabel("Facebook:")
        self.dialog_facebook_url_text_label.setObjectName("dialogFacebookUrlTextLabel")
        self.dialog_facebook_url_edit = QLineEdit()
        self.dialog_facebook_url_edit.setObjectName("dialogFacebookUrlEdit")
        self.dialog_x_url_text_label = QLabel("X:")
        self.dialog_x_url_text_label.setObjectName("dialogXUrlTextLabel")
        self.dialog_x_url_edit = QLineEdit()
        self.dialog_x_url_edit.setObjectName("dialogXUrlEdit")
        self.dialog_instagram_url_text_label = QLabel("instagram:")
        self.dialog_instagram_url_text_label.setObjectName("dialogInstagramUrlTextLabel")
        self.dialog_instagram_url_edit = QLineEdit()
        self.dialog_instagram_url_edit.setObjectName("dialogInstagramUrlEdit")
        self.dialog_linkedin_url_text_label = QLabel("linkedin:")
        self.dialog_linkedin_url_text_label.setObjectName("dialogLinkedinUrlTextLabel")
        self.dialog_linkedin_url_edit = QLineEdit()
        self.dialog_linkedin_url_edit.setObjectName("dialogLinkedinUrlEdit")
        self.dialog_github_url_text_label = QLabel("github")
        self.dialog_github_url_text_label.setObjectName("dialogGithubUrlTextLabel")
        self.dialog_github_url_edit = QLineEdit()
        self.dialog_github_url_edit.setObjectName("dialogGithubUrlEdit")
        self.dialog_website_text_label = QLabel("web:")
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