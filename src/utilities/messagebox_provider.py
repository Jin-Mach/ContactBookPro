from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QLabel

if TYPE_CHECKING:
    from src.application.main_window import MainWindow


class MessageboxProvider:

    @staticmethod
    def close_application_messagebox(ui_text: dict[str, str], parent: "MainWindow") -> bool:
        messagebox = QMessageBox(parent)
        messagebox.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        messagebox.setWindowTitle(ui_text.get("messageboxTitle", ""))
        messagebox.setIcon(QMessageBox.Icon.Question)
        messagebox.setText(ui_text.get("messageboxText", ""))
        messagebox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        messagebox.setDefaultButton(QMessageBox.StandardButton.Cancel)
        close_app_button = messagebox.button(QMessageBox.StandardButton.Ok)
        close_app_button.setText(ui_text.get("close", ""))
        close_messagebox_button = messagebox.button(QMessageBox.StandardButton.Cancel)
        close_messagebox_button.setText(ui_text.get("cancel"))
        for label in messagebox.findChildren(QLabel):
            if isinstance(label, QLabel) and label.objectName() == "qt_msgbox_label":
                label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        return messagebox.exec() == QMessageBox.StandardButton.Ok