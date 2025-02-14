from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

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
        DialogsProvider.get_ui_text(dialog, text_label, error_message)
        dialog.exec()
        return dialog

    @staticmethod
    def get_ui_text(dialog: QDialog, text_label: QLabel, error_message: str) -> None:
        ui_text = LanguageProvider.get_dialog_text(DialogsProvider.class_name)
        widgets = [text_label]
        if "dialogTitle" in ui_text:
            dialog.setWindowTitle(ui_text["dialogTitle"])
        else:
            print("error")
        for widget in widgets:
            if widget.objectName() in ui_text:
                if isinstance(widget, QLabel):
                        widget.setText(f"{ui_text[widget.objectName()]}\n{error_message}")
            else:
                print("error")