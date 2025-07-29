from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QPushButton

from src.contacts.ui.shared_widgets.validated_lineedit import ValidatedLineedit
from src.contacts.utilities.contact_validator import ContactValidator
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class FilterNameDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("filterNameDialog")
        self.setFixedSize(400, 200)
        self.setLayout(self.create_gui())
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            self.buttons = button_box.findChildren(QPushButton)
        self.set_ui_text()
        self.set_tooltips_text()
        ContactValidator.filter_name_input_validator(self.filter_name_input)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        filter_name_text_label = QLabel()
        filter_name_text_label.setObjectName("filterNameTextLabel")
        filter_name_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filter_name_text_label.setStyleSheet("font-size: 20pt;")
        self.filter_name_input = ValidatedLineedit(self)
        self.filter_name_input.setObjectName("filterNameInput")
        self.filter_name_input.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        save_filter_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        save_filter_button.setObjectName("saveFilterButton")
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setObjectName("cancelButton")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(filter_name_text_label)
        main_layout.addWidget(self.filter_name_input)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            if ui_text:
                if "dialogTitle" in ui_text:
                    self.setWindowTitle(ui_text.get("dialogTitle", ""))
                widgets = self.findChildren((QLabel, QLineEdit))
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            widget.setText(ui_text.get(widget.objectName(), ""))
                        elif isinstance(widget, QLineEdit):
                            widget.setPlaceholderText(ui_text.get(widget.objectName(), ""))
                for button in self.buttons:
                    if button.objectName() in ui_text:
                        button.setText(ui_text.get(button.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltip_text = LanguageProvider.get_tooltips_text(self.objectName())
            if tooltip_text:
                for button in self.buttons:
                    if button.objectName() in tooltip_text:
                        button.setToolTip(tooltip_text.get(button.objectName(), ""))
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def get_filter_name(self) -> str | None:
        try:
            error_text = LanguageProvider.get_error_text(self.objectName())
            input_text = self.filter_name_input.text().strip()
            if not input_text:
                if error_text:
                    DialogsProvider.show_error_dialog(error_text.get("emptyFilterName", ""), self)
                return None
            self.accept()
            return input_text
        except Exception as e:
            ErrorHandler.exception_handler(e, self)