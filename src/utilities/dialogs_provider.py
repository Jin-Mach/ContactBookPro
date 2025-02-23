from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QWidget, QPushButton

from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class DialogsProvider:
    class_name = "dialogsProvider"

    @staticmethod
    def show_error_dialog(error_message: str, parent=None) -> QDialog:
        dialog = QDialog(parent)
        dialog.setObjectName("errorDialog")
        dialog.setMinimumSize(250, 100)
        main_layout = QVBoxLayout()
        text_label = QLabel()
        text_label.setObjectName("errorTextLabel")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        main_layout.addWidget(text_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        DialogsProvider.get_ui_text(dialog, [text_label], error_message)
        return dialog.exec()

    @staticmethod
    def show_language_error_dialog(files: list) -> QDialog:
        dialog = QDialog()
        dialog.setMinimumSize(250, 100)
        main_layout = QVBoxLayout()
        text_label = QLabel(f"Critical error: Failed to load files: {files}.\nContinue without UI text or close application?")
        text_label.setObjectName("languageErrorTextLabel")
        font = QFont()
        font.setBold(True)
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close)
        continue_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        continue_button.setText("Continue")
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        main_layout.addWidget(text_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        return dialog.exec()

    @staticmethod
    def show_database_error_dialog(db_error: str) -> QDialog:
        dialog = QDialog()
        dialog.setMinimumSize(250, 100)
        main_layout = QVBoxLayout()
        text_label = QLabel()
        text_label.setObjectName("databaseErrorTextLabel")
        font = QFont()
        font.setBold(True)
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("databaseCloseButton")
        button_box.rejected.connect(dialog.reject)
        main_layout.addWidget(text_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        DialogsProvider.get_ui_text(dialog, [text_label, close_button], db_error)
        return dialog.exec()

    @staticmethod
    def get_ui_text(dialog: QDialog, widgets: list[QWidget], error_message: str, parent=None) -> None:
        ui_text = LanguageProvider.get_dialog_text(DialogsProvider.class_name)
        try:
            if "dialogTitle" in ui_text:
                dialog.setWindowTitle(ui_text["dialogTitle"])
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QLabel):
                        widget.setText(f"{ui_text[widget.objectName()]}\n{error_message}")
                    if isinstance(widget, QPushButton):
                        widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            from src.utilities.error_handler import ErrorHandler
            ErrorHandler.exception_handler(e, parent)