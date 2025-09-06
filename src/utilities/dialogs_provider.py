from typing import TYPE_CHECKING

import pathlib

from PyQt6.QtCore import Qt, QThread, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QWidget, QPushButton, QComboBox, \
    QHBoxLayout, QLayout, QProgressBar

from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.threading.download_files_object import DownloadFilesObject


# noinspection PyUnresolvedReferences,PyTypeChecker
class DialogsProvider:
    class_name = "dialogsProvider"

    @staticmethod
    def show_error_dialog(error_message: str, parent=None) -> QDialog:
        dialog = QDialog(parent)
        dialog.setObjectName("errorDialog")
        DialogsProvider.set_dialog_icon(dialog)
        dialog.setMinimumSize(300, 100)
        main_layout = QVBoxLayout()
        text_label = QLabel()
        text_label.setObjectName("errorTextLabel")
        text_label.setStyleSheet("font-size: 15pt; font-weight: bold;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(button_box.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.rejected.connect(dialog.reject)
        main_layout.addWidget(text_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        DialogsProvider.get_ui_text([text_label, close_button], error_message)
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
        DialogsProvider.get_ui_text([text_label, close_button], db_error)
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
    def get_ui_text(widgets: list[QWidget], error_message: str, parent=None) -> None:
        try:
            ui_text = LanguageProvider.get_json_text("dialog_text.json", DialogsProvider.class_name)
            if ui_text:
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            widget.setText(error_message)
                        if isinstance(widget, QPushButton):
                            widget.setText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            from src.utilities.error_handler import ErrorHandler
            ErrorHandler.exception_handler(e, parent)


class DownloadFilesDialog(QDialog):

    def __init__(self, download_files_object: "DownloadFilesObject") -> None:
        super().__init__()
        self.setObjectName("downloadFilesDialog")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.download_files_object = download_files_object
        self.setLayout(self.create_gui())
        self.start_download()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.download_text_label = QLabel("Downloading files...")
        self.download_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_text_label.setStyleSheet("font-weight: bold;")
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(15)
        self.progress_text_label = QLabel()
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_text_label)
        main_layout.addWidget(self.download_text_label)
        main_layout.addLayout(progress_layout)
        return main_layout

    def start_download(self) -> None:
        self.thread = QThread()
        self.download_files_object.moveToThread(self.thread)
        self.thread.started.connect(self.download_files_object.download_files)
        self.download_files_object.download_progress.connect(self.download_progress)
        self.download_files_object.download_finished.connect(self.download_finished)
        self.thread.start()

    def download_progress(self, downloaded: int, total: int) -> None:
        self.progress_bar.setValue(int(downloaded / total * 100))
        self.progress_text_label.setText(f"{downloaded}/{total}")

    def download_finished(self, success: bool) -> None:
        self.thread.quit()
        self.thread.wait()
        if not success:
            self.download_text_label.setText("Download failed")
            QTimer.singleShot(1000, self.accept)
        else:
            self.download_text_label.setText("Download completed")
            QTimer.singleShot(1000, self.accept)