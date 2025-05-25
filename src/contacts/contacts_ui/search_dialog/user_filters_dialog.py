from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton

from src.contacts.contacts_ui.search_dialog.search_widgets.user_filters_listwidget_widget import UserFiltersListwidgetWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class UserFiltersDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("userFiltersDialog")
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
        self.user_filters_text_label.setStyleSheet("font-size: 25px; font-family: Arial;")
        user_filters_listwidget = UserFiltersListwidgetWidget()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.filter_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.filter_button.setObjectName("filterButton")
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_button.setObjectName("cancelButton")
        main_layout.addWidget(self.user_filters_text_label)
        main_layout.addWidget(user_filters_listwidget)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_user_filters_dialog_text(self.objectName())
            widgets = self.findChildren(QLabel)
            if "dialogTitle" in ui_text:
                self.setWindowTitle(ui_text["dialogTitle"])
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QLabel):
                        widget.setText(ui_text[widget.objectName()])
            for button in self.buttons:
                if button.objectName() in ui_text:
                    button.setText(ui_text[button.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltip_text = LanguageProvider.get_tooltips_text(self.objectName())
            for button in self.buttons:
                if button.objectName() in tooltip_text:
                    button.setToolTip(tooltip_text[button.objectName()])
                    button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)