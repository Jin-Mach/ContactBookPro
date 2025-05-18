from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton

from src.contacts.contacts_ui.search_dialog.search_widgets.filters_listview_widget import FiltersListviewWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class CurrentFilterDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("currentFilterDialog")
        self.setMinimumSize(300, 200)
        self.setLayout(self.create_gui())
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            self.buttons = button_box.findChildren(QPushButton)
        self.set_ui_text()
        self.set_tooltips_text()


    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.current_filter_text_label = QLabel()
        self.current_filter_text_label.setObjectName("currentFilterTextLabel")
        self.current_filter_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_filter_text_label.setStyleSheet("font-size: 25px; font-family: Arial;")
        self.filters_listview = FiltersListviewWidget(self)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.reject)
        main_layout.addWidget(self.current_filter_text_label)
        main_layout.addWidget(self.filters_listview)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            if "currentFilterTitle" in ui_text:
                self.setWindowTitle(ui_text["currentFilterTitle"])
            for widget in self.findChildren(QLabel):
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
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            for button in self.buttons:
                if button.objectName() in tooltips_text:
                    button.setToolTip(tooltips_text[button.objectName()])
                    button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)