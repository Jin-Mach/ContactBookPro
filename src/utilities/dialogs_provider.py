import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QWidget, QPushButton, QComboBox, QHBoxLayout

from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences,PyTypeChecker
class DialogsProvider:
    class_name = "dialogsProvider"

    @staticmethod
    def show_error_dialog(error_message: str, parent=None) -> QDialog:
        dialog = QDialog(parent)
        dialog.setObjectName("errorDialog")
        DialogsProvider.set_dialog_icon(dialog)
        dialog.setMinimumSize(250, 100)
        main_layout = QVBoxLayout()
        text_label = QLabel()
        text_label.setObjectName("errorTextLabel")
        text_label.setStyleSheet("font-size: 15pt; font-weight: bold;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        main_layout.addWidget(text_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        DialogsProvider.get_ui_text(dialog, [text_label], error_message)
        return dialog.exec()

    @staticmethod
    def show_init_error_dialog(title: str, error_text: str) -> QDialog:
        dialog = QDialog()
        dialog.setWindowTitle(title)
        DialogsProvider.set_dialog_icon(dialog)
        dialog.setMinimumSize(250, 100)
        main_layout = QVBoxLayout()
        text_label = QLabel(error_text)
        text_label.setStyleSheet("font-size: 15pt; font-weight: bold;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        main_layout.addWidget(text_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        return dialog.exec()

    @staticmethod
    def show_database_error_dialog(db_error: str) -> QDialog:
        dialog = QDialog()
        DialogsProvider.set_dialog_icon(dialog)
        dialog.setMinimumSize(250, 100)
        main_layout = QVBoxLayout()
        text_label = QLabel()
        text_label.setObjectName("databaseErrorTextLabel")
        text_label.setStyleSheet("font-size: 15pt; font-weight: bold;")
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
    def language_selection_dialog(language_list: list) -> str:
        dialog = QDialog()
        DialogsProvider.set_dialog_icon(dialog)
        dialog.setWindowTitle("Language error")
        main_layout = QVBoxLayout()
        text_label = QLabel("The selected language could not be loaded.\nPlease select a supported language from the list,\n"
                            "or exit the application.")
        text_label.setStyleSheet("font-size: 15pt; font-weight: bold;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        combobox_layout = QHBoxLayout()
        combobox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        language_combobox = QComboBox()
        language_combobox.setFixedWidth(250)
        language_combobox.addItems(language_list)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close)
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Start application")
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        combobox_layout.addWidget(language_combobox)
        main_layout.addWidget(text_label)
        main_layout.addLayout(combobox_layout)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return language_combobox.currentText()
        return ""

    @staticmethod
    def set_dialog_icon(dialog: QDialog) -> None:
        try:
            icon_path = pathlib.Path(__file__).parent.parent.joinpath("icons", "mainWindow", "window_icon.png")
            if icon_path.exists():
                dialog.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            from src.utilities.error_handler import ErrorHandler
            ErrorHandler.exception_handler(e, dialog)

    @staticmethod
    def get_ui_text(dialog: QDialog, widgets: list[QWidget], error_message: str, parent=None) -> None:
        try:
            ui_text = LanguageProvider.get_dialog_text(DialogsProvider.class_name)
            if ui_text:
                if "dialogTitle" in ui_text:
                    dialog.setWindowTitle(ui_text.get("dialogTitle", ""))
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            widget.setText(error_message)
                        if isinstance(widget, QPushButton):
                            widget.setText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            from src.utilities.error_handler import ErrorHandler
            ErrorHandler.exception_handler(e, parent)