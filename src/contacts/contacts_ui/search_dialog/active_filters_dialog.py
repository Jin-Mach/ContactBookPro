from typing import Callable

from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton, QComboBox, QLineEdit

from src.contacts.contacts_ui.search_dialog.search_widgets.filters_tableview_widget import FiltersTableviewWidget
from src.contacts.contacts_ui.search_dialog.search_widgets.search_mandatory_widget import SearchMandatoryWidget
from src.contacts.contacts_ui.search_dialog.search_widgets.search_non_mandatory_widget import SearchNonMandatoryWidget
from src.database.models.advanced_filter_model import AdvancedFilterModel
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class ActiveFiltersDialog(QDialog):
    def __init__(self, advanced_filter_model: AdvancedFilterModel, remove_filter: Callable[[int, QAbstractTableModel], None],
                 search_mandatory_widget: SearchMandatoryWidget, search_non_mandatory_widget: SearchNonMandatoryWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("activeFiltersDialog")
        self.setMinimumSize(700, 400)
        self.advanced_filter_model = advanced_filter_model
        self.remove_filter = remove_filter
        self.search_mandatory_widget = search_mandatory_widget
        self.search_non_mandatory_widget = search_non_mandatory_widget
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
        self.filters_tableview_widget = FiltersTableviewWidget(self.advanced_filter_model, self.remove_filter, self)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Reset | QDialogButtonBox.StandardButton.Close)
        save_filter = button_box.button(QDialogButtonBox.StandardButton.Reset)
        save_filter.setObjectName("saveFilter")
        save_filter.clicked.connect(self.save_current_filter)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.reject)
        main_layout.addWidget(self.current_filter_text_label)
        main_layout.addWidget(self.filters_tableview_widget)
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

    def save_current_filter(self) -> None:
        from src.controlers.active_filters_controler import ActiveFiltersControler
        controler = ActiveFiltersControler(self.search_mandatory_widget, self.search_non_mandatory_widget, self)
        controler.save_filter()

    def reset_active_filters_widgets(self, row: int, model: QAbstractTableModel) -> None:
        try:
            filter_item = model.filter_data[row]
            combobox_widget = filter_item["combobox"]
            edit_widget = filter_item["edit"]
            if combobox_widget:
                combobox_widget.setCurrentIndex(0)
            if edit_widget:
                edit_widget.clear()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)