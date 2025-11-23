from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton

from src.contacts.utilities.url_utilities import open_url
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class AboutApplicationDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setObjectName("aboutApplicationDialog")
        self.parent = parent
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        IconProvider.set_window_icon(self, "mainWindow")
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.set_tooltips_text()
        self.set_edit_text()
        IconProvider.set_buttons_icon(self.objectName(), [self.github_button], QSize(30, 30), self.parent)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.about_applicaton_text_edit = QTextEdit()
        self.about_applicaton_text_edit.setObjectName("aboutApplicationTextEdit")
        self.about_applicaton_text_edit.setReadOnly(True)
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.github_button = QPushButton()
        self.github_button.setObjectName("githubButton")
        self.github_button.clicked.connect(lambda: open_url("https://github.com/Jin-Mach/ContactBookPro" ,self))
        buttons_layout.addWidget(self.github_button)
        main_layout.addWidget(self.about_applicaton_text_edit)
        main_layout.addLayout(buttons_layout)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_json_text("ui_text.json", self.objectName())
            if ui_text:
                self.setWindowTitle(ui_text.get("aboutTitle", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_json_text("tooltips_text.json", self.objectName())
            buttons = [self.github_button]
            if tooltips_text:
                for button in buttons:
                    if button.objectName() in tooltips_text:
                        button.setToolTip(tooltips_text.get(button.objectName(), ""))
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def set_edit_text(self) -> None:
        try:
            text_edits = [self.about_applicaton_text_edit]
            edit_names = [self.about_applicaton_text_edit.objectName()]
            text = LanguageProvider.get_document_text("about", edit_names)
            for text_edit in text_edits:
                text_edit.setHtml(text.get(text_edit.objectName(), ""))
                text_edit.setStyleSheet("font: Arial; font-size: 12pt;")
                text_edit.setReadOnly(True)
                text_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)