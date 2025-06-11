from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QTabWidget, QDialogButtonBox, QPushButton

from src.contacts.ui.search_dialogs.search_widgets.search_mandatory_widget import SearchMandatoryWidget
from src.contacts.ui.search_dialogs.search_widgets.search_non_mandatory_widget import SearchNonMandatoryWidget
from src.contacts.controlers.filters_controler import FiltersControler
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class AdvancedSearchDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("advancedSearchDialog")
        self.setFixedSize(600, 600)
        self.setLayout(self.create_gui())
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            self.buttons = button_box.findChildren(QPushButton)
        self.set_ui_text()
        self.set_toolpips_text()
        IconProvider.set_buttons_icon(self.objectName(), self.buttons, QSize(35, 35))
        self.active_filters_controler = FiltersControler(self.search_mandatory_widget, self.search_non_mandatory_widget, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.search_tab_widget = QTabWidget()
        self.search_tab_widget.setObjectName("searchTabWidget")
        self.search_mandatory_widget = SearchMandatoryWidget(self)
        self.search_non_mandatory_widget = SearchNonMandatoryWidget(self)
        self.search_tab_widget.addTab(self.search_mandatory_widget, "")
        self.search_tab_widget.addTab(self.search_non_mandatory_widget, "")
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel |
                                      QDialogButtonBox.StandardButton.Reset | QDialogButtonBox.StandardButton.RestoreDefaults)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.search_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        self.search_button.setObjectName("searchButton")
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_button.setObjectName("cancelButton")
        self.reset_button = button_box.button(QDialogButtonBox.StandardButton.Reset)
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_all_filters)
        self.current_filter_button = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        self.current_filter_button.setObjectName("currentFilterButton")
        self.current_filter_button.clicked.connect(self.show_current_filter_dialog)
        main_layout.addWidget(self.search_tab_widget)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            tab_text = ["mandatory", "nonMandatory"]
            if "dialogTitle" in ui_text:
                self.setWindowTitle(ui_text["dialogTitle"])
            for index, text in enumerate(tab_text):
                if text in ui_text:
                    self.search_tab_widget.setTabText(index, ui_text[text])
            for button in self.buttons:
                if button.objectName() in ui_text:
                    button.setText(ui_text[button.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_toolpips_text(self) -> None:
        tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
        for button in self.buttons:
            if button.objectName() in tooltips_text:
                button.setToolTip(tooltips_text[button.objectName()])
                button.setToolTipDuration(5000)

    def reset_all_filters(self) -> None:
        self.search_tab_widget.setCurrentIndex(0)
        self.search_non_mandatory_widget.non_mandatory_tab_widget.setCurrentIndex(0)
        self.search_mandatory_widget.reset_all_filters()
        self.search_non_mandatory_widget.search_work_widget.reset_all_filters()
        self.search_non_mandatory_widget.search_social_networks_widget.reset_all_filters()
        self.search_non_mandatory_widget.search_details_widget.reset_all_filters()

    def get_finall_filter(self) -> dict:
        try:
            filters = {"mandatory": self.search_mandatory_widget.return_mandatory_filter(),
                       "work": self.search_non_mandatory_widget.search_work_widget.return_work_filter(),
                       "social": self.search_non_mandatory_widget.search_social_networks_widget.return_social_filter(),
                       "detail": self.search_non_mandatory_widget.search_details_widget.return_detail_filter()
                       }
            empty_filters = set()
            for key in filters:
                new_filter, value = filters[key]
                if not new_filter:
                    empty_filters.add(key)
            if empty_filters:
                for table in empty_filters:
                    filters.pop(table)
            return filters
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return {}

    def show_current_filter_dialog(self) -> None:
        self.active_filters_controler.show_active_filters()