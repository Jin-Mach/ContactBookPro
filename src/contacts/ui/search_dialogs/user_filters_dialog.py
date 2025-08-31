from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton

from src.contacts.ui.search_dialogs.search_widgets.user_filters_listwidget import UserFiltersListWidget
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker,PyUnresolvedReferences
class UserFiltersDialog(QDialog):
    def __init__(self, delete_filter: Callable[[str], None], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("userFiltersDialog")
        self.delete_filter = delete_filter
        self.setFixedSize(400, 300)
        self.setLayout(self.create_gui())
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            self.buttons = button_box.findChildren(QPushButton)
        self.set_ui_text()
        self.set_tooltips_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.user_filters_text_label = QLabel()
        self.user_filters_text_label.setObjectName("userFiltersTextLabel")
        self.user_filters_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_filters_text_label.setStyleSheet("font-size: 20pt;")
        self.user_filters_listwidget = UserFiltersListWidget(self.delete_filter, self)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.check_selected_filter)
        button_box.rejected.connect(self.reject)
        self.filter_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.filter_button.setObjectName("filterButton")
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_button.setObjectName("cancelButton")
        main_layout.addWidget(self.user_filters_text_label)
        main_layout.addWidget(self.user_filters_listwidget)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_json_text("user_filters_dialog_text.json", self.objectName())
            widgets = self.findChildren(QLabel)
            if ui_text:
                if "dialogTitle" in ui_text:
                    self.setWindowTitle(ui_text.get("dialogTitle", ""))
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            widget.setText(ui_text.get(widget.objectName(), ""))
                for button in self.buttons:
                    if button.objectName() in ui_text:
                        button.setText(ui_text.get(button.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltip_text = LanguageProvider.get_json_text("tooltips_text.json", self.objectName())
            if tooltip_text:
                for button in self.buttons:
                    if button.objectName() in tooltip_text:
                        button.setToolTip(tooltip_text.get(button.objectName(), ""))
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def check_selected_filter(self) -> str | None:
        try:
            error_text = LanguageProvider.get_json_text("errors_text.json", self.objectName())
            if self.user_filters_listwidget.model().rowCount() < 1:
                if error_text:
                    DialogsProvider.show_error_dialog(error_text.get("noFilters", ""), self)
                return None
            selected_filter = self.user_filters_listwidget.return_selected_filter()
            if not selected_filter:
                if error_text:
                    DialogsProvider.show_error_dialog(error_text.get("noSelection", ""), self)
                return None
            self.accept()
            return selected_filter
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None