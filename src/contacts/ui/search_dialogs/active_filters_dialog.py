from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton

from src.contacts.ui.search_dialogs.search_widgets.filters_tableview_widget import FiltersTableviewWidget
from src.contacts.ui.search_dialogs.search_widgets.search_mandatory_widget import SearchMandatoryWidget
from src.contacts.ui.search_dialogs.search_widgets.search_non_mandatory_widget import SearchNonMandatoryWidget
from src.database.models.advanced_filter_model import AdvancedFilterModel
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class ActiveFiltersDialog(QDialog):
    def __init__(self, advanced_filter_model: AdvancedFilterModel, remove_filter: Callable[[int, AdvancedFilterModel], None],
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
            if ui_text:
                if "currentFilterTitle" in ui_text:
                    self.setWindowTitle(ui_text.get("currentFilterTitle", ""))
                for widget in self.findChildren(QLabel):
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
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            if tooltips_text:
                for button in self.buttons:
                    if button.objectName() in tooltips_text:
                        button.setToolTip(tooltips_text.get(button.objectName(), ""))
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def save_current_filter(self) -> None:
        try:
            if not self.filters_tableview_widget.advanced_filter_model.rowCount() > 0:
                error_text = LanguageProvider.get_error_text(self.objectName())
                if error_text:
                    DialogsProvider.show_error_dialog(error_text.get("noActiveFilter", ""), self)
                return
            from src.contacts.controlers.filters_controller import FiltersController
            controller = FiltersController(self.search_mandatory_widget, self.search_non_mandatory_widget, self)
            controller.save_filter()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def reset_active_filters_widgets(self, row: int, model: AdvancedFilterModel) -> None:
        try:
            filter_item = model.filter_data[row]
            combobox_widget = filter_item.get("combobox", None)
            edit_widget = filter_item.get("edit", None)
            if combobox_widget:
                combobox_widget.setCurrentIndex(0)
            if edit_widget:
                edit_widget.clear()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)