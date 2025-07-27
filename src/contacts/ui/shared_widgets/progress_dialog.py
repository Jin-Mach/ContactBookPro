from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QProgressBar

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ProgressDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("progressDialog")
        self.setFixedSize(250, 70)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint |Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.search_text_label = QLabel()
        self.search_text_label.setObjectName("searchTextLabel")
        self.search_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setRange(0, 0)
        main_layout.addWidget(self.search_text_label)
        main_layout.addWidget(self.progress_bar)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            widgets = self.findChildren(QLabel)
            for widget in widgets:
                if widget.objectName() in ui_text:
                    widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def show_dialog(self) -> None:
        if not self.isVisible():
            self.show()

    def hide_dialog(self) -> None:
        if self.isVisible():
            self.hide()