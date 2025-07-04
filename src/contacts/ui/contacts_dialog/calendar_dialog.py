from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QDialogButtonBox, QPushButton, QLineEdit

from src.contacts.ui.contacts_dialog.dialog_widgets.calendar_widget import CalendarWidget
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences,PyTypeChecker
class CalendarDialog(QDialog):
    def __init__(self, birthday_input: QLineEdit, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("calendarDialog")
        self.setMinimumSize(450, 350)
        IconProvider.set_window_icon(self, "mainWindow")
        self.birthday_input = birthday_input
        self.setLayout(self.create_gui())
        self.buttons = self.findChildren(QPushButton)
        self.set_ui_text()
        self.set_tooltips_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.calendar_widget = CalendarWidget(self)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.RestoreDefaults | QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(lambda: self.return_date(self.birthday_input))
        button_box.rejected.connect(self.reject)
        self.set_today_button = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        self.set_today_button.setObjectName("setTodayButton")
        self.set_today_button.clicked.connect(self.calendar_widget.set_today)
        self.add_date_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.add_date_button.setObjectName("addDateButton")
        self.cancel_dialog_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_dialog_button.setObjectName("cancelDialogButton")
        main_layout.addWidget(self.calendar_widget)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_dialog_text(self.objectName())
            if ui_text:
                if "calendarDialogTitle" in ui_text:
                    self.setWindowTitle(ui_text.get("calendarDialogTitle", ""))
                for button in self.buttons:
                    if button.objectName() in ui_text:
                        if isinstance(button, QPushButton):
                            button.setText(ui_text.get(button.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            for button in self.buttons:
                if button.objectName() in tooltips_text:
                    button.setToolTip(tooltips_text.get(button.objectName(), ""))
                    button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def return_date(self, birthday_input: QLineEdit) -> str | None:
        try:
            error_text = LanguageProvider.get_error_text(self.objectName())
            selected_date = self.calendar_widget.return_selected_date()
            if selected_date:
                birthday_input.setText(selected_date)
                self.accept()
                return birthday_input.text()
            DialogsProvider.show_error_dialog(error_text.get("selectedDateError", ""), self)
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e, self)